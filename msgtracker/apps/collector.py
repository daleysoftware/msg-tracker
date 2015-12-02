import sched
import time
import sys
import logging
import msgtracker
import datetime
import signal


scheduler = sched.scheduler(time.time, time.sleep)


def _collect_and_log_forever(slack_client):
    """
    Collect data from slack API and log in redis. Backend handles logging format. Run forever.
    """
    wait_minutes = msgtracker.constants.QUERY_INTERVAL_MINUTES
    try:
        logging.info("Collect and log sequence queued.")
        sample_time = datetime.datetime.utcnow()
        for user in slack_client.get_active_users():
            msgtracker.backend.log_active(user, sample_time)
    except IOError as e:
        wait_minutes = 1
        logging.error("IO error during collection round, retry soon. Error: %s" % e)

    # And enter on the scheduler to keep things rolling.
    logging.info("Wait %s minutes." % wait_minutes)
    scheduler.enter(wait_minutes * 60, 1, _collect_and_log_forever, argument=(slack_client,))


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


if __name__ == '__main__':
    msgtracker.helper.logging.init()
    logging.info("Starting collector service.")
    main(msgtracker.endpoints.slack.Slack())
