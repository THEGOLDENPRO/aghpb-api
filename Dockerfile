FROM python:3.11

USER root

WORKDIR /app

COPY /.git ./.git
COPY .gitmodules .

COPY main.py .
COPY errors.py .
COPY anime_girls.py .
COPY pyproject.toml .

RUN mkdir assets
RUN git submodule update --init --recursive

RUN pip install .

EXPOSE 8000
ENV LISTEN_PORT = 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--proxy-headers"]