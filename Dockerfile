# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user

RUN apt-get update && apt-get install -y curl

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

USER app_user
COPY . .
CMD ["bash"]