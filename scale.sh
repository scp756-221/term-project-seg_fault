#!/usr/bin/env bash
eksctl scale nodegroup --name=worker-nodes --cluster aws756 --nodes 8 --nodes-max=8

kubectl -n c756ns scale deployment/cmpt756db --replicas=40
kubectl -n c756ns scale deployment/cmpt756s1 --replicas=10
kubectl -n c756ns scale deployment/cmpt756s2-v2 --replicas=10
kubectl -n c756ns scale deployment/cmpt756s3 --replicas=10

aws dynamodb update-table --table-name Music-eamonn-zh --provisioned-throughput ReadCapacityUnits=300,WriteCapacityUnits=300
aws dynamodb update-table --table-name User-eamonn-zh --provisioned-throughput ReadCapacityUnits=300,WriteCapacityUnits=300
aws dynamodb update-table --table-name Playlist-eamonn-zh --provisioned-throughput ReadCapacityUnits=300,WriteCapacityUnits=300