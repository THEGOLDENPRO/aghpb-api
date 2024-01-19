import sys; sys.path.insert(0, '.')

import cProfile
from api.anime_girls import AGHPB

def bench_book_load():
    AGHPB()

cProfile.run("bench_book_load()", "results.prof")