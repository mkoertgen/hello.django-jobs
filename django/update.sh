#!/bin/bash -e
git pull
docker-compose pull
docker-compose up -d
