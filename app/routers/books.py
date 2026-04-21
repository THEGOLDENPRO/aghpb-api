from typing import Annotated, Optional

import random
from thefuzz import fuzz
from decouple import config
from datetime import datetime
from email.utils import formatdate
from pyrate_limiter import Limiter, Rate
from fastapi.responses import FileResponse
from fastapi_limiter.depends import RateLimiter
from fastapi import APIRouter, Depends, Query

from ..book import Book
from ..repository import ProgrammingBooks
from ..dependencies import get_programming_books
from ..errors import RateLimitedError, BookNotFoundError, CategoryNotFoundError, rate_limit_exceeded_error

__all__ = ()

router = APIRouter()

GET_BOOK_RATE_LIMIT = config("GET_BOOK_RATE_LIMIT", default = 3, cast = int)
RANDOM_BOOK_RATE_LIMIT = config("RANDOM_BOOK_RATE_LIMIT", default = 3, cast = int)

ANIME_BOOK_200_RESPONSE = {
    "content": {
        "image/png": {},
        "image/jpeg": {},
        "image/gif": {},
    },
    "description": "Returned an anime girl holding a programming book successfully. 😁",
}

ProgrammingBooksDep = Annotated[ProgrammingBooks, Depends(get_programming_books)]

@router.get(
    "/random",
    name = "Get a random programming book",
    tags = ["books"],
    response_class = FileResponse,
    responses = {
        200: ANIME_BOOK_200_RESPONSE,
        404: {
            "model": CategoryNotFoundError, 
            "description": "The category was not Found."
        },
        429: {
            "model": RateLimitedError,
            "description": "Rate limit exceeded!"
        }
    },
    dependencies = [
        Depends(
            RateLimiter(
                limiter = Limiter(Rate(limit = RANDOM_BOOK_RATE_LIMIT, interval = 3000)),
                callback = rate_limit_exceeded_error
            )
        )
    ],
)
async def random_(programming_books: ProgrammingBooksDep, category: Optional[str] = None) -> FileResponse:
    """Returns a random book."""
    if category is None:
        category = random.choice(list(programming_books.books_map.keys()))

    id_book_map = programming_books.books_map.get(category.lower())

    if id_book_map is None:
        raise CategoryNotFoundError.get_exception(category)

    book = random.choice(list(id_book_map.values()))

    return book.to_file_response()

@router.get(
    "/categories",
    name = "All available categories",
    tags = ["books"]
)
async def categories(programming_books: ProgrammingBooksDep) -> list[str]:
    """Returns a list of all available categories."""
    return list(programming_books.books_map.keys())

@router.get(
    "/search",
    name = "Query for books.",
    tags = ["books"],
)
async def search(
    query: str,
    programming_books: ProgrammingBooksDep,
    category: Optional[str] = None,
    limit: int = Query(ge = 1, default = 50)
) -> list[Book]:
    """Returns list of book objects."""
    unordered_books: list[tuple[int, Book]] = []

    for book_category in programming_books.books_map:
        id_book_map = programming_books.books_map[category]

        if category is not None and not category.lower() == book_category:
            continue

        for book in id_book_map.values():
            if len(unordered_books) == limit:
                break

            name_match_ratio = fuzz.partial_ratio(book.name.lower(), query.lower())

            if name_match_ratio > 70:
                unordered_books.append((name_match_ratio, book))

    unordered_books.sort(key = lambda x: x[0], reverse = True) # Sort in order of highest match.

    return [
        book[1] for book in unordered_books
    ]

get_book_cache: dict[str, float] = {}

@router.get(
    "/get/id/{search_id}",
    name = "Allows you to get a book by search id.",
    tags = ["books"],
    response_class = FileResponse,
    responses = {
        200: ANIME_BOOK_200_RESPONSE,
        404: {
            "model": BookNotFoundError,
            "description": "The book was not Found."
        },
        429: {
            "model": RateLimitedError,
            "description": "Rate Limit exceeded"
        }
    },
    dependencies = [
        Depends(
            RateLimiter(
                limiter = Limiter(Rate(limit = GET_BOOK_RATE_LIMIT, interval = 3000)),
                callback = rate_limit_exceeded_error
            )
        )
    ],
)
async def get_id(search_id: str, programming_books: ProgrammingBooksDep) -> FileResponse:
    """Returns the book found."""
    expires_timestamp = get_book_cache.get(search_id, 0)

    if datetime.now().timestamp() > expires_timestamp:
        timestamp_to_set = datetime.now().timestamp() + 60 * 10 # 10 minutes until this book expires.

        expires_timestamp = timestamp_to_set
        get_book_cache[search_id] = timestamp_to_set

    for id_book_map in programming_books.books_map.values():
        book = id_book_map.get(search_id)

        if book is None:
            continue

        return book.to_file_response(
            0 if expires_timestamp is None else formatdate(expires_timestamp, usegmt = True)
        )

    raise BookNotFoundError.get_exception(search_id)