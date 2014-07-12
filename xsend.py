#!/usr/bin/python
# $Id: xsend.py,v 1.8 2006/10/06 12:30:42 normanr Exp $
import sys,os,xmpp,time

if len(sys.argv) < 2:
    print "Syntax: xsend {JID} \"text\""
    sys.exit(0)

tojid=sys.argv[1]
#text=' '.join(sys.argv[2:])
text=sys.argv[-1]

jidparams={}
if os.access(os.environ['HOME']+'/.xsend',os.R_OK):
    for ln in open(os.environ['HOME']+'/.xsend').readlines():
        # Ignore comments inside $HOME/.xsend file
        if not ln[0] in ('#',';'):
            # Read values, inserting them into a dictionary
            key,val=ln.strip().split('=',1)
            jidparams[key.lower()]=val
for mandatory in ['jid','password']:
    if mandatory not in jidparams.keys():
        open(os.environ['HOME']+'/.xsend','w').write('#Uncomment fields before use and type in correct credentials.\n#JID=romeo@montague.net/resource (/resource is optional)\n#PASSWORD=juliet\n')
        print 'Please point ~/.xsend config file to valid JID for sending messages.'
        sys.exit(0)

jid=xmpp.protocol.JID(jidparams['jid'])
cl=xmpp.Client(jid.getDomain(),debug=[])

con=cl.connect()
if not con:
    print 'could not connect!'
    sys.exit()
print 'connected with',con
auth=cl.auth(jid.getNode(),jidparams['password'],resource=jid.getResource())
if not auth:
    print 'could not authenticate!'
    sys.exit()
print 'authenticated using',auth

#cl.SendInitPresence(requestRoster=0)   # you may need to uncomment this for old server
for recipient in tojid.split(','):
	id=cl.send(xmpp.protocol.Message(recipient,text))
	print 'sent message to ',recipient,'with id',id
	#print "Enviando a ",recipient," el mensaje ",text

time.sleep(1)  


