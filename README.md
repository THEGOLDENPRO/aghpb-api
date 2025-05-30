<div align="center">

  # 📚 AGHPB API

  <sub>Behold the **anime girls holding programming books** API!</sub>

  [![Docker Badge](https://img.shields.io/docker/v/devgoldy/aghpb_api?label=docker)](https://hub.docker.com/r/devgoldy/aghpb_api "We're on docker!")

</div>

This is an API I made for the anime girls holding programming books [github repo](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books) because I was bored.
It's a rewrite of the [old API](https://github.com/THEGOLDENPRO/aghpb_api_legacy) but written in Python using the [Fast API](https://github.com/tiangolo/fastapi) library instead.
It scrapes a local copy of the repo and thanks to that I was able to implement headers like ``Book-Date-Added`` (returns the date and time a book was added).

<img src="./assets/screenshot_1.png" width="600px">

> oh yeah also check out our 🌟 cousin API **(anime girls and computers)**: https://github.com/r3tr0ananas/agac-api

## 🌐 Publicly available instances
Pick the closest instance to you for FASTER ANIME GIRLS!

| Country | URL | Hosted by | Notes |
|:-----------:|-------|:-------------:|:---------:|
| 🇬🇧 | [``https://api.devgoldy.xyz/aghpb/v1``](https://api.devgoldy.xyz/aghpb/v1) | [me](https://github.com/THEGOLDENPRO) | ⭐ Official Instance |
| 🇩🇪 | [``https://aghpb.teaishealthy.me``](https://aghpb.teaishealthy.me) | [teaishealthy](https://github.com/teaishealthy) |
| 🇩🇪 | [``https://api.ananas.moe/aghpb/v1``](https://api.ananas.moe/aghpb/v1) | [Ananas](https://github.com/r3tr0ananas) | 🛠️ 🗣️ GERMAN ENGINEERING!!! |
| 🇸🇪 | [``https://aghpb.zeeraa.net``](https://aghpb.zeeraa.net) | [Zeeraa](https://github.com/AntonUden) |
| 🇺🇸 | [`https://api.emmatech.dev/aghpb`](https://api.emmatech.dev/aghpb) | [EmmmaTech](https://github.com/EmmmaTech) | 🇺🇸 🦅 FREEDOMMMMMMMM!!! |

> Also do use these instances as backups incase my servers at https://api.devgoldy.xyz go down.

## 💫 API Wrappers
I was also even more bored so I decided to write an API wrapper in every mfing language I can possible, including those I've never really written in.

These are the languages I've written so far:
- **🦀 Rust - [``aghpb.rs``](https://github.com/THEGOLDENPRO/aghpb.rs)** (async)
- **🟦 TypeScript - [``aghpb.ts``](https://github.com/THEGOLDENPRO/aghpb.ts)** (async)
- **⚫ C - [``aghpb.c``](https://github.com/THEGOLDENPRO/aghpb.c)** ~~(might blow up)~~
- **🔥 Mojo - ``Soon™``**
- **🔵 Go - ``Soon™``**
- **🌕 Lua - [``aghpb.lua``](https://github.com/THEGOLDENPRO/aghpb.lua)**

Then here are some community-made api wrappers **( thanks 💛 )**:
- **☕ Java - [``AGHPB4J``](https://github.com/JoshiCodes/AGHPB4J)**

## 🛠️ Wanna self-host?
If you would like to host your own instance of the aghpb API continue reading.

### 🐬 Docker Method (recommended)
> [!Warning]
> The docker image currently only supports **x86** architecture so if you are running anything else you may need to build the image yourself. For instructions on how to do that check out [here](#%EF%B8%8F-building-your-own-docker-image).

The easiest method to host an instance is via our [docker image](https://hub.docker.com/r/devgoldy/aghpb_api/tags). From now on in this section, I'm gonna assume you've had experience with [Docker](https://www.docker.com/) and you can at least complete the [hello world tutorial](https://docker-curriculum.com/#getting-started).

Spinning up an aghpb API container in docker is pretty simple:

1. First pull that mf
```sh
docker pull devgoldy/aghpb_api:latest
```
2. Then launch a container with this command. ``-p`` binds the api to your localhost port 8000.
```sh
docker run -p 127.0.0.1:8000:8000/tcp devgoldy/aghpb_api:latest
```
3. Now visit ``localhost:8000`` in your browser and there you go! 👍
> *if you want to host via docker-compose, [this file](https://github.com/THEGOLDENPRO/aghpb_api/blob/main/docker-compose.yml) might be useful to you*

### ⚗️ Building your own docker image.
To build your own docker image it is necessary you follow the [native method's](#-native-method-recommended-for-development) steps, but only up to **step number 3** is necessary.

Once that is done run the command below:
```sh
make docker-build
```
> ``docker images`` should display the "devgoldy/aghpb_api" image.

Now you may jump to **step 2** of the [docker method](#-docker-method-recommended).

### 🐍 Native Method (recommended for development)

#### Prerequisites:
- [Git](https://git-scm.com/downloads)
- [Python](https://www.python.org/downloads/) (3.10 - 3.13)
- [Make](https://www.gnu.org/software/make/#download) ***(otherwise you'll have to copy the commands from the [Makefile](https://github.com/THEGOLDENPRO/aghpb_api/blob/main/Makefile))***

1. Clone the repo.
```sh
git clone https://github.com/THEGOLDENPRO/aghpb_api && cd aghpb_api
```
2. Create env.
```sh
python -m venv env
source env/bin/activate # For windows it's --> cd env/Scripts && activate && cd ../../
```
3. Install the API's dependencies.
```sh
pip install . -U
```
4. Pull the ~~anime girls~~ programming books.
```sh
make pull-repo
```
5. Run that mf.
```sh
fastapi dev api/main.py
```
6. Visit ``localhost:8000`` in your browser, then all should be good! 🌈
