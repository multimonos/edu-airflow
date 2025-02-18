#!/usr/bin/env bash

pgrep nginx && valet stop # free up :9000

#grep java && brew services stop zookeeper  && brew services stop kafka

docker compose up 
