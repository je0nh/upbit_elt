FROM hadoop-base

HEALTHCHECK CMD curl -f http://namenode:9870 || exit 1

ADD hdfs-site.xml $HADOOP_CONF_DIR

RUN mkdir $HADOOP_HOME/dfs/name

ADD start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 9000 9870

CMD ["/start.sh", "/opt/hadoop/dfs/name"]