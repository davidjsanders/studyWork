export loggerPort=100
export notesvcPort=101
export bluePort=102
export monitorPort=103
export locPort=104
export phonePort=1080
export serverName="dasanderUty01"
export serverIPName="192.168.0.210"

function stop_service {
    # $1 - service port
    # $2 - service name
    echo -n "Stopping $2: "
    docker kill stage2_$2$1
    echo -n "Removing reserved name: "
    docker rm -f stage2_$2$1
    sleep 1
    echo ""
}

echo " "
echo "Stopping services."
echo ""
stop_service $phonePort "phone"
stop_service $bluePort "bluetooth"
stop_service $locPort "location_service"
stop_service $monitorPort "monitor_app"
stop_service $notesvcPort "notification"
stop_service $loggerPort "logger"
echo "Services stopped."
echo ""
echo "Done."
