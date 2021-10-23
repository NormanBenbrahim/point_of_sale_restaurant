#!/bin/bash

##### build a kubernetes cluster on gcp

# ensure working in the right project
PROJECT_ID=$(gcloud config get-value project)


# create cluster, ubuntu preferred
gcloud beta container --project "$PROJECT_ID" clusters create "api" --zone \
"northamerica-northeast2-b" --no-enable-basic-auth \
--release-channel "regular" --machine-type "e2-medium" --image-type "UBUNTU" \
--disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true \
--scopes "https://www.googleapis.com/auth/devstorage.read_only",\
"https://www.googleapis.com/auth/logging.write",\
"https://www.googleapis.com/auth/monitoring",\
"https://www.googleapis.com/auth/servicecontrol",\
"https://www.googleapis.com/auth/service.management.readonly",\
"https://www.googleapis.com/auth/trace.append" --max-pods-per-node "110" --num-nodes "4" \
--logging=SYSTEM,WORKLOAD --monitoring=SYSTEM --enable-ip-alias \
--network "projects/$PROJECT_ID/global/networks/default" \
--subnetwork "projects/$PROJECT_ID/regions/northamerica-northeast2/subnetworks/default" \
--no-enable-intra-node-visibility --default-max-pods-per-node "110" --enable-autoscaling --min-nodes "0" \
--max-nodes "4" --no-enable-master-authorized-networks \
--addons HorizontalPodAutoscaling,HttpLoadBalancing,GcePersistentDiskCsiDriver \
--enable-autoupgrade --enable-autorepair --max-surge-upgrade 1 --max-unavailable-upgrade 0 \
--enable-shielded-nodes --node-locations "northamerica-northeast2-b"