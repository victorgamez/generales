#!/bin/bash
if [ "$1" != "" ]; then
  while myExit=$(inotifywait -e open $1); do
    myFile=${myExit#?*OPEN }
    if [ $(echo $myFile | grep -i ".txt$") ]; then
    #echo "Ejecutar script trata_data $myFile"
       /usr/local/share/observadir/formatjabber.py javiprmes,tania "Fichero $myFile actualizado"
    fi
  done
else
    echo "Pon algun parametro,hombre.Del tipo \"$0 dir\""
fi
