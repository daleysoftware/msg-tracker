import redis
import logging
import msgtracker


redis_client = redis.StrictRedis()


def _format_day(sample_time):
    return "%04d%02d%02d" % (sample_time.year, sample_time.month, sample_time.day)

def _format_twenty_four_hours(sample_time):
    return "%02d:%02d:%02d" % (sample_time.hour, sample_time.minute, sample_time.second)

def _get_key_name(userid, sample_time):
    return '{}_{}_{}'.format(msgtracker.constants.REDIS_PREFIX, userid, _format_day(sample_time))


def log_active(userid, sample_time):
    """
    Log user as active at this particular sample time.

    Database format is a list where the key is a concatenation of the username and day, plus an
    application prefix, and the value is the twenty four hour time of the sampling event.
    """
    redis_client.lpush(_get_key_name(userid, sample_time), _format_twenty_four_hours(sample_time))


def del_all():
    """
    Delete all redis data belonging to this application.
    """
    for key in (redis_client.keys(msgtracker.constants.REDIS_PREFIX + '*')):
        key_decoded = key.decode('utf-8')
        logging.debug("Deleting key %s" % key_decoded)
        redis_client.delete(key_decoded)
