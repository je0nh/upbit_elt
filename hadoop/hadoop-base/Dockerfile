FROM ubuntu-base

ENV HADOOP_FILE_NAME=hadoop-3.3.6
ENV HADOOP_URL=https://dlcdn.apache.org/hadoop/common/$HADOOP_FILE_NAME/$HADOOP_FILE_NAME.tar.gz

RUN wget $HADOOP_URL
RUN tar -xvzf $HADOOP_FILE_NAME.tar.gz && rm $HADOOP_FILE_NAME.tar.gz

RUN mv $HADOOP_FILE_NAME /opt
RUN ln -s /opt/$HADOOP_FILE_NAME /opt/hadoop
ENV HADOOP_HOME=/opt/hadoop

RUN ln -s $HADOOP_HOME/etc/hadoop /etc/hadoop
ENV HADOOP_CONF_DIR=/etc/hadoop

RUN mkdir $HADOOP_HOME/dfs
RUN rm -rf $HADOOP_HOME/share/doc
RUN mkdir -p $HADOOP_HOME/yarn/timeline

ADD core-site.xml $HADOOP_CONF_DIR
ADD yarn-site.xml $HADOOP_CONF_DIR
ADD mapred-site.xml $HADOOP_CONF_DIR

ENV YARN_CONF_DIR=$HADOOP_CONF_DIR
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin