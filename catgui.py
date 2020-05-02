import argparse
import sys

import PySimpleGUI as sg

from pathlib import Path
from catguiAuxPkg import catguiMenu


def main():
    args = getargs()

    script_name = Path(sys.argv[0]).stem
    options_text = f"{script_name} options:\n  {args}"
    sg.popup(options_text, title=script_name)

    catguiMenu.menu(script_name)


def getargs():
    parser = argparse.ArgumentParser(
        description="A collection of disk file cataloging functions")
    parser.add_argument('-v', '--verbose', help='Provide detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s version 0.1')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
