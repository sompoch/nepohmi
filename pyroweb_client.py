#!/bin/local/python 
#-*- coding: utf-8 -*-
#OPC Client 

import time 
import sys,os
import Pyro4
import global_var
import pickle
import sqlite3 as lite
#import psutil


# Create time with data structure 
class objTimeStamps(object):
    def __init__(self, time_stamp = None, count = 5):
        self.time_stamp = time_stamp # Set time stamp from opc server
        self.count = count # timeout count 

def get_opc_all(host,port):
    
    uri='PYRO:opc.reconnect@'+host+':'+str(port)
    obj=Pyro4.Proxy(uri)
    print "get opc server on pyro service ",uri
    #while True:
    try:
        async=Pyro4.async(obj)
        asyncresult=async.get_opc()
        print "Waiting read opc server on %s port %s in 10 seconds..." % (host,port)
        ready=asyncresult.wait(10)   
        print "Status after waiting = ",ready  # should print False
        #server_list = obj.get_opc()
        if ready:
            return asyncresult.value
        else:
            return "Timeout "
        
        '''# Ready to get OPC List all
        read_serv0 = asyncresult.value[0]
        print "Server get list is ",read_serv0
        asyncresult=async.get_opc_list(read_serv0)
        ready=asyncresult.wait(5) 
        print "status get all opc server =",ready 
        if ready :
            for g in asyncresult.value:
                print g
        else:
            print "Timeout to read opc list "
            
        #Read OPC Tag
        read_item = asyncresult.value[30:36]
        asyncresult=async.read_opc_tag(read_serv0,read_item)
        ready=asyncresult.wait(5) 
        print "status get all opc server =",ready 
        if ready :
            for g in asyncresult.value:
                print g
        else:
            print "Timeout to read opc list "
        '''
        # Read OPC Tag (Random)
        
    except Pyro4.errors.ConnectionClosedError:
        print "(Restart the server now)"
        #obj._pyroReconnect()
        
def opc_info(host,port,server_name):
    uri='PYRO:opc.reconnect@'+host+':'+str(port)
    obj=Pyro4.Proxy(uri)
    print "get opc server on pyro service ",uri
    try:
        async=Pyro4.async(obj)
        asyncresult=async.get_opc_info(server_name)
        print "Waiting read opc server on %s port %s in 10 seconds..." % (host,port)
        ready=asyncresult.wait(10)   
        print "Status after waiting = ",ready  # should print False
        if ready:
            return asyncresult.value
        else:
            return "Timeout "
        
    except Pyro4.errors.ConnectionClosedError:
        print "(Restart the server now)"
        return "Timeout "
    
def opc_item(host,port,server_name):
    uri='PYRO:opc.reconnect@'+host+':'+str(port)
    obj=Pyro4.Proxy(uri)
    print "get opc server on pyro service ",uri
    try:
        async=Pyro4.async(obj)
        asyncresult=async.get_opc_list(server_name,True) # Flat = True
        print "Waiting to read opc item on %s port %s in 10 seconds..." % (host,port)
        ready=asyncresult.wait(10)   
        print "Status after waiting = ",ready  # should print False
        if ready:
            return asyncresult.value
        else:
            return "Timeout"
        
    except Pyro4.errors.ConnectionClosedError:
        print "(Restart the server now)"
        return "Timeout"
    
def getScriptPath():
    return os.path.dirname(os.path.realpath(sys.argv[0]))

def create_log(message):
    path_script = getScriptPath()
    if os.name == 'nt':
        #For win32
        log_name = str(path_script)+'\\log\\'+str(time.strftime("%d_%m_%Y"))+'.log'
    else:
        #For linux and other
        log_name = str(path_script)+'/log/'+str(time.strftime("%d_%m_%Y"))+'.log'
    print "Create log %s %s " % (log_name,message)
    f = open(log_name,'a')
    write_message = str(time.strftime("- %H:%M:%S")) + ' \t '+message+'\r\n'
    f.write(write_message)
    f.close()
    
