#!/bin/bash
persist_dir=''
container_name=$(date +%d%m%Y%H%M%S)""
if ! [[ -z $1  ]]; then
    echo -n "Persisting data to: "
    persist_dir='-v '${1}'/datavolume:/Module/datavolume'
    echo ""$persist_dir
fi
echo "Running contianer: module_$container_name "
docker run -p 5000:5000 $persist_dir \
    --name "module_$container_name" \
    -it dsanderscan/mscit_v1_00_module
echo -n "Stopping contianer: module_$container_name = "
docker stop "module_$container_name"
echo -n "Removing contianer: module_$container_name = "
docker rm "module_$container_name"

