#!/bin/bash
persist_dir=''
container_name=$(date +%d%m%Y%H%M%S)""
if ! [[ -z $1  ]]; then
    echo -n "Persisting data to: "
    persist_dir='-v '${1}'/datavolume:/Context/datavolume'
    echo ""$persist_dir
fi
echo "Running contianer: context_$container_name "
docker run -p 5000:5000 $persist_dir \
    --name "context_$container_name" \
    -it dsanderscan/mscit_v1_00_context
echo -n "Stopping contianer: context_$container_name = "
docker stop "context_$container_name"
echo -n "Removing contianer: context_$container_name = "
docker rm "context_$container_name"

