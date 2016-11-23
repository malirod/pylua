FROM ubuntu:16.04

ENV HOME /root
ENV PROJECT_ROOT $HOME/project

ADD . $PROJECT_ROOT

WORKDIR $HOME

RUN apt-get update
RUN apt-get install -y git fabric liblua5.2 liblua5.2-dev python3-dev python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install wheel
WORKDIR $PROJECT_ROOT
RUN pip3 install -r requirements.txt
