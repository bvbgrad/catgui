import datetime
import logging
import os

from openpyxl import Workbook
from pathlib import Path

import catgui

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


def scan_files(scan_parameters):
    logger.info(f"archive_scan_files()")

    args = catgui.getargs()
    if args.verbose: print(f"Options: {args}")

    wb = Workbook()

    ws1 = wb.active
    ws1.title = 'Summary'

    ws1['A1']= f"Scan summary "
    for parameter_key in sorted(scan_parameters):
        ws1.append((parameter_key, scan_parameters[parameter_key]))

    summary = save2(args, wb, scan_parameters)

    for summary_key in summary:
        ws1.append((summary_key, summary[summary_key]))

    filename = f'backup_scan_{datetime.datetime.now().strftime("%Y%m%dt%H%M%S")}.xlsx'
    if 'target_folder' in scan_parameters:
        filepath = Path(scan_parameters['target_folder'], filename)
        wb.save(filepath)
        logger.info(f"Scan summary saved: {filepath}")

    wb.close()


def file_survey(start_path):
    logger.info("file_survey()")

    excludelist = ('venv', '.mypy', '.git', 'build', 
        'symfony', '.pytest', 'pycache', 'RECYCLE')
    filelist = []
    ignorelist = []
    for row in os.walk(start_path):
        for filename in row[2]: #row[2] is a tuple of the filenames
            full_path: Path = Path(row[0] / Path(filename)) # row[0] is the parent directory
            st = os.stat(full_path)
            filelist.append([
                row[0], filename, st.st_size, 
                datetime.datetime.fromtimestamp(st.st_ctime), 
                datetime.datetime.fromtimestamp(st.st_mtime)
            ])
    
    print(f"number of files scanned = {len(filelist)}")
    excluded_count = 0
    keeplist = []
    for file_object in filelist:
        _exclude = False
        for item in excludelist:
            if item in file_object[0]:
                _exclude = True
        if _exclude:
            excluded_count += 1
            ignorelist.append(file_object)
        else:
            keeplist.append(file_object)
        
    print(f"number of ignored entries {excluded_count}")
    print(f"number of entries retained {len(keeplist)}")

    lists = (keeplist, ignorelist)
    return lists


def save2(args, wb, scan_parameters):
    logger.info("save2()")

    ws2 = wb.create_sheet('Files')
    header_row = ('Directory', 'Filename', 'size', 'created', 'modified', 'md5')
    ws2.append(header_row)
    ws2.auto_filter.ref = "A:F"
    ws2.freeze_panes = "B2"

    ws2d = wb.create_sheet('Ignore')
    ws2d.append(header_row)
    ws2d.auto_filter.ref = "A:F"
    ws2d.freeze_panes = "B2"

    keeplist, ignorelist = file_survey(scan_parameters['start_folder'])

    for file_object in ignorelist: #save those that were ignored in the file survey
        ws2d.append(file_object)

    number_files = 0
    number_save = 0
    number_ignore = 0

    DATE_FORMAT = "%Y-%m-%d"
    scan_start_time = datetime.datetime.strptime(scan_parameters['scan_start_date'], DATE_FORMAT)

    for file_object in keeplist:
        number_files += 1
        if scan_start_time < file_object[3]:
            number_save += 1
            ws2.append(file_object)  # save those within the scan period
        else:
            ws2d.append(file_object)  # add the rest to ignore tab
            number_ignore += 1

    print(f"Total files processed {number_files}")
    print(f"  Number of modified files since the scan date {number_save}")
    print(f"  Number of files ignored {number_ignore}")

    summary = {
    'total files': number_files,
    'Modified files': number_save, 
    'Ignored': number_ignore
    }

    return summary
