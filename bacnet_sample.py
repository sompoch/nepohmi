#!/usr/bin/env python
'''
BACnet create file.bac sample for OPC and BACnet Browser Service
Start date 17.07.2011, version 0.1 
By Sompoch Thuphom , E-MAIL: mjko68@hotmail.com 
This script write under GPL License
'''
import os
import gtk
import pickle


print "Bacnet Create tag Sample"
device_net = {}
currentPath = os.getcwd()


# Devcie to Bacnet_tag
#file structure 
#Device_net.bac-----|                           type [dic]
#                   |bac_tag                    type {dic}
device_name =['sample server','demo server']
for i in range(2):
    Server_id = str(i)
    device_net[device_name[i]]={}
    device_net[device_name[i]]['device_id'] = i
    device_net[device_name[i]]['analog input 1'] = 1,1 # Bacnet ID : Bacnet Instant ID , point number
    device_net[device_name[i]]['analog input 2'] = 1,2
    #print type(Device_net[Server_id]['analog input 1'] )
    
    #bacnet_tag.append(Device_net)

#Load init bacnet from file
'''
myload = ''
if os.name == 'nt':# check window os
    pathImage = currentPath+ '\\configure\\bacnet_tag.bac'
    myload = open(pathImage,'r')
else: # other os , linux
    myload = open('configure/bacnet_tag.bac','r')
    
device_net = pickle.load(myload)
myload.close()
print "load bacnet list from file "'''
    
for t in device_net:
    for j in device_net[t]:
        print device_net[t]['device_id']

#Save bacnet to file 
if os.name == 'nt':# check window os
    pathImage = currentPath+ '\\configure\\bacnet_tag.bac'
    savefile = open(pathImage,'wb')
else: # other os , linux
    savefile = open('configure/bacnet_tag.bac','wb')
    
pickle.dump(device_net, savefile) 
savefile.close()
    
