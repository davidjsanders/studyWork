#!/bin/bash
portToUse=$1
serverName=$2
echo "Host is ${hostname}"
if [ "$1x" == "x" ]; then portToUse='5000'; echo "Defaulting to port: $portToUse"; fi
if [ "$2x" == "x" ]; then serverName=`hostname`; echo "Defaulting to server name: $serverName"; fi
echo ""
echo -n "Starting port $portToUse with server name $serverName>> "
#
# Environment Variables passed to container
# -----------------------------------------
# portToUse: the port NGINX is to listen on.
# serverName: the name of the server, rather than localhost
# TZ: the timezone setting. Taken from the container host
#
docker run -p $portToUse:$portToUse --name stage2_logger$portToUse \
    --net=isolated_nw \
    -e portToUse=$portToUse \
    -e serverName="$serverName" \
    -e TZ=`date +%Z` \
    -v $PWD/datavolume:/Logger/datavolume \
    -d dsanders/stage2_logger /bin/bash -c /Logger/startup.sh \
