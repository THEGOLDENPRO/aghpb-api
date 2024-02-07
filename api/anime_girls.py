from __future__ import annotations
from typing import TYPE_CHECKING
from typing_extensions import List, Tuple

if TYPE_CHECKING:
    from typing import Dict
    from .book import BookData

import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime
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

        self.__update_repo()
        self.books, self.categories = self.__phrase_books()

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

    def __update_repo(self):
        print(
            Colours.CLAY.apply(f"Attempting to update git repo at '{self._repo_path}'...")
        )

        process = subprocess.Popen(
            ["git", "pull"], 
            text = True, 
            stdout = subprocess.PIPE, 
            cwd = self._repo_path
        )

        process.wait()
        output, _ = process.communicate()

        if not process.returncode == 0:
            print(Colours.RED.apply("Git errored!!!"))

        print("Git Output: " + output)

    def __phrase_books(self) -> Tuple[List[Book], List[str]]:
        books = []
        categories = []

        file_count = "???"

        print(Colours.ORANGE.apply("Loading books..."))

        if sys.platform == "linux": # NOTE: Only works on Linux.
            file_count = subprocess.check_output(f'find "{self._repo_path.absolute()}" | wc -l', shell = True, text = True)[:-1]

        cached_books = self.__get_cache()

        search_id = 0

        for index, file in enumerate(self._repo_path.rglob("*")):

            if file.suffix not in ALLOWED_FILE_EXTENSIONS: # also excludes folders.
                continue

            if file.name in EXCLUDED_FILES:
                sys.stdout.write(f"Ignoring the file '{Colours.GREY.apply(file.name)}'...\n")
                continue

            cached_book = cached_books.get(str(file))

            add_msg = f"{Colours.GREY.apply(f'({index}/{file_count})')} Adding book from '{Colours.PINK_GREY.apply(shorter_path(file))}'...\n"
            sys.stdout.write(Colours.BLUE.apply("[CACHED] ") + add_msg if cached_book is not None else add_msg)

            if cached_book is not None:
                book = Book(
                    file, 
                    str(search_id), 
                    name = cached_book["name"],
                    category = cached_book["category"],
                    date_added = datetime.fromisoformat(cached_book["date_added"]),
                    commit_url = cached_book["commit_url"],
                    commit_author = cached_book["commit_author"],
                    commit_hash = cached_book["commit_hash"]
                )

            else:
                book = Book(file, str(search_id))
                cached_books[str(file)] = book.to_dict()

            if file.parent.name not in categories:
                categories.append(file.parent.name)

            books.append(book)
            search_id += 1

        self.__set_cache(cached_books)

        print(Colours.GREEN.apply("[Done!]"))
        return books, categories

    def __get_cache(self) -> Dict[str, BookData]:
        cached_books = {}

        books_cache_file = Path("./books_cache.json")

        if books_cache_file.exists():

            with books_cache_file.open() as file:
                cached_books = json.load(file)

        else:

            with books_cache_file.open("w") as file:
                print("Creating books cache file...")
                file.write("{}")

        return cached_books

    def __set_cache(self, data: Dict[str, BookData]) -> None:

        with open("./books_cache.json", "w") as file:
            json.dump(data, file)


class CategoryNotFound(APIException):
    def __init__(self, category: str) -> None:
        super().__init__(
            f"The category '{category}' was not found!"
        )