from __future__ import annotations
from typing_extensions import List

import sys
import random
from pathlib import Path
from devgoldyutils import Colours, shorter_path

from .book import Book
from .errors import APIException
from .constants import GIT_REPO_PATH, EXCLUDED_FILES, ALLOWED_FILE_EXTENSIONS

__all__ = (
    "ProgrammingBooks", 
)

class ProgrammingBooks():
    """A class for interfacing with the anime girls holding programming books repo."""
    def __init__(self) -> None:
        self._repo_path = Path(GIT_REPO_PATH)

        self.books: List[Book] = []
        self.categories = []

        print(Colours.ORANGE.apply("Loading books..."))

        for index, file in enumerate(self._repo_path.rglob("*")):

            if file.suffix not in ALLOWED_FILE_EXTENSIONS:
                continue

            if file.name in EXCLUDED_FILES:
                sys.stdout.write(f"Ignoring the file '{Colours.GREY.apply(file.name)}'...\n")
                continue

            sys.stdout.write(
                f"{Colours.GREY.apply(f'({index}/???)')} Adding book from '{Colours.PINK_GREY.apply(shorter_path(file))}'...\n"
            )

            book = Book(file, str(index))

            if file.parent.name not in self.categories:
                self.categories.append(file.parent.name)

            self.books.append(book)

        print(Colours.GREEN.apply("[Done!]"))

    def random_category(self) -> str:
        return random.choice(self.categories)

    def random_book(self, category: str) -> Book:
        actual_category = None

        for cat in self.categories:
            if category.lower() == cat.lower():
                actual_category = cat
                break

        if actual_category is None:
            raise CategoryNotFound(category)

        return random.choice([book for book in self.books if book.category == actual_category])


class CategoryNotFound(APIException):
    def __init__(self, category: str) -> None:
        super().__init__(
            f"The category '{category}' was not found!"
        )