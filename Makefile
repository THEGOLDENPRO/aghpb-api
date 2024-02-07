build:
	pip install . -U

run:
	uvicorn api.main:app --reload

test:
	ruff .

pull-repo:
	git clone https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books ./assets/git_repo

update-repo:
	cd ./assets/git_repo && git pull

bench-test:
	python scripts/bench_book_load.py
	snakeviz results.prof

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up