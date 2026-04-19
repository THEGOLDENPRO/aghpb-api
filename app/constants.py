from decouple import config

__all__ = ()

RANDOM_BOOK_RATE_LIMIT = config("RANDOM_BOOK_RATE_LIMIT", default = 3, cast = int)
GET_BOOK_RATE_LIMIT = config("GET_BOOK_RATE_LIMIT", default = 3, cast = int)