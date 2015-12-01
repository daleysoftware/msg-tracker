import unittest
import msgtracker


def test_suite():
    return msgtracker.test.test_suite()


if __name__ == "__main__":
    unittest.main(defaultTest='test_suite', testRunner=unittest.TextTestRunner())
