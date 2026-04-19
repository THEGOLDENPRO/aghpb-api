import os
import sys
sys.path.insert(0, '.')

import cProfile
from app.repository import ProgrammingBooks

def bench_book_load():
    ProgrammingBooks(repo_path = os.environ["GIT_REPO_PATH"])

cProfile.run("bench_book_load()", "results.prof")