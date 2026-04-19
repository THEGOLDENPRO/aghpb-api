from typing import Optional

import sys
import random
import subprocess
from pathlib import Path
from datetime import datetime
from pydantic import TypeAdapter

from .book import Book
from .colours import Colours

__all__ = ()

EXCLUDED_FILES = [".DS_Store"]
ALLOWED_FILE_EXTENSIONS = [".png", ".jpeg", ".jpg", ".gif"]

class ProgrammingBooks():
    """A class for interfacing with a local anime girls holding programming books repository."""
    def __init__(self) -> None:
        self._repo_path = Path("./assets/git_repo")

        self.__repo_hash: Optional[str] = None
        self.__repo_last_updated: Optional[datetime] = None

        self.books: list[Book] = []
        self.categories: list[str] = []

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
        books: list[Book] = []
        categories: list[str] = []

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

            shortened_path = f"{file.parent.name}/{file.name}"

            add_message = f"{Colours.GREY.apply(f'({index}/{file_count})')} " \
                f"Adding book from '{Colours.PINK_GREY.apply(shortened_path)}'...\n"

            sys.stdout.write(
                Colours.BLUE.apply("[CACHED] ") + add_message if cached_book is not None else add_message
            )

            if cached_book is None:
                book = Book.parse(
                    search_id = str(search_id),
                    image_path = file,
                    git_repo_path = self._repo_path
                )
                cached_books[str(file)] = book.model_dump()
            else:
                book = cached_book
                book._image_path = file

            if file.parent.name not in categories:
                categories.append(file.parent.name)

            books.append(book)
            search_id += 1

        self.__set_cache(cached_books)

        if "git_repo" in categories:
            categories.remove("git_repo")

        self.books = books
        self.categories = categories

        print(Colours.GREEN.apply("[Done!]"))

    def __get_cache(self) -> dict[str, Book]:
        cached_books = {}

        books_cache_file = Path("./books_cache.json")

        if books_cache_file.exists():
            with books_cache_file.open() as file:
                json_data = file.read()

                adapter = TypeAdapter(dict[str, Book])

                cached_books = adapter.validate_json(json_data)

        else:
            with books_cache_file.open("w") as file:
                print("Creating books cache file...")
                file.write("{}")

        return cached_books

    def __set_cache(self, cached_books: dict[str, Book]) -> None:
        adapter = TypeAdapter(dict[str, Book])

        json_data = adapter.dump_json(cached_books)

        with open("./books_cache.json", "wb") as file:
            file.write(json_data)