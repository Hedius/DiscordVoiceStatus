# E4GL DiscordVoiceStatus
This app uses nextcord to recreate the Discord Widget JSON with member IDs.
Discord has removed the IDs from the widget. However, certain applications
depend on the member IDs in the widget.

## Why?
I operate multiple BF4 servers. Our backend grants discord members
a balancing whitelist while they are in voice channels.
The member ID is needed to have 100% correct matches 24/7.

## Features
* The bot supports multiple discord servers.
* Just invite the bot to
  * You can also ask me for help. I run a public instance and can serve data for you.
  *   Discord: Hedius#0001
* The JSON is served by a flask app on port 8080.

## Retrieving Data
The bot needs full access to the voice channels of your server!

```
/<server_id>/
/api/servers/<server_id>/widget.json
/?id=<server_id>

Examples:
/1234/
/api/servers/1234/widget.json
/?id=1234
```

If you use AdKats for your BF4 servers. AdKats has a hardcoded widget url.
My custom fork implements an option for modifying the discord API URL:
[E4GLAdKats](https://github.com/Hedius/E4GLAdKats)

## Installation
### docker-compose
 1. clone the repository
 2. adjust docker-compose.yml
 3. sudo docker-compose up -d

## Updating
### docker-compose
 1. sudo docker-compose down --rmi all
 2. git pull
 3. sudo docker-compose up -d

# LICENSE
GPLv3

Written by Hedius git@hedius.eu, 2021