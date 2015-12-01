import redis
import logging
import msgtracker
import datetime


redis_client = redis.StrictRedis()


def _format_day(sample_time):
    return "%04d%02d%02d" % (sample_time.year, sample_time.month, sample_time.day)

def _format_epoch_seconds(sample_time):
    return sample_time.strftime('%s')

def _get_key_name(userid, sample_time):
    return '{}_{}_{}'.format(msgtracker.constants.REDIS_PREFIX, userid, _format_day(sample_time))


def log_active(userid, sample_time):
    """
    Log user as active at this particular sample time.

    Database format is a list where the key is a concatenation of the username and day, plus an
    application prefix, and the value is the twenty four hour time of the sampling event.
    """
    redis_client.lpush(_get_key_name(userid, sample_time), _format_epoch_seconds(sample_time))


def del_all():
    """
    Delete all redis data belonging to this application.
    """
    for key in (redis_client.keys(msgtracker.constants.REDIS_PREFIX + '*')):
        key_decoded = key.decode('utf-8')
        logging.debug("Deleting key %s" % key_decoded)
        redis_client.delete(key_decoded)


def get_user_active_points(userid, min_epoch, max_epoch):
    """
    Get the active user points that have been logged for the given userid for the given inclusize
    range of epoch seconds.
    """
    result = []
    for e in range(min_epoch, max_epoch + 1, 24*60*60):
        key = _get_key_name(userid, datetime.datetime.utcfromtimestamp(e))
        logging.debug("Check key %s" % key)
        try:
            samples = redis_client.lrange(key, 0, -1)
            _, userid, _ = key.split('_')
            for s in samples:
                result.append(int(s.decode('utf-8')))
        except KeyError:
            continue
    return result
