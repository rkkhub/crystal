FROM python:3.8-slim-buster

RUN apt-get update && apt-install -y \
    nano \
    apache2

RUN pip install --upgrade pip
ADD . /app

WORKDIR /app/

RUN pip install -r requirements.txt