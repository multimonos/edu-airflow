#!/bin/bash

echo "initializing airflow db ..."
airflow db init

echo "airflow : creating user 'airflow' ..."
airflow users create \
    --username admin \
    --password pwd \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email searaig@gmail.com

echo "airflow : starting scheduler ..."
airflow scheduler & $SCHEDULER_PID

echo "airflow : starting webserver ..."
airflow webserver & $WEBSERVER_PID

echo "airflow : creating mysql connection 'devmysql' ..."
 airflow connections add 'devmysql' \
     --conn-type 'mysql' \
     --conn-host 'host.docker.internal' \
     --conn-login 'devmysql' \
     --conn-password 'pwd' \
     --conn-schema 'devmysql' \
     --conn-port '3306'

echo "minio : creating airflow connection devminio ..." 
 airflow connections add 'devminio' \
     --conn-type 'aws' \
     --conn-login 'minioadmin' \
     --conn-password 'minioadmin' \
     --conn-extra '{ "endpoint_url":"http://host.docker.internal:9000" }'

echo "wait wait ..."
wait $SCHEDULER_PID

