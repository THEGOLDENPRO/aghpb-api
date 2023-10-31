FROM python:3.11-slim-bookworm

USER root

WORKDIR /app

COPY /.git ./.git
COPY .gitmodules .

COPY /api ./api
COPY pyproject.toml .

RUN apt-get update && apt-get install -y git

RUN mkdir assets
RUN git submodule update --init --recursive
RUN cd ./assets/git_repo && git config features.manyFiles 1

RUN pip install .

EXPOSE 8000
ENV LISTEN_PORT = 8000

CMD ["uvicorn", "api.main:app", "--host=0.0.0.0", "--proxy-headers"]