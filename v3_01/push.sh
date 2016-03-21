echo ""
echo "Pushing Monitor App"
cd Monitor_App
bin/push.sh
echo ""
echo "Pushing Phone"
cd ../Phone
bin/push.sh
echo ""
cd ..

