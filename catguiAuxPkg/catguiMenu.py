from pathlib import Path
import sys

import PySimpleGUI as sg


def menu(args):
    print("Menu entry point")
    
    sg.ChangeLookAndFeel('LightGreen')
    sg.SetOptions(element_padding=(0, 0))

    # ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit'  ]],
                ['Scan', ['Since...', 'Archive flag', ['Reset', 'Not reset']], ],
                ['Help', 'About...'], ]

    # ------ GUI Defintion ------ #
    layout = [
        [sg.Menu(menu_def, )],
        [sg.Output(size=(60, 20))] ]

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
            options_text = f"{script_name} options:\n  {args}"
            sg.popup(options_text, title=script_name)
        elif event == 'Open':
            filename = sg.popup_get_file('file to open', no_window=True)
            print(filename)