FROM python:3.11-slim-bullseye

ENV PYTHONUNBUFFERED 1
RUN mkdir /workspace/
WORKDIR /workspace/
COPY requirements.txt /workspace/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY . /workspace/
