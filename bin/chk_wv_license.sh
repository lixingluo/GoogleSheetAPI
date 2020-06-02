#!/bin/bash
cd /opt/tomcat/logs
_date=$1
_filename="license_proxy."$_date".log"

_total=$(grep "\[*\]\ for\ CIO" "$_filename" | wc -l)
_super=$(grep "\[super\]\ for\ CIO" "$_filename" | wc -l)
_mytv=$(grep "\[mytv\]\ for\ CIO" "$_filename" | wc -l)
_null=$(grep "\[null\]\ for\ CIO" "$_filename" | wc -l)

_error=$(grep "PHP\ Error" "$_filename" | wc -l)

echo $_total
echo $_super
echo $_mytv
echo $_null
echo $_error
