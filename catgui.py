import argparse

from catguiAuxPkg import catguiMenu


def main():
    args = getargs()

    catguiMenu.menu(args)


def getargs():
    parser = argparse.ArgumentParser(
        description="A collection of disk file cataloging functions")
    parser.add_argument('-v', '--verbose', help='Provide detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s version 0.1')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
