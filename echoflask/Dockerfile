
FROM ubuntu:16.04

WORKDIR /ansible/echoflask

RUN apt update -y && apt install python-flask -yy

RUN useradd -ms /bin/bash lenka

USER lenka

LABEL maintainer="lenka"

ENV REPLY_HOSTNAME = 'unset'

COPY app.py .

ENTRYPOINT ["python","app.py"]
