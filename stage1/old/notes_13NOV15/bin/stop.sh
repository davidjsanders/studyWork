#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Stopping container $portToUse >> "
docker kill notes_13nov15$portToUse
echo -n "Removing name "
docker rm -f notes_13nov15$portToUse
