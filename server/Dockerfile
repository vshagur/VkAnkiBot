FROM python:3.9-slim

RUN mkdir /server

WORKDIR /server

COPY ./server/requirements.txt /server/requirements.txt

RUN pip install pip --upgrade \
    && pip install -r requirements.txt

COPY ./server /server

EXPOSE 8080
