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
export loggerURL="http://"$serverIPName":"$loggerPort"/v1_00/log"
export payload='{"key":"1234-5678-9012-3456","logger":"'$loggerURL'"}'
echo "Stopping services."
echo ""
echo -n "Stopping Bluetooth: "
docker kill stage2_bluetooth$bluePort
echo -n "Removing reserved name: "
docker rm -f stage2_bluetooth$bluePort
sleep 1
echo ""
echo -n "Stopping Location Service: "
docker kill stage2_location_service$locPort
echo -n "Removing reserved name: "
docker rm -f stage2_location_service$locPort
sleep 1
echo ""
echo -n "Stopping Logging Service: "
docker kill stage2_logger$loggerPort
echo -n "Removing reserved name: "
docker rm -f stage2_logger$loggerPort
sleep 1
echo ""
echo -n "Stopping Monitor App: "
docker kill stage2_monitor_app$monitorPort
echo -n "Removing reserved name: "
docker rm -f stage2_monitor_app$monitorPort
sleep 1
echo ""
echo "Services stopped."
echo ""
