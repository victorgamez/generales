#!/bin/bash
#file=backup_data_siboy
file="$1"
#what2backup="/home/tania/CIDSIBOY_V1/CID/FicherosRAW/"
what2backup="$2"
excl="$3"
fichsalida=$file\_`hostname`\_`/usr/local/bin/hoy`
echo $fichsalida
exit 0
if [ "$3" == "" ]; then
	tar cvzf $fichsalida.tar.gz $what2backup
else
	tar cvzf $fichsalida.tar.gz $what2backup --exclude $excl
fi	
