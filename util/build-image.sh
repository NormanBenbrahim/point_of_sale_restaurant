#!/bin/bash

PROJECT_ID=$(gcloud config get-value project)

gcloud artifacts repositories create point-of-sale-api --repository-format=docker \
--location=northamerica-northeast2 
--description="Docker repo for the point of sale api for restaurant menus"

gcloud builds submit \
--tag northamerica-northeast2-docker.pkg.dev/point-of-sale-329816/point-of-sale-api/point-image:tag1