# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

RUN pip3 install Flask gunicorn

COPY . .

EXPOSE 8000

CMD ["gunicorn"  , "-b", "0.0.0.0:8000", "app:app"]

