run:
	uvicorn main:app --reload

docker-build:
	python scripts/docker_build.py

docker-compose:
	docker compose up