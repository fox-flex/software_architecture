#!/bin/bash
set -e

clear
docker-compose down
docker-compose build
# docker-compose build --no-cache
docker-compose -f docker-compose.yml up
