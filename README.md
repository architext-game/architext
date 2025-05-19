> This readme is outdated, sorry.  So many things, so little time .-.

### [Play now on architext-game.com](https://architext-game.com)

![architext cover v3](https://user-images.githubusercontent.com/15345234/122195601-ccb8a000-ce96-11eb-8456-21168ee35278.png)

# Table of contents
- [Overwiew](#overwiew)
- [How to play](#how-to-play)
- [Demo](#demo)
- [Running locally for development](#running-locally-for-development)
- [Set up your own production server](#set-up-your-own-production-server)
- [Applying changes to config.yml or code](#updating-the-server-version)
# Overwiew
**Architext** is a multiplayer *virtual reality* text game that allows you to explore **and create** worlds entirely made of words (pun intended). And because of the huge expressive power of words, there is no limit to what you can find or build.

## Features
* Enter and explore worlds made by other players.
* Freely build your own worlds using a simple set of commands.
* WIP - "Program" behavior into the items present in your worlds using the same commands you would use as a player.
* Share your worlds or play them privately with your friends.
* Talk and interact with other connected players.
* Export your worlds as a backup or to share them online.
* WIP - Roll dice! 🎲

As a creator, Architext allows you to take a physical place from your imagination to a reality where you can share it with anyone. It's also great to build puzzle/scape room games and to create a setting to run role playing games in.

# How to play

Get into http://architext-game.com and play the five minute turorial!


# Running locally for development

## DB

Run the postgres database from the docker-compose file
You can also give the server the USE_MEMORY_DB env var to use an in-memory database.


## Server

```
cd server/
python3.12.8 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m architext.entrypoints.socketio.server
```

## Web

```
cd web/
npm install
npm run dev
```

# Migrations

DB migratios are done using [alembic](https://alembic.sqlalchemy.org/en/latest/).

To set up alembic I have run the following command:

```
cd server
pip install alembic
alembic init alembic
```

Alembic needs access to the running DB as well as the current SQLAlchemy models.
Currently the `alembic/env.py` file is configured to use the `DB_URL` configuration variable.

```
from architext.entrypoints.socketio.settings import DB_URL
config.set_main_option('sqlalchemy.url', DB_URL) 
```

The metadata is also imported in the `alembic/env.py` file.

```
from architext.core.adapters.sqlalchemy.config import metadata
target_metadata = metadata
```

To run migrations, run the following command:

```
alembic upgrade head
```

This will run all the migrations that have not been run yet.

To generate a new migration, run the following command:

```
alembic revision --autogenerate
```

Alembic should be installed in the venv. Currently it is included as a dependency
in the `requirements.txt` file.
