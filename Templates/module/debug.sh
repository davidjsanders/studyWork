#!/bin/bash
persist_dir=''
container_name=$(date +%d%m%Y%H%M%S)""
save_param=''
server_name='-e serverName=localhost'
port='5000'
port_param='-e portNumber='$port''
version='v1_00'
version_param='-e version='$version
let error_occurred=0
#
# Usage instructions
#
usage()
{
    echo "Usage: $0 [-p >1023] [-s /absolute/path] [-n service-name] [-h]" 1>&2
    echo
    echo "  -p [number]  Specify the port number to use. Must be higher than 1023"
    echo "  -s [path]    Specify the path to persist the data volume to."
    echo "  -n [string]  Specify the name the service should use for its url"
    echo "  -v [version] Specify the version of the service to be used"
    echo "  -h           Show this help message."
    echo
    exit 1; 
}

while getopts "s:hp:n:v:" param; do
    case "$param" in
        s) save_param="-v "$OPTARG"/datavolume:/Module/datavolume"
           ;;
        p) port=$OPTARG
           if ! [[ $port =~ $number_expression ]]; then
               not_allowed="invalid option: port must be a number!"
               let error_occurred=1
               break
           fi
           let port_number=${port}
           if (("${port_number}" < "1024")); then
               not_allowed="invalid option: start port must be higher than 1023"
               let error_occurred=1
               break
           fi
           port_param='-e portToUse='$port_number''
           ;;
        v) version=$OPTARG
           version_param='-e version='$OPTARG
           ;;
        n) server_name='-e serverName='$OPTARG
           ;;
        h) usage
           ;;
        *) not_allowed="invalid option: -"$OPTARG
           let error_occurred=1
           break
           ;;
    esac
done
if [ "$error_occurred" -eq "1" ]; then
    echo "${0}: ${not_allowed}"
    echo
    usage
fi

echo "Persistenc option: "$save_param
echo "Port being used:   "$port
echo ""
if ! [[ -z '${save_param}' ]]; then
    echo "Persisting with option: "$save_param
fi

echo "Running contianer: module_$container_name "
docker run \
    -p $port:$port \
    --name "module_$container_name" \
    ${port_param} \
    ${save_param} \
    ${server_name} \
    ${version_param} \
    -it "dsanderscan/mscit_"$version"_module"
echo -n "Stopping contianer: module_$container_name = "
docker stop "module_$container_name"
echo -n "Removing contianer: module_$container_name = "
docker rm "module_$container_name"

