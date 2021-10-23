#!/bin/bash

#### cleanup docker images, best to run this once a week or so
docker rmi -f $(docker images -qf dangling=true)