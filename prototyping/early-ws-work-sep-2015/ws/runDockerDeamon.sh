#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting service on port $portToUse"
docker run -p $portToUse:5000 -P -d dsanders/phonews /bin/bash -c "/phonews/phoneWS.py"
