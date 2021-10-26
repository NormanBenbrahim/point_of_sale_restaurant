#!/bin/bash

### start tests on the api
docker-compose exec api py.test app/tests

### test coverage
docker-compose exec api py.test --cov-report term-missing app

### linting
echo "flake8 linting:"
#docker-compose exec api flake8 .