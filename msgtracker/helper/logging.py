import logging


def init():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(levelname)-5.5s %(asctime)s %(message)s')
