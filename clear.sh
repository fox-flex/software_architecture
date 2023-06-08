#!/bin/bash

# docker-compose down
docker network prune -y
docker rm -f $(docker ps -a -q)
clear
