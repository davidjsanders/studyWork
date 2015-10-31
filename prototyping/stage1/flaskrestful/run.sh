#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting service on port $portToUse"
docker run -p $portToUse:5000 -P --name flaskrestful -v datavol:/datavol -d dsanders/flaskrestful /bin/bash -c /gendev/startup.sh

