
# debian image

FROM apache/airflow:2.7.2-python3.10

ENV AIRFLOW_HOME=/home/airflow
WORKDIR $AIRFLOW_HOME

RUN pip install --no-cache-dir apache-airflow-providers-sqlite

COPY ./docker/profile /home/airflow/.bash_profile

COPY --chown=airflow:airflow ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#EXPOSE 8080 

ENTRYPOINT ["/entrypoint.sh"]
