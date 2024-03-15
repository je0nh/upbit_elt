#!/bin/bash

# 네임스페이스 디렉토리를 입력받아서 
NAME_DIR=$1
echo $NAME_DIR

# 비어있지 않다면 이미 포맷된 것이므로 포맷을 진행
if [ "$(ls -A $NAME_DIR)" ]; then
  echo "NameNode is not formatted. Formatting NameNode."
  echo "Y" | $HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode -format
else
  echo "NameNode is already formatted."
fi

# NameNode 기동
$HADOOP_HOME/bin/hdfs --config $HADOOP_CONF_DIR namenode