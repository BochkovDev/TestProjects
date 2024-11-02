FROM python:3.12-slim-bullseye

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usr/src/chitchat
WORKDIR /usr/src/chitchat

RUN apt -y update

COPY ./requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN chmod +x /usr/src/chitchat/docker/app/server-entrypoint.sh

WORKDIR /usr/src/chitchat/app
