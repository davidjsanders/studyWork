#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:$portToUse --name geoapp$portToUse \
    --net=isolated_nw \
    -e portToUse=$portToUse \
    -e serverName='dasanderUty01' \
    -v $PWD/datavol:/geoapp/datavol \
    -d dsanders/geoapp /bin/bash -c /geoapp/startup.sh \
