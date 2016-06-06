#!/usr/bin/env python
"""sdic

A.K.A. SQL Data Integrity Checker

Asynchronous soft constraints executed against your databases.
The path to your queries and servers.ini files should be defined as an arg.
Optionally, declare a single server if you have multiple ones
in a directory, but want to only run one.

See <https://github.com/percolate/sdic> for more info

Usage:
    sdic <directory> [<server>]

Options:
    -h --help   Show this screen.
"""
from os.path import isdir
from lockfile import FileLock
import sys
import os
import fnmatch
import prettytable
import ConfigParser
import time
import syslog

from sqlalchemy import create_engine
from sqlalchemy import text

from docopt import docopt
from constants import VERSION

CONFIG_SERVERS = 'servers.ini'


def error(message):
    """Print an error message and exit the script"""
    print "Error:", message
    exit(1)


def get_query_files(directory):
    """
    Get the list of filenames of SQL files found in the specified folder

    Params: directory string
    Returns: Array
    """
    files = []

    for found_file in os.listdir(directory):
        if fnmatch.fnmatch(found_file, '*.sql'):
            files.append(found_file)

    return files


def launch_queries(directory, server):
    """
    Launch the queries found in the specified folder

    Param directory string Folder containing the SQL files
    Param server dict describing a server

    Returns: Bool value of whether we get query output or not
    """
    query_folder = os.path.join(directory, server['name'])
    files = get_query_files(query_folder)
    produced_output = False

    for filename in files:
        query_filename = os.path.join(directory, server['name'], filename)
        output = None
        with open(query_filename, 'r') as opened_file:
            query = opened_file.read()

            start_time = time.time()
            output = get_query_output(server, query)
            query_time = round(time.time() - start_time, 3)

            syslog.syslog('{} successfully ran in {} sec.'.format(filename,
                                                                  query_time))
        if output:
            produced_output = True

            # Announce that this query has results
            print "-----===== /!\ INCOMING BAD DATA /!\ =====-----"
            print
            print "Server: {}".format(server['name'])
            print "File: {}".format(filename)
            print
            # Display the raw query
            print "SQL Query:"
            print query

            # Display the results of the query
            print output
            print

    return produced_output


def get_query_output(server, query):
    """
    Launch a query and display the output in a pretty text table

    Args:
        server (dict): Server to launch the query on
        query (str): Query to launch

    Returns:
        (str) or None
    """
    db_url = server['db_url']

    # start sqlalchemy engine
    engine = create_engine(db_url)
    conn = engine.connect()
    result = conn.execute(text(query))
    rows = result.fetchall()

    table = None

    if result.rowcount > 0:
        # Get the column titles
        titles = []
        for desc in result.keys():
            titles.append(desc)
        table = prettytable.PrettyTable(titles)

        # Fill the table
        for row in rows:
            arr = []
            for item in row:
                if isinstance(item, str):
                    item = unicode(item, 'utf8', 'ignore')
                arr.append(item)

            table.add_row(arr)

    conn.close()
    result.close()

    return table


def get_servers_from_config(directory):
    """
    Get the configuration of all the servers in the config file

    param directory string Folder containing the servers.ini file
    return List of servers dictionnaries
    """
    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(directory, CONFIG_SERVERS))

    valid_config_items = ['db_url']

    servers = []
    for section in config.sections():
        server = {'name': section}
        for (item_name, item_value) in config.items(section):
            if item_name in valid_config_items:
                server[item_name] = item_value
        servers.append(server)

    return servers


def main():
    args = docopt(__doc__,
                  version="sdic {}".format(VERSION))

    # Check that the given directory exists
    if not isdir(args['<directory>']):
        error("The folder {} does not exist".format(args['<directory>']))

    # Try to get the config of the servers we are gonna use
    servers = get_servers_from_config(args['<directory>'])

    # Check that we are not already running
    program_name = os.path.basename(sys.argv[0])
    lock = FileLock("/tmp/{}.lock".format(program_name))
    if lock.is_locked():
        error("{} is already running. Delete {} if it's a mistake.".format(
            program_name, lock.path))

    # Everything's ok, run the main program
    with lock:
        syslog.openlog('sdic')

        has_output = False
        if not args['<server>']:
            for server in servers:
                if launch_queries(args['<directory>'], server):
                    has_output = True
        else:
            for server in servers:
                if server['name'] == args['<server>']:
                    if launch_queries(args['<directory>'], server):
                        has_output = True
        if has_output:
            return 1

        syslog.closelog()

if __name__ == "__main__":
    sys.exit(main())
