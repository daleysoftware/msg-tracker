import logging
import msgtracker


if __name__ == '__main__':
    msgtracker.logutil.init()
    logging.info("Cleaning all keys belonging to our service.")
    msgtracker.backend.del_all()
