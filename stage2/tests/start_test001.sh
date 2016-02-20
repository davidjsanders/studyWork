#!/bin/bash
#References
# http://stackoverflow.com/questions/2924697/how-does-one-output-bold-text-in-bash

#set -o verbose
export loggerPort=100
export notesvcPort=101
export bluePort=102
export monitorPort=103
export locPort=104
export phonePort=1080
export serverName=`hostname`
export serverIP="`ifconfig eth0 2>/dev/null|awk '/inet addr:/ {print $2}'|sed 's/addr://'`"
export serverIPName="http://"$serverIP
export phoneKey='"key":"NS1234-5678-9012-3456"'
export genKey='"key":"1234-5678-9012-3456"'
export test_pause="0.5"
export bold=$(tput rev)
export underline=$(tput smul)
export normal=$(tput sgr0)

function pre_test {
    echo ""
    echo "${underline}Test $1: ${2}${normal}"
    echo $(date)
}

function post_test {
    echo
    echo
    sleep $test_pause
}

function do_post {
    # $1 - data string
    # $2 - portNumber
    # $3 - URL
    # $4 - Heading
    # $5 - Test Number
    pre_test $5 "${4}"
    curl -X POST \
        -d "${1}" \
        $serverName:$2$3
    post_test
}

function do_put {
    # $1 - data string
    # $2 - portNumber
    # $3 - URL
    # $4 - Heading
    # $5 - Test Number
    pre_test $5 "${4}"
    curl -X PUT \
        -d "${1}" \
        $serverName:$2$3
    post_test
}

function do_delete {
    # $1 - data string
    # $2 - portNumber
    # $3 - URL
    # $4 - Heading
    # $5 - Test Number
    pre_test $5 "${4}"
    curl -X DELETE \
        -d "${1}" \
        $serverName:$2$3
    post_test
}

function do_get {
    # $1 - data string
    # $2 - portNumber
    # $3 - URL
    # $4 - Heading
    # $5 - Test Number

    pre_test $5 "${4}"
    curl -X GET \
        -d "${1}" \
        $serverName:$2$3
    post_test
}

function start_phone {
    echo "Add "${1}" as a phone screen viewer. NOTE; output will not be available UNTIL phone shuts down"
    PhoneScreen/Phone_Screen.py --server $serverIP --port 16379 > "${1}".txt &
    echo ""
}

test_id=0

echo $(tput clear)
echo 
echo "${bold}Starting tests at "$(date)"                                          ${normal}"
echo ""

# Setup Jing to be able to see the phone
((test_id++))
start_phone Jing

# Setup Bob to be able to see the phone
((test_id++))
start_phone Bob

# Send an SMS Message to the phone
((test_id++))
export data='{'$phoneKey', "sender":"SMS", "message":"This is a text message received via SMS", "action":"open"}'
do_post "${data}" \
         $phonePort \
         "/v1_00/notification" \
         "Send an SMS Message to the phone" \
         $test_id

# Connect to Monitor App
((test_id++))
export monitor_app='"monitor-app":"'$serverIPName':'$monitorPort'/v1_00"'
export service='"notification-service":"'$serverIPName':'$notesvcPort'/v1_00/notification"'
export recipient='"recipient":"'$serverIPName':'$phonePort'/v1_00/notification"'
export location='"location-service":"'$serverIPName':'$locPort'/v1_00/check"'
export provider='"location-provider":"'$serverIPName':'$phonePort'/v1_00/location"'
export data='{'$genKey', '$monitor_app', '$service', '$recipient', '$location', '$provider'}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/monitor" \
        "Connect to Monitor App. " \
        $test_id

# Configure Grindr as a monitored application
((test_id++))
export data='{'$genKey', "description":"Grindr is an app for men seeking men"}'
do_post "${data}" \
        $monitorPort \
        "/v1_00/app/grindr" \
        "Configure Grindr as a monitored application" \
        $test_id

