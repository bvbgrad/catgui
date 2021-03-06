author = __author__ = 'Brent V. Bingham'
version = __version__ = '0.1'
import argparse
import logging
import os
from logging.handlers import RotatingFileHandler

from pathlib import Path
import sys

from catguiPkg import catguiMenu

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


def log_wrap(func):
    def wrapped(*args, **kwargs):
        logger.info(f"enter {func.__name__}()")
        result = func(*args, **kwargs)
        logger.info(f"exit {func.__name__}()")
        return result
    return wrapped


@log_wrap
def main():
    logger.info("main()")

    catguiMenu.menu(author, version)

@log_wrap
def getargs():
    logger.info("getargs()")
    parser = argparse.ArgumentParser(
        description="A collection of disk file cataloging functions")
    parser.add_argument('-v', '--verbose', default=False, action="store_true",
        help='Provide detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s {version}')
    args = parser.parse_args()
    return args


def setup_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # create file handler which logs even debug messages
    fh = RotatingFileHandler(f"logs/{LOGGER_NAME}.log", maxBytes=1000000, backupCount=10)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [%(pathname)s:%(lineno)d]')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"setup_logging(): {LOGGER_NAME} logging initiated")

    logger.debug('example debug message')
    logger.warning('example warn message')
    logger.error('example error message')
    logger.critical('example critical message')


if __name__ == "__main__":
    setup_logging()

    main()
