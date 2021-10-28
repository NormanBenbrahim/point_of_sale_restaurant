#!/bin/bash

#### cleanup docker images, best to run this once a week or so
DANGLING_IMGS=$(docker images -qf dangling=true)

if [ ! "$DANGLING_IMGS" ]; then 
    echo "Dev is clean"
else
    docker rmi -f $(docker images -qf dangling=true)
    echo "Dev is clean"
fi