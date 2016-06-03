"""sql-data-integrity-checker

Asynchronous soft constraints executed against you databases.

Usage:
    sql-data-integrity-checker

Options:
    -h --help   Show this screen.
"""
from docopt import docopt
from constants import VERSION


def main():
    docopt(__doc__, version="sql-data-integrity-checker {}".format(VERSION))


if __name__ == "__main__":
    main()
