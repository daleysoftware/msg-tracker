import argparse
import time
import tzlocal
import pytz
import msgtracker
import datetime
import tabulate
import operator


algorithm = msgtracker.algorithm.Algorithm(msgtracker.constants.POST_SESSION_PADDING_SECONDS)


def main(interval_length_days, max_results, timezone, slack_client):
    # Max datetime is the beginning of today, in the provided timezone.
    max_datetime = datetime.datetime.now(tz=timezone).date()
    min_datetime = max_datetime - datetime.timedelta(days=(interval_length_days * max_results))
    max_epoch = int(time.mktime(max_datetime.timetuple()))
    min_epoch = int(time.mktime(min_datetime.timetuple()))
    # Current accounts from slack.
    users = slack_client.get_users()
    table = []
    for user in users:
        active_points = msgtracker.backend.get_user_active_points(user, min_epoch, max_epoch)
        user_activity = algorithm.compute_active_seconds(active_points, min_epoch, max_epoch, interval_length_days * 24*60*60)
        user_name = slack_client.userid_to_readable(user)
        if len(user_name) == 0:
            # Do not report on a user that doesn't have a human readable name.
            continue
        table.append([user_name] + [round(float(sec)/60/60, 1) for sec in user_activity])
    # Pretty date headers.
    formatted_date_strings = []
    for i in range(max_results):
        d = min_datetime + datetime.timedelta(days=(i * interval_length_days))
        formatted_date_strings.append("%s/%s/%s" % (d.month, d.day, d.year))
    headers = [] + formatted_date_strings
    print(tabulate.tabulate(sorted(table, key=operator.itemgetter(0)), headers, tablefmt="grid"))


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
    msgtracker.helper.logging.init()
    main(int(args.interval_length_days), int(args.max_intervals), pytz.timezone(args.timezone), msgtracker.endpoints.slack.Slack())
