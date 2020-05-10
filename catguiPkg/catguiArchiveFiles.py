import datetime
import logging
import os

from openpyxl import Workbook
from pathlib import Path

import catgui

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


def scan_files(window, scan_parameters):
    logger.info(f"archive_scan_files()")


    args = catgui.getargs()
    if args.verbose: print(f"Options: {args}")

    wb = Workbook()

    ws1 = wb.active
    ws1.title = 'Summary'
    

    ws1['A1']= f"Scan summary "
    for parameter_key in sorted(scan_parameters):
        ws1.append((parameter_key, scan_parameters[parameter_key]))

    ws2 = wb.create_sheet('Files')
    header_row = ('Directory', 'Filename', 'size', 'created', 'modified', 'md5')
    ws2.append(header_row)
    ws2.auto_filter.ref = "A:F"
    ws2.freeze_panes = "B2"

    number_files = 0
    number_save = 0
    number_ignore = 0

    DATE_FORMAT = "%Y-%m-%d"
    scan_start_time = datetime.datetime.strptime(scan_parameters['scan_start_date'], DATE_FORMAT)
    start_path = Path(scan_parameters['start_folder'])
    start_dir = Path(start_path)
    if args.verbose: print(f"Start Directory: {start_dir}")

    for path in Path(scan_parameters['start_folder']).rglob('*'):
        if path.parent != start_dir:
            start_dir = path.parent
            if args.verbose: print(f"Directory change: {start_dir}")
        if (os.path.isfile(path)):
            number_files += 1
            st = os.stat(path)
            create_date = datetime.datetime.fromtimestamp(st.st_ctime).strftime(DATE_FORMAT)
            mod_date_time = datetime.datetime.fromtimestamp(st.st_mtime)
            mod_date = mod_date_time.strftime(DATE_FORMAT)
            if scan_start_time < mod_date_time:
                number_save += 1

                t = (f"{path.parent}", path.name, st.st_size, 
                datetime.datetime.fromtimestamp(st.st_mtime), 
                datetime.datetime.fromtimestamp(st.st_ctime))
                ws2.append(t)

                if args.verbose: 
                    print(f"\t{number_files}: {st.st_size} {create_date} {mod_date} {path.name}")
            else:
                number_ignore += 1

    print(f"Total files found {number_files}")
    print(f"  Number of modified files since the scan date {number_save}")
    print(f"  Number of files last modified before the scan date {number_ignore}")

    summary = {
        'total files': number_files,
        'Modified files': number_save, 
        'Ignored': number_ignore
        }
    for summary_key in summary:
        ws1.append((summary_key, summary[summary_key]))
    # ws1.append(summary)

    filename = f'backup_scan_{datetime.datetime.now().strftime("%Y%m%dt%H%M%S")}.xlsx'
    if 'target_folder' in scan_parameters:
        filepath = Path(scan_parameters['target_folder'], filename)
        wb.save(filepath)
        logger.info(f"Scan summary saved: {filepath}")

    wb.close()
    