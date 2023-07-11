import os
import random
import dataclasses

from anime_girls import Book

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

__version__ = 1.0

API_V1 = "/v1"

app = FastAPI(
    title = "AGHPB API",
    description = "Behold the **anime girls holding programming books** API. ✴️ \n\n" \
    "This is an open api I made for the anime girls holding programming books " \
    "[github repo](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books) because I was bored.",
    license_info = {
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    version = f"v{__version__}"
)
app.mount("/cdn", StaticFiles(directory="./assets"), name="cdn")

@app.get(
    "/",
    name = "Documentation"
)
async def root():
    """Redirects you to this documentation page."""
    return RedirectResponse(url="/docs")


@app.get(
    API_V1 + "/random",
    name = "Random Book"
)
async def v1_random():
    """Returns a random book."""
    random_category = random.choice(
        [x for x in os.listdir("./assets/git_repo") if os.path.isdir(f"./assets/git_repo/{x}")]
    )
    random_book = random.choice(
        [x for x in os.listdir(f"./assets/git_repo/{random_category}") if not x == ".DS_Store"]
    )

    book = Book(
        f"./assets/git_repo/{random_category}/{random_book}"
    )

    return book.to_dict()