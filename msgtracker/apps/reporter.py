import argparse
import time
import tzlocal
import pytz
import msgtracker
import datetime


algorithm = msgtracker.algorithm.Algorithm(msgtracker.constants.POST_SESSION_PADDING_SECONDS)


def main(interval_length_days, max_results, timezone, slack_client):
    users = slack_client.get_users()
    for user in users:
        # Max datetime is the beginning of today, using the provided timezone.
        max_datetime = datetime.datetime.now(tz=timezone).date()
        min_datetime = max_datetime - datetime.timedelta(days=(interval_length_days * max_results))
        max_epoch = int(time.mktime(max_datetime.timetuple()))
        min_epoch = int(time.mktime(min_datetime.timetuple()))

        active_points = msgtracker.backend.get_user_active_points(user, min_epoch, max_epoch)

        print('---')
        print(user)
        print(active_points)
        print(algorithm.compute_active_seconds(active_points, min_epoch, max_epoch, interval_length_days * 24*60*60))
        # TODO pretty print


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-i", "--interval-length-days",
                        required=False,
                        default=1,
                        help="the query interval length in days")
    parser.add_argument("-m", "--max-intervals",
                        required=False,
                        default=7,
                        help="the maximum number of result intervals to display")
    local_tz = tzlocal.get_localzone()
    parser.add_argument("-t", "--timezone",
                        required=False,
                        default=local_tz.tzname(None),
                        help="report timezone")
    args = parser.parse_args()
    #msgtracker.helper.logging.init()
    main(args.interval_length_days, args.max_intervals, pytz.timezone(args.timezone), msgtracker.endpoints.slack.Slack())
