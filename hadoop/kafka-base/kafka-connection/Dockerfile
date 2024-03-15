FROM kafka-base

RUN mkdir -p $KAFKA_HOME/confluent/connect
ENV CONFLUENT_HUB_HOME=$KAFKA_HOME/confluent
ADD worker.properties  $CONFLUENT_HUB_HOME/connect

RUN wget http://client.hub.confluent.io/confluent-hub-client-latest.tar.gz
RUN tar -xzvf confluent-hub-client-latest.tar.gz -C $CONFLUENT_HUB_HOME && rm confluent-hub-client-latest.tar.gz
ENV PATH="$CONFLUENT_HUB_HOME/bin:$PATH"

RUN echo 'y' | confluent-hub install confluentinc/kafka-connect-hdfs3:1.1.29 --component-dir $CONFLUENT_HUB_HOME/connect --worker-configs $CONFLUENT_HUB_HOME/connect/worker.properties

ADD kafka-conn-start.sh /kafka-conn-start.sh
RUN chmod +x /kafka-conn-start.sh

CMD ["/kafka-conn-start.sh"]
