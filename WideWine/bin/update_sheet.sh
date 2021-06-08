#!/bin/bash
BIN=/opt/googleapis/bin
PYTHON_BIN=/usr/local/bin/python3.7
TARGET_ZONE=`/usr/bin/curl -s "http://169.254.169.254/latest/meta-data/placement/availability-zone"`
if [ $TARGET_ZONE == "ap-southeast-1a" ]
then
        $PYTHON_BIN $BIN/update_sheet_1.py --noauth_local_webserver
elif [ $TARGET_ZONE == "ap-southeast-1b" ]
then
        $PYTHON_BIN $BIN/update_sheet_2.py --noauth_local_webserver
else
        echo "WRONG ZONE INFO"
fi
