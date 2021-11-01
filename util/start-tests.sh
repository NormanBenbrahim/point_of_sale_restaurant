#!/bin/bash

### start tests on the api
echo "Tests:"
docker-compose exec api py.test app/tests

### test coverage
echo ""
echo "Test coverage:"
docker-compose exec api py.test --cov-report term-missing app

### linting
echo ""
echo "flake8 linting:"
docker-compose exec api flake8 .