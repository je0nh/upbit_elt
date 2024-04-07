#!/bin/bash

docker compose down

docker build -t ubuntu-base ./base-image
docker build -t hadoop-base ./hadoop-base
# docker build -t kafka-base ./kafka-base

docker build -t hadoop-namenode ./hadoop-base/namenode
docker build -t hadoop-datanode ./hadoop-base/datanode
docker build -t resourcemanager ./hadoop-base/yarn-rm
docker build -t yarn-timelineserver ./hadoop-base/yarn-tls
