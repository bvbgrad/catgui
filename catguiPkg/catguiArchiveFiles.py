import datetime
import logging
import os

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

    number_files = 0
    start_path = Path(scan_parameters['start_folder'])
    start_dir = Path(start_path)
    if args.verbose: 
        print(f"Start Directory: {start_dir}")
        print("\tFile# size created modified Name")

    for path in Path(scan_parameters['start_folder']).rglob('*'):
        if path.parent != start_dir:
            start_dir = path.parent
            print(f"Directory change: {start_dir}")
        if (os.path.isfile(path)):
            number_files += 1
            st = os.stat(path)
            if args.verbose:
                    print(f"\t{number_files}: {st.st_size} {st.st_ctime} {st.st_mtime} {path.name}")

    print(f"Found {number_files} files")
