#!/bin/bash

docker compose down

docker build -t ubuntu-base ./base-image
docker build -t hadoop-base ./hadoop-base
docker build -t kafka-base ./kafka-base

docker build -t hadoop-namenode ./namenode
docker build -t hadoop-datanode ./datanode
docker build -t resourcemanager ./yarn-rm
docker build -t yarn-timelineserver ./yarn-tls

docker compose up -d