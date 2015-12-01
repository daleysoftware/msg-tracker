# Prefix for keys stored in the redis backing store.
REDIS_PREFIX = 'msg-tracker'

# The time interval used for querying the messaging endpoint.
QUERY_INTERVAL_MINUTES = 10

# The amount of time after which the messaging endpoint detects a user as offline and marks their
# status as such.
AUTO_LOGOUT_MINUTES = 30
AUTO_LOGOUT_SECONDS = AUTO_LOGOUT_MINUTES * 60

# The amount of time that we tack on to a session. Somewhat pulling this number out of the air,
# since we don't know if it was a clean logout or a walk-away.
POST_SESSION_PADDING_MINUTES = int(AUTO_LOGOUT_MINUTES / 2)
POST_SESSION_PADDING_SECONDS = POST_SESSION_PADDING_MINUTES * 60