FROM python:3.9-slim

RUN mkdir /vkbot

WORKDIR /vkbot

COPY ./vkbot/requirements.txt /vkbot/requirements.txt

RUN pip install pip --upgrade \
    && pip install -r requirements.txt

COPY ./vkbot /vkbot