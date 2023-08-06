from __future__ import annotations
from typing import List

import os
import errors
from dataclasses import asdict
from anime_girls import AGHPB, CategoryNotFound, Book, BookDict

from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse

__version__ = "1.1"

ROOT_PATH = (lambda x: x if x is not None else "")(os.environ.get("ROOT_PATH")) # Like: /aghpb/v1

TAGS_METADATA = [
    {
        "name": "books",
        "description": "The main endpoints that allow you to get books." \
            "\n\n**All books come with extra info via headers like: ``Book-Name``, ``Book-Category``, ``Book-Date-Added``**",
    },
    {
        "name": "misc",
        "description": "Non-important endpoints."
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
@app.get(
    "/",
    name = "Takes you to these docs.",
    tags = ["misc"]
)
async def root():
    """Redirects you to this documentation page."""
    return RedirectResponse(f"{ROOT_PATH}/docs")


aghpb = AGHPB()

@app.get(
    "/random",
    name = "Get a random Book",
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
            "model": errors.CategoryNotFound, 
            "description": "The category was not Found."
        }
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

    return book.to_file_response()


@app.get(
    "/categories",
    name = "All Available Categories",
    tags = ["books"]
)
async def categories() -> List[str]:
    """Returns a list of all available categories."""
    return aghpb.categories


@app.get(
    "/search",
    name = "Query for books. NEW: v1.2",
    tags = ["books"]
)
async def search(query: str) -> List[BookDict]:
    """Returns list of book objects."""
    books: List[Book] = []

    for book in aghpb.books:
        if query.lower() in book.name.lower():
            books.append(book)

        else:
            if query.lower() in book.category.lower():
                books.append(book)

    return [
        book.to_dict() for book in books
    ]


@app.get(
    "/get/id",
    name = "Allows you to get a book by search id. NEW: v1.2",
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
            "model": errors.BookNotFound, 
            "description": "The book was not Found."
        }
    },
)
async def get_id(id: str) -> FileResponse:
    """Returns the book found."""
    for book in aghpb.books:

        if book.search_id == id:
            return book.to_file_response()

    return JSONResponse(
        status_code = 404, 
        content = {
            "error": "BookNotFound",
            "message": f"We couldn't find a book with search id '{id}'!"
        }
    )