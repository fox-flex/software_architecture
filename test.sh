#!/bin/bash

for i in {1..2}; do
    for v in {1..5}; do
        curl -d "{\"text\":\"fox flex ${v}\"}" -H "Content-Type: application/json" -X POST http://localhost:8000/
        echo
        sleep 0.5
    done
    curl http://localhost:8000/
    echo
    sleep 0.5
done

curl -d "{\"text\":\"fox flex\"}" -H "Content-Type: application/json" -X POST http://localhost:8000/
