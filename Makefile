build:
	pip install -r requirements.txt

run:
	uvicorn api.main:app --reload

test:
	ruff .

bench-test:
	python scripts/bench_book_load.py
	snakeviz results.prof

pull-submodules:
	git submodule update --init --recursive

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up