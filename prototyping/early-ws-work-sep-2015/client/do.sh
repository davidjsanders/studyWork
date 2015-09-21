#!/bin/bash
date > $1.log
echo "=================================" >> $1.log
echo "" >> $1.log
./app.py http://localhost:$1/ >> $1.log &> $1.log
echo "" >> $1.log
echo "=================================" >> $1.log
date >> $1.log
echo "" >> $1.log
echo "" >> $1.log
cat $1.log | more
