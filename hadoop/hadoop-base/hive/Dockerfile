FROM hadoop-namenode

ENV HIVE_VERSION=3.1.3

RUN wget https://downloads.apache.org/hive/hive-$HIVE_VERSION/apache-hive-$HIVE_VERSION-bin.tar.gz
RUN tar -xzvf apache-hive-$HIVE_VERSION-bin.tar.gz -C /opt
RUN rm apache-hive-$HIVE_VERSION-bin.tar.gz

RUN ln -s apache-hive-3.1.3-bin/ /opt/hive
ENV PATH=$PATH:/opt/hive/bin
ENV HIVE_HOME=/opt/hive
ENV HIVE_CONF_DIR=$HIVE_HOME/conf

ADD hive-site.xml $HIVE_CONF_DIR
ADD hive-exec-log4j2.properties $HIVE_CONF_DIR
ADD hive-log4j2.properties $HIVE_CONF_DIR
ADD beeline-hs2-connection.xml $HIVE_CONF_DIR
RUN cp $HIVE_CONF_DIR/beeline-log4j2.properties.template $HIVE_CONF_DIR/beeline-log4j2.properties

ENV MYSQL_CONNECTOR_VERSION=8.3.0
RUN wget http://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-$MYSQL_CONNECTOR_VERSION.tar.gz
RUN tar -xzvf mysql-connector-j-$MYSQL_CONNECTOR_VERSION.tar.gz
RUN cp mysql-connector-j-$MYSQL_CONNECTOR_VERSION/*.jar $HIVE_HOME/lib
RUN rm mysql-connector-j-$MYSQL_CONNECTOR_VERSION.tar.gz
RUN rm -r mysql-connector-j-$MYSQL_CONNECTOR_VERSION

CMD ["/start.sh", "/opt/hadoop/dfs/name"]