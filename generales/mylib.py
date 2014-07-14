#!/usr/bin/python
import subprocess
def executa (command):
        # Ejecutar comando
        #process=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        print "COMANDO A EJECUTAR:"+command
        process=subprocess.Popen(command,shell=True,stdout=subprocess.PIPE)
        # Eliminar espacios en blanco sobrantes
#       output= process.stdout.readline().strip()
        output = process.communicate()[0].strip()
#        output = process.communicate()[0]
        # Dividir en lineas
        output = output.split('\n')
        print output
        return output
