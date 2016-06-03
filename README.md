# sql-data-integrity-checker

[![CircleCI](https://circleci.com/gh/percolate/sql-data-integrity-checker.svg?style=svg)](https://circleci.com/gh/percolate/sql-data-integrity-checker)
[![codecov](https://codecov.io/gh/percolate/sql-data-integrity-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/percolate/sql-data-integrity-checker)

Asynchronous soft constraints executed against you databases.
Queries that are intended to be ran here should produce `bad data`,
or data that should not be in the table that is the object of the query.

## Install

`pip install sql-data-integrity-checker`

## Configuration

The script reads from a designated folder, whose path you pass as an argument.
This folder should consist of the following:

1. A `servers.ini` file, which contains the Database URL/s (see`examples` folder)

1. A sub-folder, which contains the actual queries in a `.sql` file format

## Usage

A `directory` argument is mandatory:

`sql-data-integrity-checker path/to/your/folder`

If you have e.g more than one server in a folder, but you want to
only run one of them, an optional `server` argument can be passed as well:

`sql-data-integrity-checker path/to/your/folder server1`

If a query produces an output, it will look something like this:

```bash
-----===== /!\ INCOMING BAD DATA /!\ =====-----

Server: circleci
File: test_query.sql

SQL Query:
-- This is a query that returns current time.
Select now();

+---------------------+
|        now()        |
+---------------------+
| 2016-06-03 19:27:14 |
+---------------------+
```
