echo ""
echo "Building Bluetooth"
cd Bluetooth
bin/build.sh
echo ""
echo "Building Location Service"
cd ../Location_Service
pwd
bin/build.sh
echo ""
echo "Building Logger"
cd ../Logger
bin/build.sh
echo ""
echo "Building LogViewer"
cd ../LogViewer
./build.sh
echo ""
echo "Building Monitor App"
cd ../Monitor_App
bin/build.sh
echo ""
echo "Building Notification Service"
cd ../Notification_Service
bin/build.sh
echo ""
echo "Building Phone"
cd ../Phone
bin/build.sh
echo ""
echo "Building Phone Screen"
cd ../Phone_Screen
./build.sh
cd ..

