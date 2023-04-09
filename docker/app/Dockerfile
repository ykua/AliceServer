FROM python:3.11-bullseye

ENV PYTHONUNBUFFERED 1
ENV FLASK_APP=app

WORKDIR /usr/src/app/
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
