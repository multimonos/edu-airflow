#!/usr/bin/env bash

docker compose build

docker image prune -f # always remove old
