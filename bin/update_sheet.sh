#!/bin/bash
BIN=/opt/googleapis/bin
PYTHON_BIN=/usr/local/bin/python3.6
YESTERDAY_DATE=`date -d yesterday "+%F"`
echo $YESTERDAY_DATE | $PYTHON_BIN $BIN/update_sheet.py --noauth_local_webserver

