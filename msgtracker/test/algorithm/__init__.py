import unittest
from . import algorithm_test


def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(algorithm_test.test_suite())
    return suite
