import sys; sys.path.insert(0, '.')

import cProfile
from api.anime_girls import ProgrammingBooks

def bench_book_load():
    ProgrammingBooks()

cProfile.run("bench_book_load()", "results.prof")