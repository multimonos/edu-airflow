#!/usr/bin/env bash

pgrep nginx && valet stop

pgrep java && brew services stop zookeeper  && brew services stop kafka

docker compose up 
