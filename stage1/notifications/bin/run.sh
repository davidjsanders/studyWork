#!/bin/bash
portToUse=$1
serverName=$2
if [ "$1x" == "x" ]; then portToUse='5000'; echo "Defaulting to port 5000"; fi
if [ "$2x" == "x" ]; then serverName='localhost'; echo "Defaulting to localhost"; fi
echo ""
echo -n "Starting port $portToUse with server name $serverName>> "
docker run -p $portToUse:$portToUse --name notifications$portToUse \
    --net=isolated_nw \
    -e portToUse=$portToUse \
    -e serverName="$serverName" \
    -v $PWD/datavol:/notifications/datavol \
    -d dsanders/notifications /bin/bash -c /notifications/startup.sh \
