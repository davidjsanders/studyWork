#!/bin/bash
portToUse=$1
serverName=$2
echo "Host is ${hostname}"
if [ "$1x" == "x" ]; then portToUse='5000'; echo "Defaulting to port: $portToUse"; fi
if [ "$2x" == "x" ]; then serverName=`hostname`; echo "Defaulting to server name: $serverName"; fi
echo ""
echo -n "Starting port $portToUse with server name $serverName>> "
docker run -p $portToUse:$portToUse --name notifications$portToUse \
    --net=isolated_nw \
    -e portToUse=$portToUse \
    -e serverName="$serverName" \
    -v $PWD/datavol:/notifications/datavol \
    -d dsanders/notifications /bin/bash -c /notifications/startup.sh \
