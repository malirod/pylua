FROM ubuntu:18.10

ENV HOME /root
ENV PROJECT_ROOT $HOME/project

ADD . $PROJECT_ROOT

WORKDIR $HOME

RUN apt-get update
RUN apt-get install -y git liblua5.3 liblua5.3-dev python3-dev python3-pip
RUN pip3 install --upgrade pip
WORKDIR $PROJECT_ROOT
RUN pip3 install -r requirements.txt