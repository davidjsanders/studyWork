limit=$1
if [ $1"x" == "x" ]; then limit="10"; fi 
i="0"

while [ $i -lt $limit ]
do
    port="50"
    if [ $i -lt "10" ]; then port="500"; fi
    bin/stop.sh $port$i
    i=$[$i+1]
done
