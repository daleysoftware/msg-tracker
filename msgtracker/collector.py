import sched
import time
import os
import sys
import json
import logging
import slackclient
import msgtracker
import datetime
import signal


scheduler = sched.scheduler(time.time, time.sleep)


def _slack_result_to_json(slack_result):
    return json.loads(slack_result.decode('utf-8'))


def _get_active_users(slack_client):
    """
    Get active slack users using the slack API. Return users as a list.
    """
    logging.info("Getting active users.")
    result = []
    for member in _slack_result_to_json(slack_client.api_call('users.list'))['members']:
        if not member['deleted']:
            user = member['id']
            logging.info("Presence check id=%s name=%s" % (user, member['name']))
            if _slack_result_to_json(slack_client.api_call('users.getPresence', user=user))['presence'] == 'active':
                logging.debug("User %s is online" % user)
                result.append(user)
    return result


def _collect_and_log_forever(slack_client):
    """
    Collect data from slack API and log in redis. Backend handles logging format. Run forever.
    """
    logging.info("Collect and log sequence queued. Here we go...")
    sample_time = datetime.datetime.now()
    for user in _get_active_users(slack_client):
        msgtracker.backend.log_active(user, sample_time)

    # And enter on the scheduler to keep things rolling.
    logging.info("Wait %s minutes." % msgtracker.constants.QUERY_INTERVAL_MINUTES)
    scheduler.enter(msgtracker.constants.QUERY_INTERVAL_MINUTES * 60, 1, _collect_and_log_forever,
                    argument=(slack_client,))


def signal_handler(signum, frame):
    print() # Cosmetics.
    logging.error("Received signal. Abort.")
    sys.exit(1)


def main(slack_client):
    """
    Main program. Kick off scheduler and run forever.
    """
    signal.signal(signal.SIGINT, signal_handler)
    scheduler.enter(0, 1, _collect_and_log_forever, argument=(slack_client,))
    scheduler.run()


def _parse_env():
    slack_token = os.environ.get('SLACK_TOKEN')
    if slack_token is None:
        print('Environment variable SLACK_TOKEN is absent. Abort.')
        sys.exit(1)
    return slackclient.SlackClient(slack_token)


if __name__ == '__main__':
    msgtracker.logutil.init()
    logging.info("Starting collector service.")
    main(_parse_env())