# Validate Grindr is being monitored
((test_id++))
export data='{'$genKey'}'
do_get "${data}" \
       $monitorPort \
       "/v1_00/app/grindr" \
       "Validate Grindr is being monitored" \
        $test_id

# Configure ManHunt as a monitored application
((test_id++))
export data='{'$genKey', "description":"ManHunt is a location based app for men seeking men"}'
do_post "${data}" \
        $monitorPort \
        "/v1_00/app/manhunt" \
        "Configure ManHunt as a monitored application" \
        $test_id

# Launch the Facebook client - A Notification will NOT be issued
((test_id++))
export data='{'$genKey'}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/launch/facebook" \
        "Launch the Facebook client - A Notification will NOT be issued" \
        $test_id

# Launch Grindr - A Notification will be issued
((test_id++))
export data='{'$genKey'}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/launch/grindr" \
        "Launch Grindr - A Notification will be issued" \
        $test_id

# Launch the phone mail client - A Notification will NOT be issued
((test_id++))
export data='{'$genKey'}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/launch/mailclient" \
        "Launch the phone mail client - A Notification will NOT be issued" \
        $test_id

# Send a text message to the phone
((test_id++))
export data='{'$phoneKey', "sender":"SMS", "message":"Can you pick me up at Starbucks, please? Its the one at Clair and Gordon. Thanks John.", "action":"open"}'
do_post "${data}" \
        $phonePort \
        "/v1_00/notification" \
        "Send a text message to the phone" \
        $test_id

# Stop monitoring Grindr
((test_id++))
export data='{'$genKey'}'
do_delete "${data}" \
          $monitorPort \
          "/v1_00/app/grindr" \
          "Stop monitoring Grindr" \
          $test_id

# Validate Grindr is no longer being monitored
((test_id++))
export data='{'$genKey'}'
do_get "${data}" \
       $monitorPort \
       "/v1_00/app/grindr" \
       "Validate Grindr is no longer being monitored. Monitor_App returns 404" \
        $test_id

# Launch Grindr - A Notification will NOT be issued
((test_id++))
export data='{'$genKey'}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/launch/grindr" \
        "Launch Grindr - A Notification will NOT be issued" \
        $test_id

# Define a location hot spot called downtown from 50,50 to 200,200
((test_id++))
export data='{'$genKey', "description":"The downtown hotspot", "lower-x":50, "lower-y":50, "upper-x":200, "upper-y":200}'
do_post "${data}" \
        $locPort \
        "/v1_00/config/hotspot/downtown" \
        "Define a location hot spot called downtown from 50,50 to 200,200" \
        $test_id

# Validate the hotspot downtown has been created
((test_id++))
export data='{'$genKey'}'
do_get "${data}" \
       $locPort \
       "/v1_00/config/hotspot/downtown" \
       "Validate the hotspot downtown has been created" \
        $test_id

# Set the phone current location to 100,100
((test_id++))
export data='{'$genKey', "x":100, "y":100}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/location" \
        "Set the phone current location to 100,100 (Notifications WILL be raised)" \
        $test_id

# Pause for 1 minute
echo "The phone will detect the location at the next timer check (every 30 seconds)"
echo "So sleep for 1 minute before setting the location out of a hotspot"
sleep 60

echo ""
# Set the phone current location to 1000,100
((test_id++))
export data='{'$genKey', "x":1000, "y":100}'
do_post "${data}" \
        $phonePort \
        "/v1_00/config/location" \
        "Set the phone current location to 1000,100 (Notifications WILL NOT be raised)" \
        $test_id

# Disconnect the Monitor App
((test_id++))
export data='{'$genKey'}'
do_delete "${data}" \
           $phonePort \
           "/v1_00/config/monitor" \
           "Connect to Monitor App. " \
           $test_id

echo ""
echo "${bold}Tests completed at "$(date)".                                          ${normal}"
echo 
echo 

