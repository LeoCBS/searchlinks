FROM python:3.5.2

MAINTAINER Leonardo Cesar Borges <leocborgess@gmail.com>

ENV WORKDIR /project

ENV PYTHONPATH $WORKDIR

COPY requirements.txt $WORKDIR/requirements.txt

WORKDIR $WORKDIR

RUN pip install -r requirements.txt

COPY ./ $WORKDIR
