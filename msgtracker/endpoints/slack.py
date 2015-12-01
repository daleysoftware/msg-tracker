import logging
import json
import os
import sys
import slackclient


def _slack_result_to_json(slack_result):
    return json.loads(slack_result.decode('utf-8'))


class Slack:
    def __init__(self):
        self.client = Slack.get_client_from_env_token()


    @staticmethod
    def get_client_from_env_token():
        slack_token = os.environ.get('SLACK_TOKEN')
        if slack_token is None:
            message = 'Environment variable SLACK_TOKEN is absent. Abort.'
            print(message)
            logging.error(message)
            sys.exit(1)
        return slackclient.SlackClient(slack_token)


    def get_users(self):
        """
        Get users that have not been deleted from the slack API. Return users as a list.
        """
        logging.info("Getting active users.")
        result = []
        for member in _slack_result_to_json(self.client.api_call('users.list'))['members']:
            if not member['deleted']:
                result.append(member['id'])
        return result


    def get_active_users(self):
        """
        Get active slack users using the slack API. Return users as a list.
        """
        result = []
        for user in self.get_users():
            logging.info("Presence check id=%s" % user)
            if _slack_result_to_json(self.client.api_call('users.getPresence', user=user))['presence'] == 'active':
                logging.debug("User %s is online" % user)
                result.append(user)
        return result
