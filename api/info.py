from __future__ import annotations
from typing_extensions import TypedDict, final

__all__ = (
    "InfoData",
)

@final
class InfoData(TypedDict):
    book_count: int
    api_version: str