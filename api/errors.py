from fastapi import Request
from slowapi.errors import RateLimitExceeded
from fastapi.responses import JSONResponse
from pydantic import BaseModel

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

class BookNotFound(BaseModel):
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

def RateLimited(request: Request, exc: RateLimitExceeded):
    response = JSONResponse(
        {"error": f"RateLimited", "message": f"Rate Limit exceeded: {exc.detail}"}, status_code=429
    )

    response = request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )

    return response