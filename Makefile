build:
	pip install -r requirements.txt

run:
	uvicorn api.main:app --reload

test:
	ruff .

pull-repo:
	git clone https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books ./assets/git_repo

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up