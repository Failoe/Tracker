# Tracker
Tracker is a discord bot that will log all chat messages to a database. Currently only [PostgreSQL](https://www.postgresql.org/) is the only supported database. Fortunately, it is free and easy to install.

## Using Tracker
Install Python 3.6+, the requirements.txt modules, and PostgreSQL. Run Script. Currently, the script will only log messages the first time you fire it and will have to be manually canceled and brought back online to grab new messages.

### tracker.config file
In order to function Tracker requires a config file. This file contains 3 mandatory sections and one optional section.

#### Discord Token (Mandatory)
This is the user token that Tracker uses to connect to Discord.

**Example:**
```
[Discord Auth]
token = token.goes.here
```

#### PosgreSQL Connection Information (Mandatory)
This is the information Tracker needs in order to connect to your PostgreSQL database.

**Example:**
```
[PostgreSQL]
database = tracker_db
user = tracker_user
password = track_4ll_th3_th1ngs!
host = 192.168.0.1
port = 5432
```

#### Whitelist (Mandatory)
The whitelist needs to contain the name of the guild that is being tracked.  If just the guild is specified all channels will be tracked.  To whitelist only specific channels for a guild put those channels indented under the guild.  In the below example, all channels for "Tracker guild" would be logged but only the three specified channels on "Other guild" will be logged.

**Example:**
```
[Whitelist]
Tracker guild:
Other guild:
	specific-channel-to-whitelist
	another-one
	third-one-is-the-charm
```

#### Blacklist (Optional)
Sometimes you may want to log all channels on a guild except a specific few (such as admin channels).  You can do this by whitelisting the whole guild in the whitelist section then specifying the guild and channels to not log.

**Example**
```
[Blacklist]
Tracker guild:
	bot-log
	bot-debug
	admin-hidey-hole
	keep-out-peasants
```


## Improvements I am working on

* Build database tables on initial boot
* Automatically log new messages
* Requery discord for edits/reactions and update the database
* Create User table to track user name/role changes
* Create emoji/reactions/embeds tables
* Web interface or discord output with charts of the data
* Clean up initial database building output