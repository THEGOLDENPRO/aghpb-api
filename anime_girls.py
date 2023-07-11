import os
import random
from pathlib import Path
import subprocess
from datetime import datetime
from dataclasses import dataclass, field

from errors import APIException

EXCLUDED_FILES = [".DS_Store"]

@dataclass
class Book:
    path: str

    name: str = field(init=False)
    category: str = field(init=False)
    location: str = field(init=False)
    date_added: str = field(init=False)

    def __post_init__(self):
        file_name = os.path.split(self.path)[1]

        self.name = file_name.split(".")[0]
        self.category = Path(self.path).parent.name

        git_path = f"/{self.category}/{file_name}"

        # I use git here to scrape the date the image was added to the repo.
        p = subprocess.Popen(
            [f'cd ./assets/git_repo && git log --diff-filter=A -- "{f"./{git_path}"}"'], 
            stdout = subprocess.PIPE,
            shell = True
        )
        output, _ = p.communicate()

        self.date_added = datetime.strptime((output.decode().splitlines()[2]), "Date:   %a %b %d %H:%M:%S %Y %z")
        self.location = "/git_repo" + git_path

    def to_dict(self):
        return self.__dict__

class AGHPB():
    """Interface to the anime girls holding programming books directory."""
    def __init__(self) -> None:
        self.path_to_repo = "./assets/git_repo"

        self.categories_list = [x for x in os.listdir(self.path_to_repo) if os.path.isdir(f"{self.path_to_repo}/{x}")]

    def random_category(self) -> str:
        return random.choice(self.categories_list)

    def random_book(self, category: str) -> Book:
        actual_category = None

        for cat in self.categories_list:
            if category.lower() == cat.lower():
                actual_category = cat
                break

        if actual_category is None:
            raise CategoryNotFound(category)

        books = [x for x in os.listdir(f"{self.path_to_repo}/{actual_category}") if not x in EXCLUDED_FILES]

        random_book = random.choice(books)

        return Book(f"{self.path_to_repo}/{actual_category}/{random_book}")


class CategoryNotFound(APIException):
    def __init__(self, category: str) -> None:
        super().__init__(
            f"The category '{category}' was not found!"
        )