import logging
import time


def init():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-5.5s %(asctime)s %(message)s')
    logging.Formatter.converter = time.gmtime
