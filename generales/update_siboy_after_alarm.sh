#!/bin/bash
# | sed -e 's/.*Fichero: //;s/ -.*//'

DATA=$(/usr/local/sbin/alarms.sh $@)
GETFILE=$(echo $DATA | sed -e 's/.*Fichero: //;s/ -.*//')
DIR=${GETFILE%/*}
FILE=${GETFILE##*/}
echo $DIR -- $FILE
cd /home/tania/CIDSIBOY_V1/CID/SIBOY && python manage.py runscript ingestVantage --script-args=$DIR/ $FILE
