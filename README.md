### [Play now on Grapevine](https://grapevine.haus/games/Architext/play)
[<img alt="Click to play now" src="https://user-images.githubusercontent.com/15345234/121176454-82af3900-c85c-11eb-9798-863ac83e533a.png" height="40"/>](https://grapevine.haus/games/Architext/play)

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
* "Program" behavior into the items present in your worlds using the same commands you would use as a player.
* Share your worlds or play them privately with your friends.
* Talk and interact with other connected players.
* Export your worlds as a backup or to share them online.
* Roll dice! 🎲

As a creator, Architext allows you to take a physical place from your imagination to a reality where you can share it with anyone. It's also great to build puzzle/scape room games and to create a setting to run role playing games in.

# How to play
Architext has a tutorial that lets you learn the basics in 5 minutes. The in-game help hub will teach you everything there is to know, if you want to.

The game is played over telnet. The official server is accesible at architext-game.com port 2112.

The most convenient and recommended way to connect to the game is by using [this link to enter the Grapevine web client](https://grapevine.haus/games/Architext/play).

If you are using the [Mudlet](https://www.mudlet.org/) mud client You'll need to set the following preferences:
* Set `Server data encoding` (under `Options` -> `Preferences`) to `UTF-8` 
* Set `Command Separator` (at the `Input Line` tab) to `;;;`.

Nevertheless, you can connect to the game using any telnet client **that supports utf-8**. In Ubuntu you can connect with the command:
```
telnet architext-game.com 2112
``` 

# Demo
## A piece of the tutorial
![tutorial](https://user-images.githubusercontent.com/15345234/121041849-6a371400-c7b3-11eb-95ae-fab7eddefcaf.gif)

## Creating a cake 🎂
![craft cake](https://user-images.githubusercontent.com/15345234/121041892-74591280-c7b3-11eb-8b0d-9f215198945e.gif)


## Making the cake edible 🙆
![verb](https://user-images.githubusercontent.com/15345234/121041909-79b65d00-c7b3-11eb-8a81-bd856c59fcf3.gif)


# Running locally for development
To run Architext you need:
* Python3 and Pip to run the game
* A MongoDB database's URI

>An easy and convenient way of getting the database is signing up at [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) to get a free remote database. Once you have created your cluster click in `CONNECT`/`Connect your application` to get the dababase URI, a string like:
>```
>mongodb+srv://yourusername:<password>@yourclustername.hapiq.gcp.mongodb.net/>yourdatabasename?retryWrites=true&w=majority
>```
>You'll need to replace \<password> with your MongoDB Atlas password to get the real URI. 

Once you have Python and your MongoDB URI, just use
```
git clone https://github.com/OliverLSanz/architext
cd architext/server
pip3 install -r requirements.txt
python3 -m architext -d <YOUR_DB_URI>
```
After that you can start the server again just with
```
cd architext/server
python3 -m architext -d <YOUR_DB_URI>
```
# Set up your own production server
You can easily deploy your own Architext server using the docker-compose file provided.
## tl;dr;
Run this:
```
git clone https://github.com/OliverLSanz/architext
cd architext
docker-compose up
```
and you'll have the game accessible on the machine's 2112 port.
 ## Detailed Guide

### 1. Get a server
You need a machine to run the server on. You can use your personal computer. Just have in mind that you'll need to get a static IP and to have your 2112 port accessible from the internet.

An easier but non free option is to get a Virtual Private Server (VPS). The official Architext server is hosted on MVPS. You can get a server for 3€/month and support Architext's development using [this referal link](https://www.mvps.net/?aff=12763).

### 2. Install Docker Engine and Docker Compose
They come pre-installed in MVPS servers. To find out if your have them, log into to your server and type:
```
docker -v

> Docker version 19.03.13, build cd8016b6bc    # Your out should be similar
``` 
and
```
docker-compose -v

> docker-compose version 1.25.5, build unknown  # Your out should be similar
```

Use the following resources if they are not installed:
* [Docker official installation page](https://docs.docker.com/engine/install/)
* [Docker Compose official instalation page](https://docs.docker.com/compose/install/)

### 3. Clone the repo from the server
```
git clone https://github.com/OliverLSanz/architext
cd architext
```
### 4. Edit the config.yml file (optional)
```
nano server/config.yml
```
There you can change: 
* The server language (between en_US and es_ES). 
* The per-player public world limit.
* The messages sent to players when they connect, log-in and sign-in.

### 5. Start the server
```
docker-compose up
```
or
```
docker-compose up -d
```
to detach your terminal from the output. The game will then be available at port 2112.
## Updating the server version
You can make your own changes to the game or fetch the official updates using
```
cd architext
git pull
```
Then you need to stop the server and use `docker-compose up` with the `--buid` option so that the code changes take effect.
```
docker-compose up --build
```
Also do this whenever you update the config.yml file.
