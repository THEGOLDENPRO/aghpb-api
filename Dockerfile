FROM python:3.12.13-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:0.11.2 /uv /uvx /bin/

USER root
WORKDIR /app

COPY /app ./app
COPY pyproject.toml .

RUN apt-get update && apt-get install -y git

RUN mkdir assets
RUN git clone https://github.com/cat-milk/Anime-Girls-Holding-Programming-Books ./assets/git_repo
RUN cd ./assets/git_repo && git config features.manyFiles 1

ENV UV_NO_DEV=1

COPY uv.lock .
RUN uv sync --locked

EXPOSE 8000
ENV LISTEN_PORT=8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host=0.0.0.0", "--proxy-headers"]