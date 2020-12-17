#!/bin/sh

IP=$1

date=$(date +'%Y%m%d%H%M')
data=$(curl -s http://$IP/values | hxnormalize -x | hxselect 'td.r' -s ';' | w3m -dump -T 'text/html')

echo "$date;$data"
