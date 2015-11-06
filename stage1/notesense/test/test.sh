#
# Test Script
#
portToUse=$1
if [ "$1x" == "x" ]; then portToUse='5000'; fi
echo ""
echo "Clear notifications"
echo "==================="
echo ""
curl -X PUT localhost:$portToUse/clear
echo ""
echo "Test 1 - The device is running"
echo "------------------------------"
echo ""
curl localhost:$portToUse/
echo ""
echo "Test 2 - List all routes"
echo "------------------------"
echo ""
curl localhost:$portToUse/notifications
echo ""
echo "Test 3 - Post a notification"
echo "----------------------------"
echo ""
curl -X POST -H "Content-Type: application/json" -d '{"sensitivity":"high", "note":"**Remember** Safe Sex is Good Sex", "action":"msmapp geo(234.12,123.45)"}' localhost:$portToUse/notification
echo ""
echo "Test 4 - Post a notification"
echo "----------------------------"
echo ""
curl -X POST -H "Content-Type: application/json" -d '{"note":"This is just a notification", "action":"Do an action"}' localhost:$portToUse/notification
echo ""
echo "Test 5 - Get notification 0"
echo "---------------------------"
echo ""
curl localhost:$portToUse/notification/0
echo ""
echo "Test 6 - Get notification 1"
echo "---------------------------"
echo ""
curl localhost:$portToUse/notification/1
echo ""
echo "Test 7 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:$portToUse/notifications
echo ""
echo "Test 8 - List all possible actions"
echo "----------------------------------"
echo ""
curl localhost:$portToUse/
echo ""
echo "Test 9 - Get notification 0"
echo "---------------------------"
echo ""
curl localhost:$portToUse/notification/0
echo ""
echo "Test 10 - Update notification 0"
echo "-------------------------------"
echo ""
curl -X PUT -H "Content-Type: application/json" \
  -d '{"sensitivity":"normal", "note":"updated: This is just a notification"}' \
  localhost:$portToUse/notification/0
echo ""
echo "Test 11 - Get notification 0"
echo "----------------------------"
echo ""
curl localhost:$portToUse/notification/0
echo ""
echo "Test 12 - Lock Device"
echo "---------------------"
echo ""
curl -X PUT localhost:$portToUse/lock
echo ""
echo "Test 13 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:$portToUse/notifications
echo ""
echo "Test 14 - Unlock Device"
echo "-----------------------"
echo ""
curl -X PUT localhost:$portToUse/unlock/1234
echo ""
echo "Test 15 - List all notifications"
echo "-------------------------------"
echo ""
curl localhost:$portToUse/notifications
echo ""
echo "Test 16 - Bad update notification 0"
echo "-----------------------------------"
echo ""
curl -X PUT -H "Content-Type: application/json" -d '{"notes":"updated: This is just a notification"}' localhost:$portToUse/notification/0
echo ""
echo "Test 17 - Bad update notification 1"
echo "-----------------------------------"
echo ""
curl -X PUT -H "Content-Type: application/json" \
  -d '{"note":"This is the note", "notes":"updated: This is just a notification"}' \
  localhost:$portToUse/notification/0
echo ""
echo "Test 18 - Update non-existent notification"
echo "------------------------------------------"
echo ""
curl -X PUT -H "Content-Type: application/json" -d '{"note":"updated: This is just a notification"}' localhost:$portToUse/notification/20202
echo ""
