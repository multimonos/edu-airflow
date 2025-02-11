
# debian

FROM apache/airflow:2.7.2-python3.10

ENV AIRFLOW_HOME=/opt/airflow
WORKDIR $AIRFLOW_HOME

RUN pip install --no-cache-dir apache-airflow-providers-sqlite

COPY src/profile /home/airflow/.bash_profile
COPY dags/ dags/
COPY --chown=airflow:airflow src/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#EXPOSE 8080 

ENTRYPOINT ["/entrypoint.sh"]
