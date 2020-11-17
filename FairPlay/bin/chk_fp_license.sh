#!/bin/bash
cd /var/log/httpd
_date=$1
_filename="access_log-"$_date

_total=$(grep "POST" "$_filename" | grep "fps/ksm" | grep "\" 200" | wc -l)

echo $_total
