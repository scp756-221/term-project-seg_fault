#!/usr/bin/env bash
docker container run --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=a46554ebb03344aa7be0a794f8cdde78-213372141.us-west-2.elb.amazonaws.com \
  -e USERS=$1 \
  -e SIM_NAME=ReadPlaylistSim \
  --label gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.ReadPlaylistSim