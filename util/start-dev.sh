#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible

# add a command line argument (anything, really) to keep a cache. useful for testing
docker-compose rm -f
docker-compose down 

if [ $# -eq 0 ]; then 
    #docker rm -f $(docker ps -a -q)
    docker system prune -f
    docker image prune -f
    docker volume prune -f
    
    # docker rmi {image id}

    # add utility to delete volumes, images & containers with grep
    docker-compose build --no-cache
    docker-compose up 
else
    docker-compose build
    docker-compose up
fi