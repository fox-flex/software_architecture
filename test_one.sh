#!/bin/bash
set -e

curl -d "{\"text\":\"fox flex\"}" -H "Content-Type: application/json" -X POST http://localhost:8000/
echo
curl http://localhost:8000/
