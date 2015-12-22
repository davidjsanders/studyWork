#!/bin/bash
ip=$(/sbin/ifconfig eth0 | grep "inet addr" | awk '{str=$2 ; print substr(str,6)}')
host=$(hostname)
echo "IP Address is $ip"
echo "Hostname is $host"
echo "Server to attach is $1"
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting Interpreter"
docker run -i -t  \
    -e ipaddr=$ip -e hostname=$host -e serverName="$1" \
    --net=isolated_nw \
    dsanders/microservice-interpreter /bin/bash -c bin/start.sh
#    dsanders/microservice-interpreter /interpreter/bin/startup.sh

