from __future__ import annotations
from typing import List

import os
from errors import APIError
from anime_girls import AGHPB, CategoryNotFound

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

__version__ = 1.0

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH"))

TAGS_METADATA = [
    {
        "name": "books",
        "description": "The main endpoints that allow you to get books." \
            "\n\n**All books come with extra info via headers like: ``Book-Name``, ``Book-Category``, ``Book-Date-Added``**",
    }
]

app = FastAPI(
    title = "AGHPB API",
    description = "Behold the **anime girls holding programming books** API. ✴️ \n\n" \
    "This is an open api I made for the anime girls holding programming books " \
    "[github repo](https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books) because I was bored.",
    license_info = {
        "name": "Apache 2.0",
        "identifier": "MIT",
    },
    openapi_tags = TAGS_METADATA,
    version = f"v{__version__}",

    root_path = ROOT_PATH
)


aghpb = AGHPB()

@app.get(
    "/random",
    name = "Random Book",
    tags = ["books"],
    response_class = FileResponse,
    responses = {
        200: {
            "content": {
                "image/png": {},
                "image/jpeg": {}
            },
            "description": "Returned an anime girl holding a programming book successfully. 😁",
        },
        404: {
            "model": APIError, 
            "description": "The category was not Found."
        },
        422: {"content": None, "description": "This is not returned!"}
    },
)
async def random(category: str = None) -> FileResponse:
    """Returns a random book."""
    if category is None:
        category = aghpb.random_category()

    try:
        book = aghpb.random_book(category)
    except CategoryNotFound as e:
        return JSONResponse(
            status_code = 404, 
            content = {
                "error": e.__class__.__name__,
                "message": e.msg
            }
        )

    return FileResponse(
        book.path,
        headers = {
            "Book-Name": book.name,
            "Book-Category": book.category,
            "Book-Date-Added": str(book.date_added),
            "Last-Modified": str(book.date_added),

            "Pragma": "no-cache",
            "Expires": "0",
            "Cache-Control": "no-cache, no-store, must-revalidate, public, max-age=0"
        }
    )

@app.get(
    "/categories",
    name = "All Available Categories",
    tags = ["books"]
)
async def categories() -> List[str]:
    """Returns a list of all available categories."""
    return aghpb.categories_list