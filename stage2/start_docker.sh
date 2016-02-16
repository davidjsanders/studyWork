export loggerPort=100
export notesvcPort=101
export bluePort=102
export monitorPort=103
export locPort=104
export phonePort=1080
export serverName="dasanderUty01"
export serverIPName="192.168.0.210"
echo " "
echo "Setting up variables"
echo " "
#
# Logger
#
echo "Starting services."
echo ""
echo -n "Logging Service (port $loggerPort on $serverName): "
docker run -p $loggerPort:$loggerPort --name stage2_logger$loggerPort \
    --net=isolated_nw -e portToUse=$loggerPort -e serverName="$serverName" \
    -e TZ=`date +%Z` -v $PWD/Logger/datavolume:/Logger/datavolume \
    -d dsanders/stage2_logger /bin/bash -c /Logger/startup.sh
sleep 1
echo ""
echo -n "Clear all logs: "
curl -X DELETE -d '{"key":"1234-5678-9012-3456"}' http://$serverName:$loggerPort/v1_00/log
echo ""
sleep 1
#
# Bluetooth
#
echo -n "Bluetooth (port $bluePort on $serverName): "
docker run -p $bluePort:$bluePort --name stage2_bluetooth$bluePort \
    --net=isolated_nw -e portToUse=$bluePort -e serverName="$serverName" \
    -e TZ=`date +%Z` -v $PWD/Bluetooth/datavolume:/Bluetooth/datavolume \
    -d dsanders/stage2_bluetooth /bin/bash -c /Bluetooth/startup.sh
sleep 1
#
# Location Service
#
echo -n "Location Service (port $locPort on $serverName): "
docker run -p $locPort:$locPort --name stage2_location_service$locPort \
    --net=isolated_nw -e portToUse=$locPort -e serverName="$serverName" \
    -e TZ=`date +%Z` -v $PWD/Location_Service/datavolume:/Location_Service/datavolume \
    -d dsanders/stage2_location_service /bin/bash -c /Location_Service/startup.sh
sleep 1
#
# Monitor App
#
echo -n "Monitor App (port $monitorPort on $serverName): "
docker run -p $monitorPort:$monitorPort --name stage2_monitor_app$monitorPort \
    --net=isolated_nw -e portToUse=$monitorPort -e serverName="$serverName" \
    -e TZ=`date +%Z` -v $PWD/Monitor_App/datavolume:/Monitor_App/datavolume \
    -d dsanders/stage2_monitor_app /bin/bash -c /Monitor_App/startup.sh
sleep 1
echo ""
echo "Services started."
echo ""
echo -n "Pausing to let services start: "
sleep 2
echo "done."
echo ""
echo "Configure logging."
echo ""
export loggerURL="http://"$serverIPName":"$loggerPort"/v1_00/log"
export payload='{"key":"1234-5678-9012-3456","logger":"'$loggerURL'"}'
echo "Configure logging to "$loggerURL
echo -n "Bluetooth: "
sleep .5
curl -X POST -d $payload http://$serverName:$bluePort/v1_00/config/logger
echo ""
echo -n "Location Service: "
sleep .5
curl -X POST -d $payload http://$serverName:$locPort/v1_00/config/logger
echo ""
echo -n "Monitor App: "
sleep .5
curl -X POST -d $payload http://$serverName:$monitorPort/v1_00/config/logger
echo ""
echo ""
echo "Logging configured."
echo ""

