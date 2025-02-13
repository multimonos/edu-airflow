# debian
FROM apache/airflow:2.7.2-python3.10

# --- system:root ---
USER root

RUN apt-get update \
    && apt-get install -y tree procps vim \
    && rm -rf /var/lib/apt/lists/*


# --- airflow:airflow ---
USER airflow


ENV AIRFLOW_HOME=/home/airflow
WORKDIR $AIRFLOW_HOME

RUN pip install --upgrade pip \
    && pip install --no-cache-dir apache-airflow-providers-sqlite  apache-airflow-providers-mysql 


COPY ./docker/profile /home/airflow/.bash_profile

COPY --chown=airflow:airflow ./docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

#EXPOSE 8080 

ENTRYPOINT ["/entrypoint.sh"]
