#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Starting port $portToUse >> "
docker run -p $portToUse:80 -P --name notesfinal$portToUse \
    -v ~/Documents/studyWork/stage1/notes_final/datavol:/datavol \
    -i -t dsanders/notesfinal /bin/bash
