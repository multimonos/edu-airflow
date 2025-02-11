#!/bin/bash

echo "initializing airflow db ..."
airflow db init
airflow users create --username admin --password pwd --firstname Admin --lastname User --role Admin --email searaig@gmail.com

echo "starting airflow scheduler ..."
airflow scheduler & $SCHEDULER_PID

echo "starting airflow webserver ..."
airflow webserver

wait $SCHEDULER_PID

