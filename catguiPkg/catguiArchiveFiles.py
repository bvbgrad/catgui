import datetime
import hashlib
import logging
import os
import shutil

from openpyxl import Workbook, load_workbook
from pathlib import Path
import PySimpleGUI as sg

import catgui

from catgui import log_wrap

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)


@log_wrap
def create_backup(scan_file_name):
    logger.info(f"create_backup({scan_file_name})")

    wb = load_workbook(filename=scan_file_name, read_only=True, data_only=True)

    target_path = ""

    ws_summary = wb["Summary"]
    for value in ws_summary.iter_rows(min_col=1, max_col=2, values_only=True):
        print(value)
        if value[0] == "target_folder":
            target_path = Path(value[1])
            print(f"target_path {target_path}")

    if not os.path.isdir(target_path):
        return ("No target folder")

    files_copied = 0
    files_processed = 0
    ws_files = wb["Files"]
    for value in ws_files.iter_rows(min_row=2, min_col=1, max_col=6, values_only=True):
        source_file_path = Path(Path(value[0]) / Path(value[1]))
        destination_file_path = Path(target_path / Path(value[1]))
        files_processed += 1
        if os.path.exists(destination_file_path):
            filename = destination_file_path.stem
            suffix = destination_file_path.suffix  #append first 5 hash characters
            adjusted_filename = filename + '(' + value[5][0:5] +')' + suffix 
            destination_file_path = Path(target_path / adjusted_filename)
            print(f"duplicate? {destination_file_path}")
        try:
            shutil.copyfile(source_file_path, destination_file_path)
            print(f"Copy {source_file_path} to \n\t{destination_file_path}")
            files_copied += 1
        except Exception as e:
            print(e)

    return (f"Copied {files_copied} of {files_processed} files")


@log_wrap
def scan_files(scan_parameters):
    logger.info(f"archive_scan_files()")

    args = catgui.getargs()
    if args.verbose: print(f"Options: {args}")

    wb = Workbook()

    ws1 = wb.active
    ws1.title = 'Summary'

    ws1['A1']= f"Scan summary "
    for parameter_key in sorted(scan_parameters):
        if isinstance(scan_parameters[parameter_key], list):
            for item in scan_parameters[parameter_key]:
                ws1.append((parameter_key, item))
        else:
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


@log_wrap
def file_survey(scan_parameters):
    logger.info("file_survey()")

    filelist = []
    ignorelist = []
    start_path = scan_parameters['start_folder']
    for parent, dirs, files in os.walk(start_path):
        for filename in files: #row[2] is a tuple of the filenames
            full_path: Path = Path(parent / Path(filename)) # row[0] is the parent directory
            st = os.stat(full_path)
            filelist.append([
                parent, filename, st.st_size, 
                datetime.datetime.fromtimestamp(st.st_ctime), 
                datetime.datetime.fromtimestamp(st.st_mtime),
                'hash'
            ])
    
    print(f"number of files scanned = {len(filelist)}")
    excluded_count = 0
    keeplist = []
    for file_object in filelist:
        _exclude = False
        for item in scan_parameters["exclude_list"]:
            if item in file_object[0]:
                _exclude = True
        if _exclude:
            excluded_count += 1
            ignorelist.append(file_object)
        else:
            keeplist.append(file_object)
        
    print(f"number of ignored entries {len(ignorelist)}")
    print(f"number of entries retained {len(keeplist)}")

    return (keeplist, ignorelist)


@log_wrap
def save2(args, wb, scan_parameters):
    logger.info("save2()")

    header_row = ('Directory', 'Filename', 'size', 'created', 'modified', 'blake2')

    ws2 = wb.create_sheet('Files')
    ws2.append(header_row)
    ws2.auto_filter.ref = "A:F"
    ws2.freeze_panes = "B2"

    ws2d = wb.create_sheet('Dups')
    ws2d.append(header_row)
    ws2d.auto_filter.ref = "A:F"
    ws2d.freeze_panes = "B2"

    ws2i = wb.create_sheet('Ignore')
    ws2i.append(header_row)
    ws2i.auto_filter.ref = "A:F"
    ws2i.freeze_panes = "B2"

    keeplist, ignorelist = file_survey(scan_parameters)

    logger.info(f"Begin data save: keep candidates {len(keeplist)}")
    logger.info(f"Begin data save: ignore list files {len(ignorelist)}")
    for file_object in ignorelist: #save those that were ignored in the file survey
        ws2i.append(file_object)

    number_files = 0
    number_save = 0
    size_save = 0
    number_ignore = 0
    size_ignore = 0
    duplicate_count_list = {}

    DATE_FORMAT = "%Y-%m-%d"
    scan_start_time = datetime.datetime.strptime(scan_parameters['scan_start_date'], DATE_FORMAT)

# Compute the hash digest only if a filename concatenated with its file size 
# is added to the duplicate_list multiple times.
# This situation indicates the filename is a possible duplicate.
# Keep the candidate file objects and the number of possible duplications

    for file_object in keeplist:
        number_files += 1
        if scan_start_time < file_object[4]:  #keep files with scan start before modified time
            number_save += 1
            size_save += file_object[2]

            filename_size = file_object[1] + str(file_object[2])
            if filename_size in duplicate_count_list.keys():
            # try:
                duplicate_count_list[filename_size] += 1 
                full_path = Path(file_object[0]) / Path(file_object[1])
                try:
                    file_hash = hashlib.blake2b()
                    with open(full_path, "rb") as f:
                        while chunk := f.read(8192):
                            file_hash.update(chunk)
                    file_object[5] = file_hash.hexdigest()[:20]
                    ws2d.append(file_object)
                except PermissionError as e:
                    sg.popup_quick_message(f'exception {e}', 
                        'Check if a previous Excel scan file is still open.', 
                        keep_on_top=True, auto_close_duration=5,
                        background_color='yellow', text_color='black')
                    break
            # except Exception as e:
            else:
                duplicate_count_list[filename_size] = 1

            ws2.append(file_object)  # save those within the scan period
        else:
            ws2i.append(file_object)  # add the rest to ignore tab
            number_ignore += 1
            size_ignore += file_object[2]

    print(f"Total files processed {number_files}")
    print(f"  Number of modified files {number_save}")
    print(f"  Number of files ignored {number_ignore}")

    duplicates = list(duplicate_count_list.values())
    duplicate_count = 0
    for duplicate in duplicates:
        if duplicate > 1:
            duplicate_count += 1
    print(f"  Number of candidate duplicates {duplicate_count}")

    summary = {
    'total files' : number_files,
    'Modified files after scan date' : number_save, 
    'size_save' : size_save,
    'Before scan date (ignored)' : number_ignore,
    'size_ignore' : size_ignore,
    'duplicates?' : duplicate_count
    }

    return summary
