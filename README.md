<div align="center">

  # 📚 AGHPB API

  <sub>Behold the **anime girls holding programming books** API!</sub>

</div>

This is an API I made for the anime girls holding programming books [github repo](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books) because I was bored.
It's a rewrite of the [old API](https://github.com/THEGOLDENPRO/aghpb_api) but written in Python using the [Fast API](https://github.com/tiangolo/fastapi) library instead.
It scraps a local copy of the repo and thanks to that I was able to implement the ``Book-Date-Added`` header so we know exactly when a book was added.

<img src="./assets/screenshot_1.png" width="600px">

> ### You can catch the api at https://api.devgoldy.xyz/aghpb/v1
> *(When it's up of course)* 🫠

## 💫 API Wrappers
I was also even more bored so I decided to write an API wrapper in every mfing language I can possible, including those I've never really written in.

These are the languages I've written so far:
- **🦀 Rust - [``aghpb.rs``](https://github.com/THEGOLDENPRO/aghpb.rs)**
- **🟦 TypeScript - [``aghpb.ts``](https://github.com/THEGOLDENPRO/aghpb.ts)**
- **⚫ C - [``aghpb.c``](https://github.com/THEGOLDENPRO/aghpb.c)**
- **🔥 Mojo - ``Soon™``**
- **🔵 Go - ``Soon™``**
- **🌕 Lua - [``aghpb.lua``](https://github.com/THEGOLDENPRO/aghpb.lua)** (not async)
- ~~**☕ Java** - ``Soon™``~~ *"fuck you java (maven included)"*

<br>

If you are cloning this repo to run it for yourself you'll probably want to pull the submodule too.
```sh
git submodule update --init --recursive
```
> It pulls down the anime girls holding programming books [github repo](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books).
