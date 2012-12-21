#!python

from twisted.internet import reactor, protocol
import time
import pickle
#import signal
import sys
import os
import global_var
# a client protocol
'''
date : 8-1-2012
by   : sompoch thuphom
e-mail: mjko68@hotmail.com

Opc option select from opc client

--all           To get all opc server name
--status        To read opc peoperty status
-p              Configure server port , defualt 8002
-s              Server Host name or server ip address
-o              OPC Server Name for connect
-d              Disconnect Current OPC Server
-h              Shutdown OPC Server
-r              Restart OPC Server

'''


class EchoClient(protocol.Protocol):
    """Once connected, send a message, then print the result."""
    def __init__(self):
        print "initial to read OPC client "
        #except error cancel by CTRL+C
        #signal.signal(signal.SIGINT, self.signal_handler)
        self.start = False
        self.option = global_var.option
        print "Option select = ",global_var.option
        
    def connectionMade(self):
        #for i in range(10):
        send ={}
        '''if self.start == False:
            send['get_opc_server'] = 'read_tag_list'
        else:
            #send['read_all_tag'] = 1,6'''
        if global_var.option == '--all':
            send['get_opc_servers'] = None
        else:
            send['server_status'] = None
            
        send_command = pickle.dumps ( send )   
        self.transport.write(send_command)
    
    def dataReceived(self, data):
        
        list =  pickle.loads(data)
        if self.start == False:
            self.start = True
            
        for y in list:
            if y =='server_status':
                os.system(['clear','cls'][os.name == 'nt']) # clear value on terminal
                print "OPC Recieve From Server Information : " + str(time.ctime())
                print "-------------------------------------------------------------------------"
                for j in list[y]:
                    print 'Status name %-25s  : value = %-25s ' % (j,list[y][j])
            if y =='get_opc_servers':
                print 'READ ALL OPC SERVER'
                print '-------------------'
                for j in list[y]:
                    print j
                print '-------------------'
                
            '''else:
                os.system(['clear','cls'][os.name == 'nt']) # clear value on terminal
                print "OPC Recieve From Server data time : " + str(time.ctime())
                print "-------------------------------------------------------------------------"
               
                for j in list:
                    print "Tag %-45s      %5s  " %(j,list[j])'''
        
        #reactor.callLater(2, self.connectionMade)#, "hello, world")   
        global_var.opc_value = list
        self.transport.loseConnection()
    
    def connectionLost(self, reason):
        print "connection lost"
        

    def force_lose(self):
        self.transport.loseConnection()

    '''def signal_handler(self,signal, frame):
        print 'You pressed Ctrl+C!'
        self.transport.loseConnection()'''
        

    

class EchoFactory(protocol.ClientFactory):
    
    protocol = EchoClient
    '''def __init__(self,option):
        print "Option"
        self.option = option'''
        
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed - goodbye!"
        reactor.stop()
    
    def clientConnectionLost(self, connector, reason):
        print "Connection lost - goodbye!"
        reactor.stop()



# this connects the protocol to a server runing on port 8000
class running():
    def __init__(self):
        print "start run opc"
        #self.main_read()
    def main_read(self):
        print "Start Read OPC"
        f = EchoFactory()
        reactor.connectTCP("localhost", 8002, f)
        reactor.run()
        return global_var.opc_value
        
#running()
'''
# this only runs if the module was *not* imported
if __name__ == '__main__':
    print sys.argv[1]
    if len(sys.argv) > 1:
        opt = sys.argv[1]
        global_var.option = opt
        if opt == '--status' or opt == None:
            main_read()
        if opt == '--all':
            print "Get server all"
            main_read()
    else:
        main_read()'''
