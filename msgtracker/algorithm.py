class Algorithm:
    def __init__(self, post_session_padding_seconds):
        self.post_session_padding_seconds = post_session_padding_seconds


    def _compute_active_seconds_in_bucket(self, active_points_bucket):
        """
        Compute the number of seconds a user is online for a give day given the activity log times
        for that day (i.e. the active points bucket).

        For simplicity we ignore time before the first bucket entry.
        """
        if len(active_points_bucket) == 0:
            return 0
        if len(active_points_bucket) == 1:
            return self.post_session_padding_seconds
        active_points_bucket = sorted(active_points_bucket)
        result = self.post_session_padding_seconds # For the last point.
        for i in range(0, len(active_points_bucket) - 1):
            a = active_points_bucket[i]
            b = active_points_bucket[i + 1]
            result += b-a if b-a < self.post_session_padding_seconds else self.post_session_padding_seconds
        return result


    def compute_active_seconds(self, active_points, min_epoch, max_epoch, interval_length_seconds):
        """
        Compute the number of active seconds for the given active_points array using the provided
        interval parameters (min_epoch, max_epoch, interval_length_seconds).

        The return value of this function is an array of seconds, which represent the number of
        active seconds in each interval bucket.
        """
        active_points_buckets = []
        for i in range(min_epoch, max_epoch, interval_length_seconds):
            active_points_buckets.append([j for j in active_points if i <=j < i + interval_length_seconds])
        result = []
        for active_points_bucket in active_points_buckets:
            result.append(self._compute_active_seconds_in_bucket(active_points_bucket))
        return result