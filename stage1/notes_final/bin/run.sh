#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:$portToUse --name notesfinal$portToUse \
    -e portToUse=$portToUse \
    -v $PWD/datavol:/notes/datavol \
    -d dsanders/notesfinal /bin/bash -c '/notes/startup.sh ${portToUse}'
