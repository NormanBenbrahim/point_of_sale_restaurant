#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible
docker-compose rm -f
docker-compose down 
docker-compose build --no-cache
docker-compose up 