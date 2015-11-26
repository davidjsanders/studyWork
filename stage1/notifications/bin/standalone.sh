#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:80 -P --name notesuwsgi$portToUse \
    -v ~/Documents/studyWork/stage1/notesuwsgi/datavol:/datavol \
    -i -t dsanders/notesuwsgi /bin/bash
