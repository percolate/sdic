# sql-data-integrity-checker

[![CircleCI](https://circleci.com/gh/percolate/sql-data-integrity-checker.svg?style=svg)](https://circleci.com/gh/percolate/sql-data-integrity-checker)
[![codecov](https://codecov.io/gh/percolate/sql-data-integrity-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/percolate/sql-data-integrity-checker)

Asynchronous soft constraints executed against you databases.
Queries that are intended to be ran here should produce `bad data`,
or data that should not be in the table that is the object of the query.

## Install

`pip install sql-data-integrity-checker`

## Configuration

This script reads from a folder whose path you pass in as an argument.
This folder needs to be consisted of:

1. A `servers.ini` file, which contains the Database URL/s (see`examples` folder)

2. A sub-folder, which contains the actual queries in a `.sql` file format.

## Usage

A `directory` argument is mandatory:
`sql-data-integrity-checker path/to/your/folder`

If you have e.g more than one server in a folder, but you want to
only run one of them, an optional `server` argument can be passed as well:

`sql-data-integrity-checker path/to/your/folder server1`
