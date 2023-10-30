from __future__ import annotations
from typing_extensions import List, TypedDict, final

import os
import sys
import random
from pathlib import Path
import subprocess
from datetime import datetime
from dataclasses import dataclass, field
from devgoldyutils import Colours
from fastapi.responses import FileResponse

from errors import APIException

EXCLUDED_FILES = [".DS_Store"]
GIT_REPO_PATH = "./assets/git_repo"

@final
class BookDict(TypedDict):
    search_id: str
    name: str
    category: str
    date_added: str

@dataclass
class Book:
    path: str = field(repr=False)
    search_id: str

    name: str = field(init=False)
    category: str = field(init=False)
    location: str = field(init=False, repr=False)
    date_added: datetime = field(init=False)

    def __post_init__(self):
        file_name = os.path.split(self.path)[1]

        self.name = file_name.split(".")[0].replace("_", " ").capitalize()
        self.category = Path(self.path).parent.name

        git_path = f"/{self.category}/{file_name}"

        # I use git here to scrape the date the image was added to the repo.
        p = subprocess.Popen(
            ["cd", GIT_REPO_PATH, "&&", "git", "log", "--diff-filter=A", "--", f"./{git_path}"],
            #[f'cd {GIT_REPO_PATH} && git log --diff-filter=A -- "{f"./{git_path}"}"'], 
            stdout = subprocess.PIPE,
            shell = True
        )
        output, _ = p.communicate()

        self.date_added = datetime.strptime((output.decode().splitlines()[2]), "Date:   %a %b %d %H:%M:%S %Y %z")
        self.location = "/git_repo" + git_path

    def to_dict(self) -> BookDict:
        return {
            "search_id": self.search_id,
            "name": self.name,
            "category": self.category,
            "date_added": str(self.date_added)
        }

    def to_file_response(self) -> FileResponse:
        """Returns file response object."""
        return FileResponse(
            self.path,
            headers = {
                "Book-Name": self.name,
                "Book-Category": self.category,
                "Book-Search-ID": self.search_id,
                "Book-Date-Added": str(self.date_added),
                "Last-Modified": str(self.date_added),

                "Pragma": "no-cache",
                "Expires": "0",
                "Cache-Control": "no-cache, no-store, must-revalidate, public, max-age=0"
            }
        )

class AGHPB():
    """Interface to the anime girls holding programming books directory."""
    def __init__(self) -> None:
        self.books: List[Book] = []
        self.categories = [x for x in os.listdir(GIT_REPO_PATH) if os.path.isdir(f"{GIT_REPO_PATH}/{x}")]

        print(Colours.ORANGE.apply("Loading books..."))

        _id = 0
        for category in self.categories:

            for book in os.listdir(f"{GIT_REPO_PATH}/{category}"):
                if book in EXCLUDED_FILES:
                    continue

                book = Book(f"{GIT_REPO_PATH}/{category}/{book}", str(_id))
                self.books.append(book)

                sys.stdout.write(f"Book '{Colours.BLUE.apply(book.name)}' added!\n")
                _id += 1

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