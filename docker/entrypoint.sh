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

echo "creating mysql connector 'dev_mysql' ..."
 airflow connections add 'devmysql' \
     --conn-type 'mysql' \
     --conn-host 'host.docker.internal' \
     --conn-login 'devmysql' \
     --conn-password 'pwd' \
     --conn-schema 'devmysql' \
     --conn-port '3306'



echo "wait wait ..."
wait $SCHEDULER_PID

