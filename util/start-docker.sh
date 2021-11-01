#!/bin/bash

# deletes and re-builds each time to emulate full production deployments as much as possible
# add a command line argument (anything, really) to keep a cache. useful for testing
docker-compose rm -f
docker-compose down 

# if no command line args, build from scratch
if [ $# -eq 0 ]; then
    echo ""
    echo "No command line argument given, building from scratch"
    echo "Cleaning previous instance"
    
    # unlink everything
    echo ""
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
        elif [ ! "$img" ]; then
            echo ""
        else
            echo "" 
            echo "Removing image $img"
            docker rmi $img
        fi
    done

    # build everything
    echo ""
    echo "Building & launching container from scratch"
    docker-compose build --no-cache
    docker-compose up 
else
    # build from cache
    echo ""
    echo "Command line argument given, building from cache & launching container"
    docker-compose build
    docker-compose up
fi