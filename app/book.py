from __future__ import annotations

import subprocess
from pathlib import Path
from datetime import datetime
from fastapi.responses import FileResponse

from pydantic import BaseModel, PrivateAttr

__all__ = ()

class Book(BaseModel):
    name: str
    category: str
    date_added: str
    commit_url: str
    commit_author: str
    commit_hash: str
    search_id: str

    _image_path: Path = PrivateAttr()

    @classmethod
    def parse(cls, search_id: str, image_path: Path, git_repo_path: Path) -> Book:
        git_command = [
            "git",
            f"--git-dir={git_repo_path.absolute().joinpath(".git")}",
            "log",
            "--diff-filter=A",
            "--",
            f"{image_path.parent.name}/{image_path.name}"
        ]

        git_log_string = subprocess.check_output(
            git_command,
            text = True
        )

        commit_hash = git_log_string.splitlines()[0].split('commit ')[1]

        date_added = datetime.strptime(
            git_log_string.splitlines()[2],
            "Date:   %a %b %d %H:%M:%S %Y %z"
        )

        book = cls(
            name = image_path.name.split(".")[0].replace("_", " ").capitalize(),
            category = image_path.parent.name,
            date_added = str(date_added),
            commit_hash = commit_hash,
            commit_author = git_log_string.splitlines()[1].split('Author: ')[1].split("<")[0][:-1],
            commit_url = f"https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books/commit/{commit_hash}",
            search_id = search_id
        )

        book._image_path = image_path

        return book

    def to_file_response(self, expires: str = "0") -> FileResponse:
        # NOTE: Is that better than just setting it as "null" if the name can't be encoded.
        commit_author_name = self.commit_author.encode("utf-8").decode("latin-1", "replace")

        return FileResponse(
            self._image_path,
            headers = {
                "Book-Name": self.name,
                "Book-Category": self.category,
                "Book-Search-ID": self.search_id,
                "Book-Date-Added": self.date_added,
                "Book-Commit-URL": self.commit_url,
                "Book-Commit-Author": commit_author_name,
                "Book-Commit-Hash": self.commit_hash,

                "Last-Modified": self.date_added,
                "Expires": expires,
            }
        )
