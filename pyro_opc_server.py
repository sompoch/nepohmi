#!python.exe
import site

#!python.exe
# -*- coding: utf-8 -*-
import OpenOPC
import time
from threading import *#Thread
import threading
import datetime
import subprocess
#import pyro_opc_server # import own 


import signal
import sys,gobject,os
import psutil
import ConfigParser

import Pyro4

'''The OPC find item to list use method opc.list and flat == True
Version 0.1 create date june.2011
by Mr. sompoch thuphom this script write under GLP License.
Test run script  on python 2.6.5 windowXP,win7. You need to download
OpenOPC library from http://openopc.sourceforge.net
'''

global_list={}
global save_process
save_process = 0


class OPCThread(Thread):
    def __init__ (self,server,tag_read,global_list):
        Thread.__init__(self)
        self.tag_read = tag_read
        self.server = server
        self.killed = False
        self.global_list = global_list
        
    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        self.run = self.__run      # Force the Thread to install our trace.
        threading.Thread.start(self)
        print "Thread OPC start"
        
    def run(self):
        self.readOPC(self.server,self.tag_read)
        
        
    def readOPC(self,server,tag_read):
        opc = OpenOPC.client() 
        opc.connect(server)
        result = opc.read(tag_read,timeout=7000)
        del self.global_list[server]['value'][:] # delete all item 
        self.global_list[server]['value'] = result
        
        check_time_out = 0
        run_proc = True
        try:
            while run_proc:
                # reset tag timeout
                if check_time_out > 3:
                    check_time_out = 0
                    tag_read = []
                    del_tag = []
                    for t in self.global_list[server]['tag']:
                        time_out = self.global_list[server]['tag'][t]-1
                        print "Tag %s timeout %s " % (t,time_out)
                        if time_out > 0  :
                            self.global_list[server]['tag'][t]=time_out
                            tag_read.append(t)
                        else:
                            del_tag.append(t)
                    # delete tag from servie 
                    
                    for t in del_tag:
                        del self.global_list[server]['tag'][t]
                    
                    
                #print "OPC thread service update between 2 second \r\n Try to set new value in global_list : ",
                #print self.global_list
                time.sleep(2)
                if len(tag_read)>0:
                    result = opc.read(tag_read,timeout=7000)
                    #print result
                    del self.global_list[server]['value'][:] # delete all item 
                    self.global_list[server]['value'] = result
                    
                    check_time_out +=1
                else:
                    run_proc = False # exit process 
                    del self.global_list[server] # delete all tag and server
                    
        except Exception,err:
            print "interrupt exit with thread opc : ",err
        finally:
            opc.close()
            print "The OPC client will be close connect..."
        
    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        try:
            if self.killed:
                if why == 'line':
                    raise SystemExit()
            return self.localtrace
        except:
            raise SystemExit()

    def kill(self):
        self.killed = True
        

