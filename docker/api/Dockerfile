FROM python:3.10

ENV PYTHONUNBUFFERED 1
RUN mkdir /workspace/
WORKDIR /workspace/
COPY requirements.txt /workspace/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . /workspace/
