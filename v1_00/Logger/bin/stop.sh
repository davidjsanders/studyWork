#!/bin/bash
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo -n "Stopping container $portToUse >> "
docker kill stage2_logger$portToUse
echo -n "Removing name "
docker rm -f stage2_logger$portToUse
