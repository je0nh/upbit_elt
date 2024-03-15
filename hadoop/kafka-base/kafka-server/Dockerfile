FROM kafka-base

ADD server.properties $KAFKA_HOME/config/kraft
ADD kafka-start.sh /kafka-start.sh
RUN chmod +x /kafka-start.sh

CMD ["/kafka-start.sh"]