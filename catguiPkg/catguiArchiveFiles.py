import logging

from pathlib import Path

import catgui

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


def scan_files(window, scan_parameters):
    logger.info(f"archive_scan_files()")

    args = catgui.getargs()
    if args.verbose: print(f"Options: {args}")

    print(f"Parameters for this scan: ")
    for parameter_key in sorted(scan_parameters):
        print(f"\t{parameter_key}:{scan_parameters[parameter_key]}")

    i = 0
    for path in Path(scan_parameters['start_folder']).rglob('*'):
        i += 1
        if args.verbose: print(f"File {i}: {path}")

    print(f"Found {i} files")
