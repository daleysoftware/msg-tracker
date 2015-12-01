import unittest
import msgtracker


algorithm = msgtracker.algorithm.Algorithm(15)


class AlgorithmTest(unittest.TestCase):
    def test__something_something_something(self):
        test_cases = [
                (
                    ([15], 0, 299, 100),
                    [15, 0, 0]
                ),
                (
                    ([15, 20], 0, 299, 100),
                    [20, 0, 0]
                ),
                (
                    ([15, 115, 215], 0, 299, 100),
                    [15, 15, 15]
                ),
        ]

        for tc in test_cases:
            i, o = tc
            active_points, min_epoch, max_epoch, interval_length_seconds = i
            self.assertEqual(o, algorithm.compute_active_seconds(active_points, min_epoch, max_epoch, interval_length_seconds))

def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromName(__name__)

