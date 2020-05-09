import datetime
import logging
from pathlib import Path
import sys
import typing

import PySimpleGUI as sg
import catgui
from catguiPkg import catguiArchiveFiles

RESET_ARCHIVE_FLAG = 'reset_archive_flag'
SCAN_START_DATE = 'scan_start_date'
START_FOLDER_NAME = 'start_folder'
TARGET_FOLDER_NAME = 'target_folder'
scan_parameters: typing.Dict[str, str] = {}

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)

def update_scan_parameters(window, key, value):
    logger.info(f"update_scan_parameters({key}:{value})")
    args = catgui.getargs()
    
    scan_parameters[key] = value
    if window: 
        window['status'](f"New parameter: {key}:{value}")
        if args.verbose: print_scan_parameters()

def print_scan_parameters():
    print(f"Current parameters list: ")
    for parameter_key in sorted(scan_parameters):
        print(f"\t{parameter_key}:{scan_parameters[parameter_key]}")


def menu(author, version):
    logger.info("menu()")
    args = catgui.getargs()
    
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['File', 
                    ['Open', 'Save', 'Exit'  ]
                ],
                ['Scan', 
                    ['Folders', ['Start folder', 'Target folder'],
                    'Since...', 
                    'Archive flag', ['Reset', 'No change'], 
                    'Start scan'
                    ], 
                ],
                ['Help', 'About...'], 
                ]

    # ------ GUI Defintion ------ #
    update_scan_parameters(None, RESET_ARCHIVE_FLAG, True)
    
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Output(size=(60, 20))],
        [sg.Text(f"Options: {args}", key='status', size=(60,1))] ]

    script_name = Path(sys.argv[0]).stem
    window = sg.Window(script_name, layout, default_element_size=(12, 1), 
        auto_size_text=False, auto_size_buttons=False, 
        default_button_element_size=(12, 1))

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == None or event == 'Exit':
            break
        if args.verbose: print('Menu item = ', event)
        # ------ Process menu choices ------ #
        if event == 'About...':
            about_text = f"{script_name} v{version} (c) 2020\nAuthor: {author}\nOptions:" \
                f"\n  {args}"
            sg.popup(about_text, title=script_name)
        elif event == 'Start folder':
            folder_name = sg.popup_get_folder('Starting folder', no_window=True)
            update_scan_parameters(window, START_FOLDER_NAME, folder_name)
        elif event == 'Target folder':
            folder_name = sg.popup_get_folder('Backup folder', no_window=True)
            update_scan_parameters(window, TARGET_FOLDER_NAME, folder_name)
        elif event == 'Reset':
            update_scan_parameters(window, RESET_ARCHIVE_FLAG, True)
        elif event == 'No change':
            update_scan_parameters(window, RESET_ARCHIVE_FLAG, False)
        elif event == 'Since...':
            date = get_scan_date()
            update_scan_parameters(window, SCAN_START_DATE, date)
        elif event == 'Start scan':
            start_scan(window)
 
    logger.info("exit menu()")
    window.close()


def get_scan_date():
    logger.info("get_scan_date()")
    date30 = datetime.datetime.today() - datetime.timedelta(days=30)
    date = date30.strftime("%Y-%m-%d")
    layout = [[sg.In(date, size=(20,1), key='input')],
            [sg.CalendarButton('Choose Date', target='input', key='date', 
                default_date_m_d_y=(date30.month, date30.day, date30.year),
                button_color=('black','lightblue'), 
                tooltip='Default is 30 days prior to today.')],
            [sg.Ok(key='Ok')]]

    calendar_window = sg.Window('Calendar', grab_anywhere=False, ).Layout(layout)
    calendar_event,calendar_values = calendar_window.Read()
    if calendar_event == 'Ok':
        date = calendar_values['input'][:10]
        calendar_window.close()
    
    return date

def start_scan(window):
    logger.info("start_scan()")
    _scan = True
    if SCAN_START_DATE not in scan_parameters:
        print(f"\tMissing '{SCAN_START_DATE}'")
        _scan = False
    if START_FOLDER_NAME not in scan_parameters:
        print(f"\tMissing '{START_FOLDER_NAME}'")
        _scan = False
    if TARGET_FOLDER_NAME not in scan_parameters:
        print(f"\tMissing '{TARGET_FOLDER_NAME}'")
        _scan = False

    # run the scan if all required scan parameters are available
    if _scan:
        print("Start scan for archived files")
        catguiArchiveFiles.scan_files(window, scan_parameters)
    else:
        print("Missing one or more scan parameters.")
        print_scan_parameters()
