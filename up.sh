#!/usr/bin/env bash

pgrep nginx && valet stop

pgrep java && brew services stop zookeeper 

docker compose up 
