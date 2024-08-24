FROM python:3.11-slim-bookworm

USER root

WORKDIR /app

COPY /api ./api
COPY pyproject.toml .
COPY Makefile .

RUN apt-get update && apt-get install -y git make

RUN mkdir assets
RUN make pull-repo
RUN cd ./assets/git_repo && git config features.manyFiles 1

RUN pip install .

EXPOSE 8000
ENV LISTEN_PORT=8000

CMD ["uvicorn", "api.main:app", "--host=0.0.0.0", "--proxy-headers"]