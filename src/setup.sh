#!/bin/bash

# airflow db init
# airflow users create --username admin --password pwd --firstname Admin --lastname User --role Admin --email searaig@gmail.com
# airflow scheduler
# airflow webserver
#
# Start Zookeeper
# ~/kafka/bin/zookeeper-server-start.sh ~/kafka/config/zookeeper.properties &
# ZOOKEEPER_PID=$!
#
# # Wait for Zookeeper to initialize
# sleep 5
#
# # Start Kafka
# ~/kafka/bin/kafka-server-start.sh ~/kafka/config/server.properties &
# KAFKA_PID=$!
#
# # echo env vars
# printenv
#
# # Wait for both processes to keep the container alive
# wait $ZOOKEEPER_PID $KAFKA_PID
#
