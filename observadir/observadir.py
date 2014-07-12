#!/usr/bin/python

#####################################################################
######################## OBSERVADIR.PY ##############################
#####################################################################
import time,sys,subprocess,commands,argparse,logging,formatjabber
from watchdog.observers import Observer  
from watchdog.events import PatternMatchingEventHandler,LoggingEventHandler


class MyHandler(PatternMatchingEventHandler):
		
	def process(self, event):
		"""
        	event.event_type 
            	'modified' | 'created' | 'moved' | 'deleted'
        	event.is_directory
            	True | False
       	 	event.src_path
            	path/to/observed/file
        	"""
		whichEvent= {'modified': self.modificado, 'created': self.modificado}.get(event.event_type,self.noIdea)(event)
		#print whichEvent.src_path, event.event_type  # print now only for degug
		#observer.schedule(event_handler, path, recursive=True)
		
	#def creado(self,event):
		#self.current_file=event.src_path
		#print 'Has creado '+self.current_file+'...y lo sabes'
		#elcomando="lsof -n | grep \""+event.src_path+"\" | awk '{print $NF;}'"
		#while True:
		#	output=commands.getoutput(elcomando)
		#	print "OUTPUT:"+output
		#	if not output:
		#		break 
		#	else:
		#		pass
		#print "Fin transferencia: "+self.current_file
		#output2=commands.getoutput("/usr/local/lib/observadir/trata_fich_creado -i '"+self.current_file+"' -o "+args.Output)
		#print "El comando devuelve: "+output2	

	def on_created(self, event):
		self.process(event)
	def on_modified(self, event):
        	self.process(event)
	def modificado(self,event):
		# Send a notification
		self.current_file=event.src_path
		print "Se ha modificado el fichero "+self.current_file
		#commandtoExec="/mnt/bin/envia_jabber2.0 javiprmes,tania \"Datos APRAM actualizados\""
		Fjabb.SendJabberMsg("Fichero actualizado:"+self.current_file)

		#print "Ejecutando "+commandtoExec
		#output2=commands.getoutput(commandtoExec)
		#self.process(event)
	def on_deleted(self, event):
        	self.process(event)
	def noIdea(self,event):
		print "No conozco ese evento "+event.event_type

parser= argparse.ArgumentParser()
parser.add_argument("-d","--dir",dest='Dir2Check',required=True,help="Input file")
#parser.add_argument("-o","--output-file",dest='Output',required=True,help="Output dir/file")
args=parser.parse_args()

###
############# MAIN ####################
###
Fjabb=formatjabber.formatjabber()
if __name__ == '__main__':
	Fjabb.SetRecipients("javiprmes,tania")
#	Fjabb.SendJabberMsg("Probando")

	observer = Observer()
	# Files to watch 
    	event_handler=MyHandler(patterns = ["*.txt"],ignore_directories=True)
	# Dir to be checked ('.' if no parameter specified using "-d")
    	observer.schedule(event_handler, path=args.Dir2Check if args else '.',recursive=False)
	observer.start()

    	try:
        	while True:
            		time.sleep(1)
			 #print "Waiting"
    	except KeyboardInterrupt:
        	observer.stop()

	observer.join()

