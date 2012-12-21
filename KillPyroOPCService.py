#!python
import wmi
import time

#This script to stop PyroOPC service 
#Step1 : Force to stop process 
#Step2 : If process can't stop with some trouble it will be force kill by command
#Version 0.0.1 date 24.02.2012 
#Own : sompoch thuphom 
#E-mail : mjko68@hotmail.com
#Run : python kill_service.py 
#Make exe :python kill_service.py py2exe
#Use with NSIS help check when install/Uninstall new PyroOPC service

def kill_proc():
    c = wmi.WMI ()
    #Force process stop
    for service in c.Win32_Service(Name="PyroOPC"):
        state = service.State
        if state != 'Stopped':
            result, = service.StopService()
            if result == 0:
                print "Found Service PyroOPC is start try to  ", service.Name, "stopped"
            else:
                print "Some problem when stop PyroOPC service"
                break
        else:
            print "PyroOPC service is stopped!"
            break
        
    time.sleep(3)
    #Check service stopped again
    #If service can't stop by above command this is backup force stopped service 
    #For make sure this service has kill all
    for process in c.Win32_Process ():
        if 'python' in process.Name:
            proc_command  = process.CommandLine
            if 'pyro_opc_server' in proc_command:
                print proc_command,
                print process.ProcessId
                print "Terminate PyroOPC process...",
                print process.Terminate()
                
            
if __name__ == '__main__':
    #Delay time to waiting some task
    time.sleep(2)
    kill_proc()