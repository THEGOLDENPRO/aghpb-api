from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel

__all__ = (
    "APIException",
    "CategoryNotFoundError",
    "BookNotFoundError",
    "RateLimitedError",
    "rate_limit_error_handler"
)

class APIException(Exception):
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

class RateLimitedError(BaseModel):
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

def rate_limit_error_handler(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        status_code = 429,
        content = {
            "error": "RateLimited", 
            "message": f"Rate limit exceeded: {exc.detail} (Follow the rates: https://github.com/THEGOLDENPRO/aghpb_api/wiki#rate-limiting)"
        }
    )

    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )

    return response