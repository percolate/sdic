# sdic

A.K.A. __SQL Data Integrity Checker__

[![CircleCI](https://circleci.com/gh/percolate/sdic.svg?style=svg)](https://circleci.com/gh/percolate/sdic)
[![codecov](https://codecov.io/gh/percolate/sdic/branch/master/graph/badge.svg)](https://codecov.io/gh/percolate/sdic)

## One line purpose

`sdic` executes all the SQL queries found in a folder and displays its output.

## More detailed purpose

In any RDBMS, you can set constraints to prevent the application to save the
data in a way that's not consistent. E.g. if you want all your users to have an
email, you can set the email column to `NOT NULL`.

This works for simple constraints:

1. It's easy to implement
1. It's cheap for the database to check on every change

But for more complex constraints that you'd like to set, it'd be either very
expensinve to check on every write, or even impossible to write as a
constraint.

With `sdic`, you can write you complex constraints as simple queries, and have
the database run them asynchronously at the occurence you want.

We call them "soft constraints".

## Example

Let's say that you have a `users` table, defined like this:

- `id` Primary Key `NOT NULL`
- `firstname` `NULL`
- `lastname` `NULL`
- `email` `NOT NULL`

Now, let's suppose your application allow users to register just with their
`email` but can fill in they `firstname` and `lastname` later on, but we don't
want our users to have only a firstname or a lastname.

Simply put, our constraint is: Make sure every users has either a `firstname`
and a `lastname` set, or both set to NULL.

With `sdic`, you can add this `enforce_fullname.sql` file and let `sdic` check
that every user comply nightly.

```sql
-- Make sure every user with a name has both a firstname and a lastname
SELECT id, firstname, lastname
FROM users
WHERE
    (firstname IS NULL AND lastname IS NOT NULL) OR
    (firstname IS NOT NULL AND lastname IS NULL)
LIMIT 10
;
```

Put this file in `your-environment/your-server/enforce_fullname.sql`.

Edit the `your-environment/servers.ini` file to tell sdic how to connect to
your server.

Now run `sdic your-environment` and it will output any user that do no comply
with your soft constraint.

You can have as many soft constraints on as many servers and as many
environments as you need.

## Install as a cron

If you want to get an email every night to give you a list of all the soft
constraints that have been broken during the last day, just add it to you
crontab. We like to have it run daily, so we can fix any bug generating bad
data before it becomes a real problem.

Example crontab:

```
MAILTO="dba@acme.com"
@daily sdic live
```

`dba@acme.com` is the email that will get the soft constraints broken every
day. Make sure your local MTA is well configured on your system. You can test
it by doing `date | mail -s test dba@acme.com`.

## Databases supported

Any database supported by [SQLAlchemy](http://www.sqlalchemy.org/) should be
supported, including [PostgreSQL](https://www.postgresql.org/) and
[MySQL](https://www.mysql.com/).

## Install

`pip install sdic`

## Configuration

An example configuration is given in the `example-environment` folder.

The script reads from a designated folder, whose path you pass as an argument.
This folder should consist of the following:

1. A `servers.ini` file, which contains the Database URLs (see the
    `example-environment` folder)
1. A sub-folder, which contains the actual queries in a `.sql` file format

## Usage

A `directory` argument is mandatory:

`sdic path/to/your/folder`

If you have e.g more than one server in a folder, but you want to
only run one of them, an optional `server` argument can be passed as well:

`sdic path/to/your/folder server1`

If a query produces an output, it will look something like this:

```
-----===== /!\ INCOMING BAD DATA /!\ =====-----

Server: big-database
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
