'''
Project readme 
date 6.2.2012  

[****service win32****] 
How to add python script to win32 service 

You can found for this example path 
D:\home\pro\wxpython\winservice.py

Sqlite3 Update value
update TIMEOUT SET time_refresh = 100000;

[Modbus Example]

modbus minimal test --> D:\home\pro\openhmi\pymodbus\example\myModbus.py 
Support standard modbus RTU connect PLC ABB

MOdbus test script .bat
****************************************************************
echo off
d:
cd "D:\home\pro\openhmi\pymodbus\modbus test\modpoll.3.1\win32"
modpoll -b 19200 -d 8 -p none -m rtu -a 1 -r 1 -c 15 COM2
****************************************************************

[WMI]
python library check window process and service 
File example sourcecode
$ D:\home\pro\openhmi\example\wmi_check_service_running.py
File setup library
$ D:\home\pro\openhmi\NSIS\NepoSetup\Utility\WMI-1.4.9.win32
Document 
http://timgolden.me.uk/python/wmi/index.html

[PYTHON WIN32 SERVICE]
$ D:\home\pro\openhmi\pyro_opc__winservice.py
build service with py2exe
Dir D:\home\pro\openhmi\pyexe\pyro_opc
delete some win32 service with command 
--------------------
net stop your_service
sc delete your_service
--------------------
or remove from registry when fail 1072
HKEY_LOCAL_MACHINE/SYSTEM/CurrentControlSet/Services

[NSIS Create Install Package]
#Main script
D:\home\pro\openhmi\NSIS\NepoSetup\nepo_setup.nsi
#Example script 
#	- Install and Check Pyro Service 
D:\home\pro\openhmi\NSIS\example\NepoSetup\install_service.nsi

http://nsis.sourceforge.net/NSIS_Simple_Service_Plugin

[UML Diagram ]
D:\home\pro\openhmi\UML
    1. Service Diagram  # date 20.2.2012
    2. Installation service diagram # date 22.2.2012

'''