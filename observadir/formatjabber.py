#!/usr/bin/env python
import sys
from datetime import datetime, date, time
sys.path.append('/mnt/bin/')
import mylib
import socket

######## Class formatjabber ############
########################################
class formatjabber(object):
	def __init__(self):
		self.hostname=socket.gethostname()
		self.LeftBracket='['
		self.RightBracket=']'
	######### SendMessage ##########
	## Formats the string to be sent
	################################ 
	def __ComposeMessage(self,message):
		# Kind of : [[ DATE ]] HOST: name: message 
		self.SetCurrentDate()
		Message = self.LeftBracket*2 + self.now + self.RightBracket*2 + " MESSAGE FROM HOST:" + self.hostname + " :: " + message
		return Message

	def SetRecipients(self,Recipients):
		 self.Recipients=Recipients
	def SetCurrentDate(self):
		 now = datetime.now()
		 self.now=now.strftime("%Y-%m-%d %H:%M")
		
	def GetCurrentDate(self):
		 return self.now
		
	def SendJabberMsg(self,Message):
		FrmtdMessage= self.__ComposeMessage(Message)
		command_exec="/mnt/bin/envia_jabber2.0 "+ self.Recipients + " " + "\""+FrmtdMessage+"\""
#		print "Ejecutando "+command_exec
		mylib.executa(command_exec)

if __name__ == '__main__':
	Fjabb=formatjabber()
	Fjabb.SetRecipients("javiprmes")
	if len(sys.argv)==3:
		Fjabb.SetRecipients(sys.argv[1]) 
		Fjabb.SendJabberMsg(sys.argv[2])
	else:
		print "Use: "+ sys.argv[0] + " user{[,user]}* \"text\""
