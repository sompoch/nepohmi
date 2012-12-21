#!/usr/bin/env python
'''
Sample create database.db  for OPC,BACnet,Other and Browser Service
Start date 03.08.2011, version 0.1 
By Sompoch Thuphom , E-MAIL: mjko68@hotmail.com 
This script write under GPL License
'''
import os
import gtk
import pickle


print "Create Sample Database for Tag Browser"
server_net = {}
currentPath = os.getcwd()


# Create root database
db =['OPC','Bacnet IP','Modbus','XML','Simulate','Local']
for svr in db:
    server_net[svr] = {} # add root database to dictionary 
    print svr
#Load init bacnet from file
'''
myload = ''
if os.name == 'nt':# check window os
    pathImage = currentPath+ '\\configure\\tag.db'
    myload = open(pathImage,'r')
else: # other os , linux
    myload = open('configure/tag.db','r')
    
server_net = pickle.load(myload)
myload.close()
for g in sorted(server_net.iterkeys()):
    print g
print "load  list from file "'''
    

#Save database to file 
if os.name == 'nt':# check window os
    pathImage = currentPath+ '\\configure\\tag.db'
    savefile = open(pathImage,'wb')
else: # other os , linux
    savefile = open('configure/tag.db','wb')
    
pickle.dump(server_net, savefile) 
savefile.close()
    
