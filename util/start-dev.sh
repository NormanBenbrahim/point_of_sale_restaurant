#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible

# add a command line argument (anything, really) to keep a cache. useful for testing
docker-compose rm -f
docker-compose down 

if [ $# -eq 0 ]; then 
    # unlink everything
    docker system prune -f
    docker image prune -f
    docker volume prune -f
    
    # delete images, add utility to grep and remove by id later
    docker rmi point_of_sale_restaurant_api
    docker rmi python
    docker rmi postgres

    # build everything
    docker-compose build --no-cache
    docker-compose up 
else
    docker-compose build
    docker-compose up
fi