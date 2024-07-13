FROM python:3.10-slim

RUN mkdir /web
WORKDIR /web

COPY requirements.txt /web/

RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . /web/

RUN python manage.py makemigrations && python manage.py migrate