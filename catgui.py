author = __author__ = 'Brent V. Bingham'
version = __version__ = '0.1'
import argparse
import logging
import os
from logging.handlers import RotatingFileHandler

from pathlib import Path
import sys

from catguiAuxPkg import catguiMenu

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)

def main():
    logger.info("main()")
    args = getargs()

    catguiMenu.menu(author, version, args)


def getargs():
    logger.info("getargs()")
    parser = argparse.ArgumentParser(
        description="A collection of disk file cataloging functions")
    parser.add_argument('-v', '--verbose', default=False,
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
    fh = RotatingFileHandler(f"logs/{LOGGER_NAME}.log", maxBytes=10240, backupCount=10)
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"setup_logging() {LOGGER_NAME} logging initiated")

    logger.debug('debug message')
    logger.warning('warn message')
    logger.error('error message')
    logger.critical('critical message')


if __name__ == "__main__":
    setup_logging()

    main()
