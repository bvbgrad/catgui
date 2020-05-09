import logging

import catgui

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


def scan_files(window, scan_parameters):
    logger.info(f"archive_scan_files()")

    args = catgui.getargs()
    print(f"Options: {args}")

    print(f"Parameters from archive_scan_files(): ")
    for parameter_key in sorted(scan_parameters):
        print(f"\t{parameter_key}:{scan_parameters[parameter_key]}")
