#!/bin/bash

# 첫 번째 명령어 실행하여 UUID 생성
KAFKA_UUID="$($KAFKA_HOME/bin/kafka-storage.sh random-uuid)"
echo "Generated Kafka UUID: $KAFKA_UUID"

# 두 번째 명령어 실행하여 Kafka 서버 포맷팅 및 설정
$KAFKA_HOME/bin/kafka-storage.sh format -t "$KAFKA_UUID" -c "$KAFKA_HOME/config/kraft/server.properties"

# kafka 실행
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/kraft/server.properties