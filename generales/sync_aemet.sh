#!/bin/bash
#/usr/local/share/aemetv3/obten_aemet && /bin/envia_jabber "$(/bin/date \+\"%Y%m%d %H:%M\") `/bin/hostname` Sincronizacion AEMET hecha"
/usr/local/share/aemetv3/obten_aemet && /mnt/bin/envia_jabber2.0 javiprmes,tania "$(/mnt/bin/pythonlib/formatjabber.py 'Sincronizacion AEMET-SIBOY realizada')"
