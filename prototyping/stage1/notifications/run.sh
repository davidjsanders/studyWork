#!/bin/bash
echo - n "Directory: "; pwd
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo "Starting service on port $portToUse"
docker run -p $portToUse:5000 -P --name notifications \
    -v /home/dasander/Documents/studyWork/prototyping/stage1/flaskTest/datavol:/datavol \
    -d dsanders/notifications /bin/bash -c /gendev/startup.sh

