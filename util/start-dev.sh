#!/bin/bash

# deletes and re-builds each time to emulate prod as much as possible
docker-compose rm -f
docker-compose up --build