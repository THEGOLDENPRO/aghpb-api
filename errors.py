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