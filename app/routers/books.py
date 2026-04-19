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
        category = random.choice(programming_books.categories)

    book = programming_books.random_book(category)

    if book is None:
        raise CategoryNotFoundError.get_exception(category)

    return book.to_file_response()

@router.get(
    "/categories",
    name = "All available categories",
    tags = ["books"]
)
async def categories(programming_books: ProgrammingBooksDep) -> list[str]:
    """Returns a list of all available categories."""
    return programming_books.categories

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
    books: list[tuple[int, Book]] = []

    for book in programming_books.books:
        if len(books) == limit:
            break

        if category is not None and not category.lower() == book.category.lower():
            continue

        name_match_ratio = fuzz.partial_ratio(book.name.lower(), query.lower())

        if name_match_ratio > 70:
            books.append((name_match_ratio, book))

    books.sort(key = lambda x: x[0], reverse = True) # Sort in order of highest match.

    return [
        book[1] for book in books
    ]

# TODO: omg this code is dogshit, this all should be prefetched
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
        # NOTE: If you update the git repo it may take a literal minute for books to refresh, depending on how your master server caches.

        expires_timestamp = timestamp_to_set
        get_book_cache[search_id] = timestamp_to_set

    for book in programming_books.books:

        if book.search_id == search_id:
            return book.to_file_response(
                0 if expires_timestamp is None else formatdate(expires_timestamp, usegmt = True)
            )

    raise BookNotFoundError.get_exception(search_id)