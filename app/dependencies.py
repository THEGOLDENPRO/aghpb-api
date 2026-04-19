from fastapi import Request

from .repository import ProgrammingBooks

__all__ = ()

def get_programming_books(request: Request) -> ProgrammingBooks:
    return request.app.state.repository