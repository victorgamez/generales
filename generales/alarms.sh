#!/bin/bash
function CheckParameters()
{
	if [ ${#BASH_ARGV[@]} -eq 4 ]; then
	# Read parameters or file with parameters
		if [ ! -d ${BASH_ARGV[2]} ]; then
			echo Dir ${BASH_ARGV[1]} doesn\'t exist
			exit -1
		fi
		RECIPIENTS=${BASH_ARGV[0]}
		FILE2CHECK=${BASH_ARGV[1]}
		DIR2CHECK=${BASH_ARGV[2]}
		STATIONNAME=${BASH_ARGV[3]}
	else
		echo Please specify path to check, or configfile
		exit -1
	fi
		
}
# ############################################ #
# ########## CheckTimestamp ################## #
# More than ### SPECIFIED TIME ###?Then alarm  #
# ############################################ #
function CheckTimestamp()
{
  # Get timestamp for newest modified file in directory specified by $1
  # INFO=GET FILENAME##MDATE LINUX FORMAT(SCNDS FROM 01011970)##MDATE(HUMAN FORMAT)
	# FILENAME: [[:alfnum:]]+(\.[[:alfnum:]]+)?
        # MDATE LINUX: longint
        # MDATE HUMAN: 2014-07-18 11:56:05.000000000 +0100 
  #INFO="ls -1r $DIR2CHECK| grep $FILE2CHECK | head -1 | xargs stat -c %n##%Y##%y"
  #INFO=$(ls -1r \"$DIR2CHECK\" | grep \"$FILE2CHECK\" | head -1 | sed 's#.\*#$DIR2CHECK/\&#gi' | xargs stat -c %n##%Y##%y)
  INFO=$(ls -1r "$DIR2CHECK" | grep "$FILE2CHECK" | head -1 | sed 's#.*#'$DIR2CHECK'&#gi' | xargs stat -c %n##%Y##%y)
  ## Split data
  # MDATE LINUX FORMAT
  TIMESTAMP=${INFO#*##}
  TIMESTAMP=${TIMESTAMP%##*}
  ## MDATE (HUMAN FORMAT)
  HUMANTIMESTAMP=${INFO##*##}
  ## FILENAME
  FILENAME=${INFO%%##*}
  ##
  # Substract to calculate file last update respect from current date
  DIFFTIME=$(($CURRENT-$TIMESTAMP))
  STATEREPORT="Estacion: $STATIONNAME - Fichero: $FILENAME - Fecha: $HUMANTIMESTAMP - Estado: "
  #echo $DIFFTIME,$ALARMUPAT
  if [[ $DIFFTIME -ge $ALARMUPAT ]]; then 
	STATEREPORT="$STATEREPORT ** DESACTUALIZADO **"
  else
	STATEREPORT="$STATEREPORT Actualizado "
  fi
  #echo $DIFFTIME
  # Check if difference is less than ### SPECIFIED TIME ###
  [[ $DIFFTIME -ge $ALARMUPAT && $DIFFTIME -le $ALARMUPLIMIT ]] && { 
#   [[ $DIFFTIME -ge $ALARMUPAT ]] && { 
	echo FICHERO $FILENAME DESACTUALIZADO:$DIFFTIME SEGUNDOS
	SendEmail 
  }
  
}

# ############################################ #
# ############### SendEmail ################## #
# Send email to recipient(s)                   #
# $1: recipients{,recipients}*		       #
# ############################################ #
function SendEmail()
{
  echo """
Estimado usuario:

Este es un correo automatico enviado por PLOCAN para comunicarle que no se han recibido datos nuevos desde hace mas de 24 horas de las siguientes estaciones: 

	$STATEREPORT

Atentamente,

GRUPO TIC PLOCAN	
		
  """ | mail -s "Actualizacion de datos" -a "From: javier.perez@plocan.eu" $RECIPIENTS
}

# ############################################ #
# ############### SendJabber ################# #
# Send jabber to recipient(s)                  #
# $1: recipients{,recipients}*		       #
# ############################################ #
function SendJabber()
{
  echo "Jabber $STATEREPORT"  
  /usr/local/share/observadir/formatjabber.py javiprmes,tania "$STATEREPORT"
}


# ############################################# #
# ################ MAIN ####################### #
# ############################################# #
# GLOBAL VAR INIT

DIR2CHECK=""
FILE2CHECK=""
STATIONNAME=""
RECIPIENTS=""
STATEREPORT=""
CURRENT=$(date +%s)
#ALARMUPAT=86400 ### SPECIFIED TIME ###
ALARMUPAT=86400 ### SPECIFIED TIME ###
ALARMUPLIMIT=90000

CheckParameters
CheckTimestamp
SendJabber
