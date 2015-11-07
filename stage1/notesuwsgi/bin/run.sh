#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:5000 -p 4082:80 -P --name notesuwsgi$portToUse \
    -d dsanders/notesuwsgi /bin/bash -c /notes/startup.sh
#    -v /home/dasander/Documents/studyWork/prototyping/stage1/flaskTest/datavol:/datavol \

