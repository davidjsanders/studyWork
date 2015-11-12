#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:$portToUse --name notes002$portToUse \
    -e portToUse=$portToUse \
    -v $PWD/datavol:/notes/datavol \
    -d dsanders/notes002 /bin/bash -c /notes/startup.sh
