build:
	pip install .

run:
	uvicorn api.main:app --reload

pull-submodules:
	git submodule update --init --recursive

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up