FROM python:3.9-slim

RUN mkdir /VkAnkiBot

WORKDIR /VkAnkiBot

COPY ./requirements.txt /VkAnkiBot/requirements.txt

RUN pip install pip --upgrade \
    && pip install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:./"

COPY . /VkAnkiBot
