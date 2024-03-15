# Ubuntu base
FROM ubuntu:latest

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y wget

# Install python 3.10
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.10

# 기존 설정 초기화
RUN echo "alias python='/usr/bin/python3'" >> ~/.bashrc
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3

# pip 설치
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip

# OpenJDK 설치
RUN apt-get install -y openjdk-11-jdk
ENV JAVA_HOME='/usr/lib/jvm/java-11-openjdk-amd64'
