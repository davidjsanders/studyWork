echo ""
echo "Pushing base"
cd base
bin/push.sh
echo ""
echo "Pushing Bluetooth"
cd ../Bluetooth
bin/push.sh
echo ""
echo "Pushing Location Service"
cd ../Location_Service
pwd
bin/push.sh
echo ""
echo "Pushing Logger"
cd ../Logger
bin/push.sh
echo ""
echo "Pushing LogViewer"
cd ../LogViewer
./build.sh
echo ""
echo "Pushing Monitor App"
cd ../Monitor_App
bin/push.sh
echo ""
echo "Pushing Notification Service"
cd ../Notification_Service
bin/push.sh
echo ""
echo "Pushing Phone"
cd ../Phone
bin/push.sh
echo ""
echo "Pushing Phone Screen"
cd ../Phone_Screen
./build.sh
cd ..

