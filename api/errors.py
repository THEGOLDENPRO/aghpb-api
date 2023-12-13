from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel

__all__ = (
    "APIException",
    "CategoryNotFound",
    "BookNotFound",
    "RateLimited",
    "rate_limit_handler"
)

class APIException(Exception):
    def __init__(self, msg) -> None:
        self.msg = msg
        super().__init__(msg)


class CategoryNotFound(BaseModel):
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

class BookNotFound(BaseModel):
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

class RateLimited(BaseModel):
    error: str
    message: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "RateLimited",
                    "message": "Rate Limit exceeded: 3 per 1 second"
                }
            ]
        }
    }


def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code = 429,
        content = {
            "error": "RateLimited", 
            "message": f"Rate limit exceeded: {exc.detail} (Follow the rates: )" # TODO: Add link to git wiki page.
        }
    )

    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )

    return response