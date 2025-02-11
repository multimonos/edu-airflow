#!/bin/bash

echo "initializing airflow db ..."
airflow db init

echo "creating airflow user ..."
airflow users create \
    --username admin \
    --password pwd \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email searaig@gmail.com

echo "starting airflow scheduler ..."
airflow scheduler & $SCHEDULER_PID

echo "starting airflow webserver ..."
airflow webserver & $WEBSERVER_PID

wait $SCHEDULER_PID

