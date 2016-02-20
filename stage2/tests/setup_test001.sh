export loggerPort=100
export notesvcPort=101
export bluePort=102
export monitorPort=103
export locPort=104
export phonePort=1080
export serverName="dasanderUty01"
export serverIPName="192.168.0.210"

function config_logging {
    # $1 - Port number
    # $2 - Container image name
    export loggerURL="http://"$serverIPName":"$loggerPort"/v1_00/log"
    export payload='{"key":"1234-5678-9012-3456","logger":"'$loggerURL'"}'
    echo "Configure $2 (port $1 on $serverName)"
    echo "Logging to central logger ($loggerURL)"
    echo -n "Result: "
    curl -X POST \
        -d $payload http://$serverName:$1/v1_00/config/logger
    sleep .5
    echo ""
    echo ""
}
function run_docker {
    # $1 - Port number
    # $2 - Container image name
    # $3 - Directory path
    echo -n "Starting service $2 (port $1 on $serverName): "
    docker run -p $1:$1 --name stage2_$2$1 \
        --net=isolated_nw -e portToUse=$1 -e serverName="$serverName" \
        -e TZ=`date +%Z` -v $PWD/$3/datavolume:/$3/datavolume \
        -d dsanders/stage2_$2 /bin/bash -c /$3/startup.sh
    sleep 1
}
function run_docker_phone {
    echo -n "Starting phone (port $phonePort on $serverName): "
    docker run -p 16379:6379 -p $phonePort:$phonePort \
        --name stage2_phone$phonePort \
        --net=isolated_nw \
        -e portToUse=$phonePort \
        -e serverName="$serverName" \
        -e TZ=`date +%Z` \
        -v $PWD/datavolume:/Phone/datavolume \
        -d dsanders/stage2_phone /bin/bash -c /Phone/startup.sh \
    sleep 1
}
echo " "
echo "Setting up variables"
echo " "
#
# Logger
#
echo "Starting services."
echo ""
run_docker $loggerPort "logger" "Logger"
sleep 1
echo -n "Clear existing logs: "
curl -X DELETE \
  -d '{"key":"1234-5678-9012-3456"}' http://$serverName:$loggerPort/v1_00/log
echo ""
echo ""
sleep 1
run_docker $bluePort "bluetooth" "Bluetooth"                   # Bluetooth
run_docker $locPort "location_service" "Location_Service"      # Location Service
run_docker $monitorPort "monitor_app" "Monitor_App"            # Monitor App
run_docker $notesvcPort "notification" "Notification_Service"  # Notification Service
run_docker_phone                                               # Start the phone
echo ""
echo -n "Pausing to let services complete start-up: "
sleep 2
echo "done."
echo ""
echo "Configure logging."
echo ""
config_logging $bluePort "Bluetooth"                 # Bluetooth
config_logging $locPort "Location Service"           # Location Service
config_logging $monitorPort "Monitor App"            # Monitor App
config_logging $notesvcPort "Notification Service"   # Notification Service
config_logging $phonePort "Phone"                    # Phone
echo ""
echo "Logging configured."
echo ""
echo "Done."