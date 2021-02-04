FROM python:3.9-slim

COPY ./vkbot /vkbot

RUN pip install pip --upgrade \
    && pip install -r /vkbot/requirements.txt

WORKDIR /vkbot
