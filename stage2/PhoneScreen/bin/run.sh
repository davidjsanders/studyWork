#!/bin/bash
echo ""
echo "Command: bin/run.sh servername redis_port"
echo ""
ip=$(/sbin/ifconfig eth0 | grep "inet addr" | awk '{str=$2 ; print substr(str,6)}')
host=$(hostname)
echo "Server to attach is $1"
echo "Redis port is $2"
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting Phone Screen"
docker run -i -t  \
    -e redis_port=$2 -e hostname=$host -e serverName="$1" \
    --net=isolated_nw \
    dsanders/stage2_phone_screen /bin/bash \
    -c "/flask/bin/python3 /Phone_Screen/Phone_Screen.py"

