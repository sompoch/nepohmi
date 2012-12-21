import pickle
import socket
import threading
#import OpenOPC
import getopt, string, re, sys,os
import time
from datetime import datetime
import random
import global_var
if os.name == 'nt':
    import OpenOPC
# Here's our thread:

class opcservice ( threading.Thread ):
    
    def __init__(self,opc_server_name,tag,opt):
        self.options = {}
        self.options['opc_server_name'] = opc_server_name
        self.options['tag'] = tag
        self.options['state'] = opt
        #print 'initial opc service running...'
        threading.Thread.__init__ (self)
        
    def run ( self ):
        
        if self.options['state']== 'R':
            upTime = str(datetime.now())
            
            for t in self.options['tag']:
                state_val = random.choice(['True','False']) #random test value
                global_var.opc_tag_value[t] = (state_val,'Bad',upTime[:19])
            '''
            tag_list =[]
            for j in self.options['tag']:
                tag_list.append(j)
            #self.options['opc_server_name'] 
            
            pre_send = [self.options['opc_server_name'],tag_list,'R']
            
            pickledList = pickle.dumps (pre_send)
            
            try:
                client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                client.connect ( ( 'localhost', 2728 ) )
                #setTag = '3,M30.0,BOOL,R,'
                #client.send (setTag)
                
                client.send(pickledList)
                Rinput = True
                data = ''
                
                timeout = False
                set_count = 50
                #while timeout == False:
                while Rinput:
                    Rinput = client.recv (4096)
                    data += Rinput
                list =  pickle.loads(data)
                for rd in list:
                    #print rd
                    #print type(rd)
                    tagRead = rd[0]
                    tag_val = (str(rd[1]),rd[2],rd[3])
                    global_var.opc_tag_value[tagRead]=tag_val
                    #print 'tag name  ',tagRead
                    #print 'tag value ',tag_val
                    #print tag_val
                    
                client.close()
            except Exception,e:
                pass
                '''
                #print 'error found :',e
            
            
        if self.options['state'] == 'W':
            client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
            client.connect ( ( '192.168.13.35', 2728 ) )
            setTag = '3,'+self.options['tagname'] +',BOOL,W,'+ str(self.options['value'])
            client.send (setTag)
            print client.recv ( 4096  )


class update_item():
    def __init__(self):
        print '****initial load update item data****'
        
    def update_on_running(self,list_item,canvas):
        for t in list_item:
            print t
        
        return global_var.mode_run
        #opcService(opc_server_name,tag,opt).start()
        

class read_from_socket():
    def __init__(self):
        print '****initial load update item data****'
        
    def readOPCSocket(self,opcname,list_item):
        try:
            print 'connection at %s ' % (time.ctime() ),
            client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
            client.connect ( ( 'localhost', 2728 ) )
            list_tag_str = []
            for tg in list_item:
                list_tag_str.append(tg)
            pack_send = [opcname,list_tag_str,'R','None']
            
            pickledList = pickle.dumps (pack_send)
            client.sendall ( pickledList )
            Rinput = True
            data = ''
            timeout = False
            set_count = 50
            #while timeout == False:
            while Rinput:
                Rinput = client.recv (4096)
                data += Rinput
            list =  pickle.loads(data)

            client.close()
            for t in list:
                typeIn = type(list[t][0])
                #print 'Type OPC is... ',tyepIn
                #if typeIn  == '<type \'float\'>':
                if list[t][0] == 0.0:
                    val = ('False',list[t][1],list[t][2])
                if list[t][0] == 1.0:
                    val = ('True',list[t][1],list[t][2])
                        
                #else:
                    #val = (str(list[t][0]),list[t][1],list[t][2])
                global_var.opc_tag_value[t] = val
                #print val
            return list
        except:
            print 'error to connect'
            
    def writeOPCSocket(self,opcname,list_item,value):
        try:
            
            print 'connection at %s ' % (time.ctime() ),
            client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
            client.connect ( ( 'localhost', 2728 ) )
            list_tag_str = []
            for tg in list_item:
                list_tag_str.append(tg)
            pack_send = [opcname,list_tag_str,'W',value]
            
            pickledList = pickle.dumps (pack_send)
            client.sendall ( pickledList )
            Rinput = True
            data = ''
            timeout = False
            set_count = 50

            while Rinput:
                Rinput = client.recv (4096)
                data += Rinput
                
            return data
            client.close()
            
        except Exception ,e:
            print 'Error on connection',e
        
            
        
'''
for x in xrange ( 3 ):
    myTag = ['1','2','3']
    opcService('OPC_DA2.9',myTag,'R').start()
    
print 'End of process'
'''

