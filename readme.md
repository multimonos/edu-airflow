# Airflow dev
Starting point for airflow dev with services,
- airflow
- minio

## Airflow 
- webui http://localhost:8080

## Minio
s3 bucket replacement for onprem
- webui http://127.0.0.1:9001/
- api http://127.0.0.1:9000/

### Notes
- files must be uploaded via api/ui 

## Mysql Airflow Connector
Check mysql running in localhost
- `which mysql` -> `/opt/homebrew/bin/mysql`
- `lsof -i :3306` -> show lines with mysqld
- check conn with `mysql -uroot -p`

Check connection from container -> localhost,
```
Given i have mysql running on mac os x
  And airflow is running in container
  And logged into airflow container
  And `mysql -h host.docker.internal -u -p` was run 
  And connection was successful
When `show databases` is run
Then should see all my development databases
```
    
NOTE: `host.docker.internal` is alias for my machine's `localhost`


