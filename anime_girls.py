import os
from pathlib import Path
import subprocess
from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Book:
    path: str = field(kw_only=True)

    name: str = field(init=False)
    category: str = field(init=False)
    date_added: str = field(init=False)
    image_location: str = field(init=False)

    def __init__(self, path: str):
        file_name = os.path.split(path)[1]

        self.name = file_name.split(".")[0]
        self.category = Path(path).parent.name

        git_path = f"/{self.category}/{file_name}"

        # I use git here to scrape the date the image was added to the repo.
        p = subprocess.Popen(
            [f'cd ./assets/git_repo && git log --diff-filter=A -- "{f"./{git_path}"}"'], 
            stdout = subprocess.PIPE,
            shell = True
        )
        output, _ = p.communicate()

        self.date_added = datetime.strptime((output.decode().splitlines()[2]), "Date:   %a %b %d %H:%M:%S %Y %z")
        self.image_location = "/git_repo" + git_path

    def to_dict(self):
        return self.__dict__

class AGHPB():
    """Interface to the anime girls holding programming books directory."""
    def __init__(self) -> None:
        ...