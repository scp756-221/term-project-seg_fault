#!/usr/bin/env bash
docker container run --rm \
  -v ${PWD}/gatling/results:/opt/gatling/results \
  -v ${PWD}/gatling:/opt/gatling/user-files \
  -v ${PWD}/gatling/target:/opt/gatling/target \
  -e CLUSTER_IP=a877253f7233e49709d2f46080c8856d-1381043525.us-west-2.elb.amazonaws.com \
  -e USERS=10 \
  -e SIM_NAME=ReadUserSim \
  --label gatling \
  ghcr.io/scp-2021-jan-cmpt-756/gatling:3.4.2 \
  -s proj756.ReadUserSim