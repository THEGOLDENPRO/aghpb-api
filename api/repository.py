from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Dict, Optional, List

    from .book import BookData

import sys
import json
import random
import subprocess
from pathlib import Path
from datetime import datetime
from devgoldyutils import Colours, shorter_path

from .book import Book

__all__ = (
    "ProgrammingBooks", 
)

EXCLUDED_FILES = [".DS_Store"]
ALLOWED_FILE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif"]

class ProgrammingBooks():
    """A class for interfacing with a local anime girls holding programming books repository."""
    def __init__(self, repo_path: str) -> None:
        self._repo_path = Path(repo_path)

        self.__repo_hash: str = None
        self.__repo_last_updated: datetime = None

        self.books: List[Book] = []
        self.categories: List[str] = []

    def random_book(self, category: str) -> Optional[Book]:
        actual_category = None

        for cat in self.categories:
            if category.lower() == cat.lower():
                actual_category = cat
                break

        if actual_category is None:
            return None

        return random.choice(
            [book for book in self.books if book.category == actual_category]
        )

    @property
    def repo_hash(self) -> str:
        if self.__repo_hash is None:
            output = subprocess.check_output(
                ["git", "rev-parse", "HEAD"],
                cwd = self._repo_path,
                text = True,
            )

            self.__repo_hash = output.removesuffix("\n")

        return self.__repo_hash

    @property
    def repo_last_updated(self) -> datetime:
        if self.__repo_last_updated is None:
            output = subprocess.check_output(
                ["git", "log", "-1"],
                cwd = self._repo_path,
                text = True,
            )

            self.__repo_last_updated = datetime.strptime((output.split("Date:   ")[1].splitlines()[0]), "%a %b %d %H:%M:%S %Y %z")

        return self.__repo_last_updated

    def update_repo(self):
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

    def parse_books(self) -> None:
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

        self.books = books
        self.categories = categories

        print(Colours.GREEN.apply("[Done!]"))

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