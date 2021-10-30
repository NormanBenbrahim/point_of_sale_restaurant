#!/bin/bash

if [ -f .env ]; then
    # load .env variables
    export $(cat .env | grep -v '#' | awk '/=/ {print $1}')

    # add dev variable
    export FLASK_ENV="development"
    
    # run the app
    workers="4"
    echo "Running app with $workers workers"
    echo ""
    gunicorn -w $workers -b 0.0.0.0:8000 --access-logfile - "app.api:create_app()"
fi