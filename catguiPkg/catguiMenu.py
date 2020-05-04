import datetime
import logging
from pathlib import Path
import sys
import typing

import PySimpleGUI as sg

RESET_ARCHIVE_FLAG = 'reset archive flag'
SCAN_START_DATE = 'scan start date'
scan_parameters: typing.Dict[str, str] = {}

LOGGER_NAME = "catgui"
logger = logging.getLogger(LOGGER_NAME)

def update_scan_parameters(window, key, value):
    logger.info("update_scan_parameters()")
    
    scan_parameters[key] = value
    if window: 
        print(value)
        window['status'](f"Parameters: {scan_parameters}")

def menu(author, version, args):
    logger.info("menu()")

    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit'  ]],
                ['Scan', ['Since...', 'Archive flag', ['Reset', 'No change'], 'Scan'], ],
                ['Help', 'About...'], ]

    # ------ GUI Defintion ------ #
    scan_parameters = {}
    update_scan_parameters(None, RESET_ARCHIVE_FLAG, True)
    
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Output(size=(60, 20))],
        [sg.Text(f"Parameters: {scan_parameters}", key='status', size=(60,1))] ]

    script_name = Path(sys.argv[0]).stem
    window = sg.Window(script_name, layout, default_element_size=(12, 1), 
        auto_size_text=False, auto_size_buttons=False, 
        default_button_element_size=(12, 1))

    # ------ Loop & Process button menu choices ------ #
    while True:
        event, values = window.read()
        if event == None or event == 'Exit':
            break
        print('Button = ', event)
        # ------ Process menu choices ------ #
        if event == 'About...':
            about_text = f"{script_name} v{version} (c) 2020\nAuthor: {author}\nOptions:" \
                f"\n  {args}"
            sg.popup(about_text, title=script_name)
        elif event == 'Open':
            folder_name = sg.popup_get_folder('Starting folder', no_window=True)
            print(folder_name)
        elif event == 'Reset':
            update_scan_parameters(window, RESET_ARCHIVE_FLAG, True)
        elif event == 'No change':
            update_scan_parameters(window, RESET_ARCHIVE_FLAG, False)
        elif event == 'Since...':
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
            update_scan_parameters(window, SCAN_START_DATE, date)

    window.close()
