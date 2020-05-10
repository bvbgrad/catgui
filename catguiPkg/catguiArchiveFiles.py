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
    number_save = 0
    number_ignore = 0
    DATE_FORMAT = "%Y-%m-%d"
    scan_start_time = datetime.datetime.strptime(scan_parameters['scan_start_date'], DATE_FORMAT)
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
            create_date = datetime.datetime.fromtimestamp(st.st_ctime).strftime(DATE_FORMAT)
            mod_date_time = datetime.datetime.fromtimestamp(st.st_mtime)
            mod_date = mod_date_time.strftime(DATE_FORMAT)
            if scan_start_time < mod_date_time:
                number_save += 1
                if args.verbose: print(f"\t{number_files}: {st.st_size} {create_date} {mod_date} {path.name}")
            else:
                number_ignore += 1
                        

    print(f"Total files found {number_files}")
    print(f"  Number of modified files since the scan date {number_save}")
    print(f"  Number of files last modified before the scan date {number_ignore}")
