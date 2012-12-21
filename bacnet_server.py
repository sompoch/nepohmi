import os
import time
import pickle
from threading import Thread
import threading
import socket
import datetime
from twisted.internet import reactor
from twisted.spread import pb
'''
Bacnet server service is running when request from client
and interface socket use twisted
script version 0.1 
begin date 23.7.2011

'''
class BacnetThread(Thread):
    def __init__ (self,device_net_name):
        Thread.__init__(self)
        self.state = device_net_name
        
        
    def run(self):
        while True:
            self.getBacnetDevice3(self.state)
            time.sleep(5)
        
    def getBacnetDevice3(self,device_net_name):
        
        #print "Get BACnet device on network! "
        print "Read tag value on ",device_net_name['device_id']
        id = str(device_net_name['device_id'])
        for tag in device_net_name:
            time.sleep(0.05) # delay for load CPU
            print tag,
            if tag != 'device_id':
                tag_id = device_net_name[tag]
                arg = id+ ' '+str(tag_id[0])+ ' ' + str(tag_id[1])+' 85'
                cmd = "./getDeviceValue.sh "+arg #run command script for find BACnet device name
                print cmd,
                result = os.popen(cmd)
                value = result.read()
                print 'value = '
                print value
                if 'Error: APDU Timeout' in value:
                    print 'Error: APDU Timeout when get bacnet device'
                    return True # break if found error
            
        '''for j in devicelist:
            arg = j+ ' '+ '8 '+j+' 77'
            cmd = "./getDeviceValue.sh "+arg #run command script for find BACnet device name
            print "command read bacnet name ",cmd
            result = os.popen(cmd)
            for i in result.readlines():
                i = i.replace('"','')
                i = i.replace('\n','')
                i = i.replace('\r','')
                success = i,j
                #widgetPack['getDevice'].append(success) # return value   devciename,id
                disp = disp + i + '['+j+']  '
                
                
        
        shwText =  "Found  %s device " % (len(devicelist))
        disp = disp.replace('\n','')
        disp = disp.replace('\r','')'''
            
       
        
        return True
    
    def checkTagExist(self,device_net,result_device):
        for j in device_net:
            if j == result_device[0]:
                #Show dialog warning 
                message = "Can't add new device because  %s exist." % (j)
                print message
                #self.warning_dialog(message)
                return False
            if device_net[j]['device_id'] == result_device[1]:
                message = "Can't add new device because ID %s exist." % (result_device[1])
                print message
                #self.warning_dialog(message)
                return False
                #end of dialog warning
        return True
    
class Echoer(pb.Root):
    def remote_echo(self, st):
        print 'echoing:', st
        if st == 'sompoch':
            dt = 'Mr. sompoch'
        else:
            dt = str(datetime.datetime.now())
            
        return dt

class bacnet_service():
    def run_server(self):
        widgetPack = {}
        widgetPack['getDevice'] = []
        
        myload = ''
        if os.name == 'nt':# check window os
            pathImage = currentPath+ '\\configure\\bacnet_tag.bac'
            myload = open(pathImage,'r')
        else: # other os , linux
            myload = open('configure/bacnet_tag.bac','r')
            
        device_net = pickle.load(myload)
        myload.close()
        widgetPack['device_net'] = device_net
        for bac_name in device_net:
            print bac_name,
            print device_net[bac_name]['device_id']
            getDevcie = BacnetThread(device_net[bac_name])
            getDevcie.start()
        '''
        for i in range(3):
            getDevcie = BacnetThread(widgetPack)
            getDevcie.start()
        print "Try to start bacnet service on port 8008"
        '''
        #reactor.listenTCP(8008, pb.PBServerFactory(Echoer()))
        #reactor.run()
        
        
# We'll pickle a list of numbers:
someList = [ 1, 2, 7, 9, 0 ]
pickledList = pickle.dumps ( someList )

# Our thread class:
class ClientThread ( threading.Thread ):

   # Override Thread's __init__ method to accept the parameters needed:
    def __init__ ( self, channel, details ):

        self.channel = channel
        self.details = details
        threading.Thread.__init__ ( self )

    def run ( self ):

        print 'Received connection:', self.details [ 0 ]
        self.channel.send ( pickledList )
        self.channel.close()
        print 'Closed connection:', self.details [ 0 ]

# Set up the server:
server = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
server.bind ( ( '', 2728 ) )
server.listen ( 5 )
st = bacnet_service()
st.run_server()
# Have the server serve "forever":
print "Start bacnet socket service"
while True:
    channel, details = server.accept()
    ClientThread ( channel, details ).start()

'''
if __name__ == "__main__":
    st = bacnet_service()
    st.run_server()
    #bacnet_device()'''
    
    
    
    
    
    