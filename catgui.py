author = __author__ = 'Brent V. Bingham'
version = __version__ = '0.1'
import argparse

from catguiAuxPkg import catguiMenu


def main():
    args = getargs()

    catguiMenu.menu(author, version, args)


def getargs():
    parser = argparse.ArgumentParser(
        description="A collection of disk file cataloging functions")
    parser.add_argument('-v', '--verbose', default=False,
        help='Provide detailed information')
    parser.add_argument('--version', action='version', version='%(prog)s {version}')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
