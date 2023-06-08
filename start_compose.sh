#!/bin/bash
set -e

clear
docker compose down
docker compose -f docker-compose.yml up --build
