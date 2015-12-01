import unittest
import msgtracker

from . import algorithm

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(msgtracker.test.algorithm.test_suite())
    return suite
