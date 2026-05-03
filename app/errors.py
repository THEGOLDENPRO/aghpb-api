from typing import NoReturn

from pydantic import BaseModel
from fastapi import Request, Response

__all__ = ()

# TODO: will need to revamp and improve all of this

class APIError(Exception):
    def __init__(
        self,
        error: str,
        message: str,
        status_code: int,
    ) -> None:
        self.error = error
        self.message = message
        self.status_code = status_code

class CategoryNotFoundError(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "CategoryNotFound",
                    "message": "The category 'rust' was not found!"
                }
            ]
        }
    }

    @classmethod
    def get_exception(_cls, category: str) -> APIError:
        return APIError(
            error = "CategoryNotFound",
            message = f"The category '{category}' was not found!",
            status_code = 404
        )

class BookNotFoundError(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "BookNotFound",
                    "message": "We couldn't find a book with search id '396'!"
                }
            ]
        }
    }

    @classmethod
    def get_exception(_cls, search_id: str) -> APIError:
        return APIError(
            error = "BookNotFound",
            message = f"We couldn't find a book with search id '{search_id}'!",
            status_code = 404
        )

class RateLimitedError(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "RateLimited",
                    "message": "Rate Limit exceeded!"
                }
            ]
        }
    }

    @classmethod
    def get_exception(_cls) -> APIError:
        return APIError(
            error = "RateLimited",
            message = "Rate limit exceeded! Follow the rates: https://github.com/THEGOLDENPRO/aghpb_api/wiki#rate-limiting",
            status_code = 429
        )

def rate_limit_exceeded_error(_request: Request, _response: Response) -> NoReturn:
    raise RateLimitedError.get_exception()