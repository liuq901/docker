FROM ubuntu

MAINTAINER liuq901

RUN apt-get install python -y

ADD main.py main.py
ADD run.sh run.sh

ENTRYPOINT ./run.sh
