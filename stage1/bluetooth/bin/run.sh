#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:$portToUse --name bluetooth$portToUse \
    --net=isolated_nw \
    -e portToUse=$portToUse \
    -e serverName='dasanderUty01' \
    -v $PWD/datavol:/bluetooth/datavol \
    -d dsanders/bluetooth /bin/bash -c /bluetooth/startup.sh \
