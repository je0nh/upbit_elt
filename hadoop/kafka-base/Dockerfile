FROM ubuntu-base

ENV SCALA_VERSION=2.12
ENV KAFKA_VERSION=3.7.0
ENV KAFKA_FILE_NAME=kafka_$SCALA_VERSION-$KAFKA_VERSION
ENV KAFKA_URL=https://downloads.apache.org/kafka/$KAFKA_VERSION/$KAFKA_FILE_NAME.tgz

RUN wget $KAFKA_URL
RUN tar -xvzf $KAFKA_FILE_NAME.tgz && rm $KAFKA_FILE_NAME.tgz
RUN mv $KAFKA_FILE_NAME /opt
RUN ln -s /opt/$KAFKA_FILE_NAME /opt/kafka
RUN mkdir /opt/kafka/kraft-combined-logs

ENV KAFKA_HOME=/opt/kafka
ENV PATH=$PATH:$KAFKA_HOME/bin