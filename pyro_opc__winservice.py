'''

 Author: Alex Baker
 Date: 7th July 2008
 Description : Simple python program to generate wrap as a service based on example on the web, see link below.
 
 http://essiene.blogspot.com/2005/04/python-windows-services.html

 Usage : python aservice.py install
 Usage : python aservice.py start
 Usage : python aservice.py stop
 Usage : python aservice.py remove
 
 C:\>python aservice.py  --username <username> --password <PASSWORD> --startup auto install

'''

import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os
import time
import subprocess
import psutil

class aservice(win32serviceutil.ServiceFramework):
   
    _svc_name_ = "PyroOPC"
    _svc_display_name_ = "PyroOPC"
    _svc_description_ = "OPC server service with pyro remote object"
     
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

    def SvcStop(self):
        '''Find process and force terminate it'''
        for t in psutil.get_pid_list():
            p = psutil.Process(t)
            opc_serv = p.cmdline
            if p.name == 'python.exe':
                if 'pyro_opc_server' in opc_serv[len(opc_serv)-1]:
                    p.terminate()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)                    
     
    def SvcDoRun(self):
        import servicemanager      
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 

        self.timeout = 3000
        cnt = 0
        
        cmd = ["start", "python","D:\\home\\pro\\openhmi\\pyro_opc_server.py"] # t = opc server name
        theproc = subprocess.Popen(cmd,shell = True)
        theproc.communicate()

        while True:
            # Wait for service stop signal, if I timeout, loop again
            #for t in range(10):
            time.sleep(1)
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            # Check to see if self.hWaitStop happened
            if rc == win32event.WAIT_OBJECT_0:
                # Stop signal encountered
                servicemanager.LogInfoMsg("Pyro OPC Service - STOPPED")
                break
            '''else:
                cnt +=1
                if cnt > 10 :
                    cnt = 0
                    dt = time.strftime('%d-%m-%Y %H:%M:%S')
                    servicemanager.LogInfoMsg(str(dt)+" Pyro and OPC service running") '''  
               

def ctrlHandler(ctrlType):
    return True
                  
if __name__ == '__main__':   
    win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
    win32serviceutil.HandleCommandLine(aservice)
