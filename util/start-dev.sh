#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible

# add a command line argument (anything, really) to keep a cache. useful for testing
# multiple changes & not having to rebuild each time
docker-compose rm -f
docker-compose down 

if [ $# -eq 0 ]; then 
    docker-compose build --no-cache
    docker-compose up 
else
    docker-compose build
    docker-compose up
fi