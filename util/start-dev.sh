#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible
# add a command line argument (anything, really) to keep a cache. useful for testing
echo "Cleaning previous instance"
docker-compose rm -f
docker-compose down 

# if no command line args, build from scratch
if [ $# -eq 0 ]; then 
    echo "No command line argument given, building from scratch"
    
    # unlink everything
    echo "Unlinking everything"
    docker system prune -f
    docker image prune -f
    docker volume prune -f
    
    # collect all images
    IMAGES=$(docker images | awk '{print $3}' | grep -v ID)

    # if images present remove them
    for img in $IMAGES
    do 
        if [ $img = "IMAGE" ]; then 
            echo ""
        elif [ $img = "" ]; then
            echo ""
        else 
            echo "Removing image $img"
            docker rmi $img
        fi
    done

    # build everything
    echo "Building & launching container"
    docker-compose build --no-cache
    docker-compose up 
else
    # build from cache
    echo "Command line argument given, building from cache & launching container"
    docker-compose build
    docker-compose up
fi