#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting service on port $portToUse"
docker run -p $portToUse:5000 -P --name gendev -v datavol:/datavol -d dsanders/gendev /bin/bash -c /gendev/startup.sh

