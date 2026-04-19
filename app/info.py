from pydantic import BaseModel

__all__ = ()

class Info(BaseModel):
    book_count: int
    api_version: str
    repo_hash: str
    repo_last_updated: str