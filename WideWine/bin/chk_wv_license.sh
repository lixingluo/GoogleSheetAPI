#!/bin/bash
cd /var/log/tomcat8
_date=$1
_filename="localhost_access_log."$_date".txt"

_total=$(grep "POST" "$_filename" | grep "contentid=" | grep "\" 200" | wc -l)

echo $_total