def opc_read(alias_name,host,port,server_name,tag,time_out,database_name):
    #*********************************************************
    #alias_name = opc alias name 
    #host       = ip address of server or 'localhost'
    #port       = pyro server port defualt 7777
    #tag        = opc tag read
    #time_out   = timeout count default = 10
    #database name = sqlite3 database name that mean graphic file_name+_temp.db
    #                Example if your HMI graphic name is 'test_pyro.xgd' = test_pyro_temp.db
    #*********************************************************
    uri='PYRO:opc.reconnect@'+host+':'+str(port)
    obj=Pyro4.Proxy(uri)
    #print "get opc server on pyro service ",uri
    
    
    con = lite.connect(database_name)
    cur = con.cursor()
    query = "select * from ITEM;"
    cur.execute(query)
    result = cur.fetchall()
    for t in result:
        print t
    
    count_none = 0
    process_alive = True
    #Create python data structure 
    tsmp = objTimeStamps(time_stamp=0,count=10)
    #parameter : tsmp.time_stamp,tsmp.count see class objTimeStamps on top script for more detial
    
    try:
        while process_alive :
        #time_out -= 1 # Count loop
            try:
                async=Pyro4.async(obj)
                #print tsmp
                print "Get opc  1st tag timesatamp %s and counting %s " % (tsmp.time_stamp,tsmp.count)
                asyncresult=async.read_opc_tag(server_name,tag,tsmp.time_stamp,tsmp.count)
                #print "Waiting to read opc item on %s port %s in 10 seconds..." % (host,port)
                ready=asyncresult.wait(2)   
                #print "Status after waiting = ",ready  # should print False
                if ready:
                    opc_get_value = asyncresult.value
                    if opc_get_value is not None:
                        tsmp.time_stamp = opc_get_value[1]
                        tsmp.count = opc_get_value[2]
                        
                        for t in opc_get_value[0]:
                            get_tag = "OPC."+alias_name+'.'+server_name+'.'+t[0]
                            query = "UPDATE ITEM SET value=?,time_stamp=?,quality=? WHERE tag=\'"+get_tag+"\'"
                            #print query
                            cur.execute(query,(t[1],t[3],t[2]))
                            #print t
                        
                        con.commit()
                        #*********************************************************
                        #print opc_get_value
                        #Read time refresh from table TIMEOUT 
                        #*********************************************************
                        query = "SELECT time_refresh FROM TIMEOUT"
                        cur.execute(query)
                        time_alive = cur.fetchone()
                        #Return time_alive data value type tuple
                        if time_alive is not None:
                            time_check =  time_alive[0]-1
                            #*********************************************************
                            #Try to rocess alive decount
                            #This service reduce[-1] time_refresh every loop scan
                            #*********************************************************
                            if time_check> -1:            
                                query = "UPDATE TIMEOUT SET time_refresh= "+ str(time_check)+';'
                                cur.execute(query)
                                con.commit()
                            
                            if time_check<0:
                                # Exit process
                                print "close the process with time not respone from client"
                                
                                process_alive = False # Set process die
                        else:
                            #*********************************************************
                            #This process can't connect database file try to 20 times 
                            #if count_none more than 20 process will be ending.
                            #*********************************************************
                            count_none +=1
                            print count_none
                            if count_none >20 :
                                print "Process die check timeout == None"
                                process_alive = False
                            
                    
                    
                else:
                    print "Timeout when get opc tag from server"
                    
                time.sleep(1)
                    
                    
            except Pyro4.errors.ConnectionClosedError:
                print "(Restart the server now)"
                msg = 'Pyro4.errors.ConnectionClosedError from %s \r\n \t\t Server not respond or connection lose ' % (uri)
                create_log(msg)
                obj._pyroReconnect()
                
            except Pyro4.errors.CommunicationError:
                print "CommunicationError..."
                msg = 'Pyro4.errors.CommunicationError  from % s \r\n \t\t cause pyro_opc_server.py not running or specific port or ip invalid ' % (uri)
                create_log(msg)
                obj._pyroReconnect()
                
            
                #return "Timeout"
        #print "Exit from pyro service now cause run state = ",global_var.mode_run
    except Exception,err:
        print "Error found ",err
        create_log(str(err))
    
    finally:
        if con:
            con.close()
        
#PC23434 test_opc_pyro4_temp.db localhost 7777 KEPware.KEPServerEx.V4 PC23434KEPware.KEPServerEx.V4.tag
if __name__ == '__main__':
    if len(sys.argv) > 0:
        alias_name = 'PC23434'#sys.argv[1]
        database_name = 'test_opc_pyro4_temp.db'#sys.argv[2]#"test_opc_pyro4.xgd"#
        ip = 'localhost'#sys.argv[3] # type string
        port = '7779'#sys.argv[4] # type string 
        opc_server_name = 'KEPware.KEPServerEx.V4'#sys.argv[5] #type string
        list_read = 'PC23434KEPware.KEPServerEx.V4.tag'#sys.argv[6] # type pickle create by 'db_update_value.py'
        print list_read
        f = open(list_read,'r')
        #start to opc service for read pass pyro
        
        list_r = pickle.load(f)
        f.close()
        #print list_read
        opc_get_value =None
        opc_read(alias_name,ip,port,opc_server_name,list_r,10,database_name)
    
    