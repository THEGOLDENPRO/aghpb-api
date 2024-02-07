from __future__ import annotations
from typing_extensions import TypedDict, final

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from fastapi.responses import FileResponse

from .constants import GIT_REPO_PATH, GIT_REPO_URL

__all__ = (
    "BookData",
)

@final
class BookData(TypedDict):
    search_id: str
    name: str
    category: str
    date_added: str
    commit_url: str
    commit_author: str
    commit_hash: str

@dataclass
class Book:
    path: Path = field(repr=False)
    search_id: str

    name: str = field(default=None)
    category: str = field(default=None)
    date_added: datetime = field(default=None)
    commit_url: str = field(default=None)
    commit_author: str = field(default=None)
    commit_hash: str = field(default=None)

    def __post_init__(self):
        self.name = self.name or self.path.name.split(".")[0].replace("_", " ").capitalize()
        self.category = self.category or self.path.parent.name

        if self.date_added is None and self.commit_url is None and self.commit_author is None and self.commit_hash is None:

            # I use git here to scrape the date the book was added to the repo.
            args = [f'cd "{GIT_REPO_PATH}" && git log --diff-filter=A -- "{f"{self.path.absolute()}"}"']

            if sys.platform == "win32":
                args = ["cd", GIT_REPO_PATH, "&&", "git", "log", "--diff-filter=A", "--", f"{self.path.absolute()}"]

            p = subprocess.Popen(
                args,
                stdout = subprocess.PIPE,
                shell = True
            )
            output, _ = p.communicate()
            git_log = output.decode()

            self.commit_hash = git_log.splitlines()[0].split('commit ')[1]
            self.commit_author = git_log.splitlines()[1].split('Author: ')[1].split("<")[0][:-1]
            self.commit_url = GIT_REPO_URL + f"/commit/{self.commit_hash}"

            self.date_added = datetime.strptime((git_log.splitlines()[2]), "Date:   %a %b %d %H:%M:%S %Y %z")

    def to_dict(self) -> BookData:
        return {
            "search_id": self.search_id,
            "name": self.name,
            "category": self.category,
            "date_added": str(self.date_added),
            "commit_url": self.commit_url,
            "commit_author": self.commit_author,
            "commit_hash": self.commit_hash
        }

    def to_file_response(self, expires: str = "0") -> FileResponse:
        """Returns file response object."""
        #try: # Testing to see if the author name can encode. If not just set it as null.
        #    self.commit_author.encode("latin-1")
        #except UnicodeEncodeError as e:
        #    self.commit_author = "null"
        #    print(e)

        return FileResponse(
            self.path,
            headers = {
                "Book-Name": self.name, 
                "Book-Category": self.category, 
                "Book-Search-ID": self.search_id, 
                "Book-Date-Added": str(self.date_added), 
                "Book-Commit-URL": self.commit_url, 
                "Book-Commit-Author": self.commit_author.encode("utf-8").decode("latin-1", "replace"), 
                # NOTE: Is that better than just setting it as "null" if the name can't be encoded.
                "Book-Commit-Hash": self.commit_hash, 
                "Last-Modified": str(self.date_added), 

                #"Pragma": "no-cache", 
                "Expires": expires, 
                #"Cache-Control": "no-cache, no-store, must-revalidate, public, max-age=0"
            }
        )