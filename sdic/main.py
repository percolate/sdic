#!/usr/bin/env python
"""sdic

A.K.A. SQL Data Integrity Checker

Asynchronous soft constraints executed against your databases.
The path to your queries and servers.ini files should be defined as an arg.
Optionally, declare a single server if you have multiple ones
in a directory, but want to only run one.

See <https://github.com/percolate/sdic> for more info

Usage:
    sdic [options] <directory> [<server> [--server_url=<url>]] [<query>]

Options:
    -h --help   Show this screen.
    --output_location=<syslog|stdout>  Where to send output [default: stdout]
    --server_url=<url>                 Optionally pass the db_url for the server.

"""
import sys
import fnmatch
import logging
from os import walk
from os import path
import time

import ConfigParser
from lockfile import FileLock
import prettytable

from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError

from docopt import docopt
#from constants import VERSION
VERSION = 1

CONFIG_SERVERS = "servers.ini"

log = logging.getLogger("sdic")


def format_query_result(result):
    """
    Launch a query and display the output in a pretty text table

    Args:
        server (dict): Server to launch the query on
        query (str): Query to launch

    Returns:
        (str) or None
    """
    table = None

    if result.rowcount > 0:
        # Get the column titles
        titles = result.keys()

        try:
            table = prettytable.PrettyTable(titles)
        except Exception as e:
            # PrettyTable raises a generic Exception error for duplicate field names
            # Duplicate field names are likely caused by the query.
            log.exception("PrettyTable crashed while trying to format row names.", e)
            return None

        # Fill the table
        for row in rows:
            arr = []
            for item in row:
                if isinstance(item, str):
                    item = unicode(item, "utf8", "ignore")
                arr.append(item)

            table.add_row(arr)

    return table


def get_connections_from_config(
    directory, server=None, server_url=None, output="stdout"
):
    """
    Returns a function for running queries on each database server. Establishes a
    connection to each server as needed.

    Args:
        directory (str): Folder containing the servers.ini file and queries.
        server (str, optional): Database server name, should also be folder in
            directory. Defaults to None.
        server_url (str, optional): Database server URL. Defaults to None.
        output (str, optional): Where to redirect output, only options are "stdout" and
            "syslog". Defaults to "stdout."
    Returns:
        function: Will run a query on a corresponding server.
    """
    assert path.exists(directory), "The folder {} does not exist".format(directory)

    # TODO determine if this is necessary
    assert output in ("stdout", "syslog"), "Invalid value for --output_location"

    servers = {}
    print servers

    if server_url:
        engine = create_engine(db_url)
        servers[server] = engine.connect()
    else:
        config = ConfigParser.RawConfigParser()
        config.read(path.join(directory, CONFIG_SERVERS))

        valid_config_items = ["db_url"]

        for server_name in config.sections():
            print servers
            if not server or (server_name == server):
                for (item_name, item_value) in config.items(server_name):
                    print item_name
                    print item_value

                    if item_name == "db_url":
                        engine = create_engine(item_value)
                        servers[server_name] = engine.connect()
                        print "done"

    assert servers, "Could not find any server URLs in the server.ini or --server_url."

    def launch_query(server_name, query_filename):
        """
        Run query on specific server.

        Args:
            server_name (str): database server name.
            query_filename (str): name of the file for running queries.
        """
        query_log = logging.getLogger(
            "sdic.{}".format(path.splitext(query_filename))
        )
        print server, query_filename
        query_full_path = path.join(directory, server_name, query_filename)
        output = None

        with open(query_full_path, "r") as opened_file:
            query = opened_file.read()

            start_time = time.time()

            try:
                print "inside try"
                result = servers[server_name].execute(query)
                rows = result.fetchall()
            except DBAPIError as e:
                query_log.exception(
                    "The following SQL query got interrupted: {}".format(query)
                )
                return

            query_time = round(time.time() - start_time, 3)

            query_log.info(
                "{} successfully ran in {} sec.".format(query_filename, query_time)
            )

            output = format_query_result(result)

        if output:
            # Announce that this query has results
            if output is "syslog":
                query_log.error(output)
            elif output is "stdout":
                print(
                    "-----===== /!\ INCOMING BAD DATA /!\ =====-----",
                    "\n",
                    "Server: {}".format(server_name),
                    "File: {}".format(filename),
                    "\n",
                    "SQL Query:\n{}".format(query),
                    output,
                )
    return launch_query


def main():
    args = docopt(__doc__, version="sdic {}".format(VERSION))

    # 1 if directory, then run on each file in the directory
    # create a closure here
    launch_query = get_connections_from_config(
        args["<directory>"], server=args["<server>"], server_url=args["--server_url"]
    )
    program_name = path.basename(sys.argv[0])

    # Check that we are not already running
    lock = FileLock("/tmp/{}.lock".format(program_name))
    if lock.is_locked():
        raise RuntimeError(
            "{} is already running. Delete {} if it's a mistake.".format(
                program_name, lock.path
            )
        )

    # Everything's ok, run the main program
    with lock:
        # Try to get the config of the servers we are gonna use
        if args["<query>"]:
            # TODO
            print "query"
            launch_query(args["<server>"], args["<query>"])
        else:
            for root_dir, dirs, files in walk(args["<directory>"]):
                server_name = path.basename(path.normpath(root_dir))
                print root_dir
                print server_name
                if not args["<server>"] or (args["<server>"] == server_name):
                    for found_file in files:
                        if fnmatch.fnmatch(found_file, "*.sql"):
                            launch_query(server_name, found_file)


if __name__ == "__main__":
    sys.exit(main())
