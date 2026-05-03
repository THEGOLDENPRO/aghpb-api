import sys
sys.path.insert(0, '.')

import cProfile
from app.repository import ProgrammingBooks

def bench_book_load():
    ProgrammingBooks()

cProfile.run("bench_book_load()", "results.prof")