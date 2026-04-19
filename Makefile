.PHONY: build

build:
	echo "Nothing to build here."

bench-test:
	python scripts/bench_book_load.py
	snakeviz results.prof