# Tracker
Tracker is a discord bot that will log all chat messages to a database. Currently only [PostgreSQL](https://www.postgresql.org/) is supported.

### Config Files
In order to connect to your database Tracker requires a "db.config" file the PostgreSQL database with the following structure:

```
[db]
database = DB Name
user = username
password = password
host = ip/hostname
port = port (5432 is default)
```