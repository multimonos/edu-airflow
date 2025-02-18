#!/usr/bin/env bash

echo 'minio-client : useful commands,'
echo '  mc ls local/airflow-dev'
echo '  mc cp path/to/src/file local/airflow-dev'


docker exec -it minio-client /bin/sh