class ServiceClass(object):
    def method(self,arg):
        print "Method called with %s" % arg
        print "You can now try to stop this server with ctrl-C/ctrl-Break"
        time.sleep(1)
        
    def get_opc(self):
        print "Get opc server "
        opc = OpenOPC.client() 
        all = opc.servers()
        opc.close()
        return all
    
    def stop_process(self):
        print "Command stop opc process"
        
    def end_process(self):
        print "Commnad end opc process"
        
    def start_process(self):
        print "Start opc process"
    
    def process_info(self):
        #Process infomation 
        for t in psutil.get_pid_list():
            p = psutil.Process(t)
            opc_serv = p.cmdline
            if p.name == 'python.exe':
                #opc_serv = p.cmdline
                if 'pyro_opc_server' in opc_serv[len(opc_serv)-1]:
                    mem_info = psutil.phymem_usage()
                    mem_use = ((mem_info[0]*p.get_memory_percent()))/104857600
                    msg = "pyro_opc_server.py  process memory use %s percent %s mb" %(p.get_memory_percent(),mem_use)
                    self.create_log(msg)
                    '''print "PID              : ",t
                    print "Process name     : ",opc_serv[len(opc_serv)-1]
                    print "Status           : ",p.status
                    print "% Process CPU    : ",p.get_cpu_percent(interval=1.0)
                    print "% Process MEM    : ",p.get_memory_percent()
                    print "Memory usage %s Mb    : " % (mem_use)'''
    
    def get_opc_info(self,opc_server):
        print "Get opc server infomation"
        opc = OpenOPC.client() 
        opc.connect(opc_server)
        all = opc.info()
        opc.close()
        
        return all 
    
    def get_opc_list(self,opc_server,browe_option):
        print "Initial to get all OPC item from  ",opc_server
        opc = OpenOPC.client() 
        opc.connect(opc_server)
        #all = opc.list()
        if browe_option: #Flat == True
            all = opc.list('*',flat = True)
            print "------------------------"
            for t in all:
                print t
            opc.close()
            
            return all # rerturn all opc server
        else:
            return all
        
    def threadDianostic(self):
        print "Get all thread on opc service "
        thread_name = []
        for thread in enumerate():
            thread_name =  str(thread.getName())
            thread_name.append(thread_name)
            
    def tag_on_service(self):
        return global_list
    
    def kill_service(self):
        sys.exit(1)
        
    def getScriptPath(self):
        return os.path.dirname(os.path.realpath(sys.argv[0]))

    def create_log(self,message):
        path_script = self.getScriptPath()
        if os.name == 'nt':
            #For win32
            log_name = str(path_script)+'\\log\\'+str(time.strftime("%d_%m_%Y"))+'.log'
        else:
            #For linux and other
            log_name = str(path_script)+'/log/'+str(time.strftime("%d_%m_%Y"))+'.log'
        
        f = open(log_name,'a')
        write_message = str(time.strftime("- %H:%M:%S")) + ' \t '+message+'\r\n'
        f.write(write_message)
        f.close()
        
    
    def read_opc_tag(self,opc_server,tag,time_stamp,count_stamp): 
        #*****************************************************************
        #tsmp = object timestamp -- tsmp.time_stamp , tsmp.count
        #
        #define global_list to keep the return tag value from OPC server
        #if global_list{dict} hasn't opc server name key that will be to 
        #create new OPCThread service try to read some 
        #request tag from opc server every 2 second
        #*****************************************************************
        global save_process
        if not global_list.has_key(opc_server):
            print "Global list not has key ",opc_server
            global_list[opc_server]={}
            global_list[opc_server]['value']= [] 
            global_list[opc_server]['tag']={}
            for t in tag:
                #Define tag timeout if not respond from client more than 5 times there is remove from read opc service
                global_list[opc_server]['tag'][t]= 5 # time out = 10 
            start_opc = OPCThread(opc_server,tag,global_list)
            start_opc.setName(opc_server) # set thread name
            start_opc.start()
            
            msg = "OPCThread  %s is start..." % (opc_server)
            print msg
            self.create_log(msg) #Create log message
             
        else:
            # update new tag time out 
            for t in tag:
                if not global_list[opc_server]['tag'].has_key(t):
                    global_list[opc_server]['tag'][t]= 5 # update timeout = 5
                else:
                    global_list[opc_server]['tag'][t]= 5
            
            #print "Found %s key has existing!" % (opc_server)
        time_s = 0
        save_process +=1
        #save process
        if save_process > 200:
            save_process =0
            self.process_info()
        
            
        #To check process has log time respond[opc hang] and try to kill this thread and restart
        #new opc thread service
        if global_list[opc_server]['value'] is not None:
            if len(global_list[opc_server]['value'])>0:
                time_s = global_list[opc_server]['value'][0][3]
                if time_stamp != time_s:
                    time_stamp = time_s
                    #print "Time stamp check ",time_stamp
                    count_stamp = 20 # refresh new time stamp timeout count 
                else:
                    count_stamp -= 1
                    #print "Time out count = ",count_stamp 
                    if count_stamp < 0 :
                        print "OPC Thread hang! try to restart"
                        print ":KILL THREAD FUNC__"
                        msg = "OPC Thread %s has long time responded try to  :KILL THREAD FUNC__" % (opc_server)
                        self.create_log(msg)

                        thread_read = {}
                        cnt_thread = 0
                        for thread in enumerate():
                            cnt_thread += 1
                            thread_name =  str(thread.getName())
                            if "Thread-" in thread_name:
                                #Except Thread-1,4
                                pass
                            else:
                                if not thread_read.has_key(thread_name):
                                    thread_read[thread_name] = 1
                                else:
                                    thread_read[thread_name] +=1
                            print thread_name
                            #if thread.isAlive():
                            try:
                                if thread_name == opc_server:
                                    thread.kill()
                                    if global_list.has_key(opc_server):
                                        del global_list[opc_server] # make sure global list has key opc server 
                            except Exception,err:
                                msg = 'Error found when try to kill thread : ',str(thread.getName()),err
                                print msg
                                self.create_log(msg)
                        
                        all_thread = "Print OPC service thread total[+hidden]  :  %s \r\n" % (cnt_thread)
                        count_thread = 0 
                        for v in thread_read:
                            if thread_read[v] > 1:
                                count_thread = thread_read[v]
                                all_thread = all_thread + '\t\t\t'+v+'['+str(thread_read[v])+']\r\n'
                            else:
                                all_thread = all_thread + '\t\t\t'+v+'\r\n'

                        self.create_log(all_thread)
                        #Restart all service because OPCthread more than limited
                        msg = "Count thread = %s "%(count_thread)
                        self.create_log(msg)
                        if count_thread > 10:
                            self.create_log("Try to restart pyro_opc_service.py because OPCthread has more than limited[5].")
                            for t in psutil.get_pid_list():
                                p = psutil.Process(t)
                                opc_serv = p.cmdline
                                
                                #print p.name,
                                if p.name == 'python.exe':
                                    #opc_serv = p.cmdline
                                    if 'pyro_opc_server' in opc_serv[len(opc_serv)-1]:
                                        print "PID              : ",t
                                        print "Process name     : ",opc_serv[len(opc_serv)-1]
                                        print "Status           : ",p.status
                                        print "% Process CPU    : ",p.get_cpu_percent(interval=1.0)
                                        print "% Process MEM    : ",p.get_memory_percent()
                                        print "Try to terminate process and restart new process "
                                        path_script = self.getScriptPath()
                                        opc_script = str(path_script)+'\\pyro_opc_server.py'
                                        cmd = ["start", "python",opc_script] 
                                        theproc = subprocess.Popen(cmd,shell = True)
                                        theproc.communicate()
                                        p.terminate()
                                        break
                                    
        if not global_list.has_key(opc_server):
            return None
        else:
            #Return opc tag value with new time stamp and counting stamp
            return global_list[opc_server]['value'],time_stamp,count_stamp
        
obj=ServiceClass()

# We are responsible to (re)connect objects with the same object Id,
# so that the client can reuse its PYRO-uri directly to reconnect.
# There are a few options, such as depending on the Name server to
# maintain a name registration for our object (see the serverNS for this).
# Or we could store our objects in our own persistent database.
# But for this example we will just use a pre-generated id (fixed name).
# The other thing is that your Daemon must re-bind on the same port.
# By default Pyro will select a random port so we specify a fixed port.
reboot = 5
while reboot > 0 :
    print "Pyro service will be start in 5 second"
    time.sleep(5)
    try:
        daemon = Pyro4.core.Daemon(port=7779)
        uri = daemon.register(obj,objectId="opc.reconnect")
        print "Server started, uri=%s" % (uri)
        daemon.requestLoop()
    except Exception,err:
        print "Error : " ,err
    reboot -=1
    


