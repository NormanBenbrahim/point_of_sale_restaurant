#!/bin/bash

# deletes and re-builds each time to emulate production builds as much as possible
docker-compose rm -f
docker-compose down 
docker-compose build --no-cache
docker-compose up 