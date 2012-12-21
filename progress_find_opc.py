
import os,sys
import gtk, gobject
import time
import signal
from threading import Thread
import random

from readopc import running
import webclient

import global_var

global state
state = False
theVar = 0

def progress_timeout(pbar,label,finish):
    global state
    #print 'pbar running'
    #if pbobj.activity_check.get_active():
     #   pbobj.pbar.pulse()
    #else:
        # Calculate the value of the progress bar using the
        # value range set in the adjustment object
    pbar.pulse()
   
    '''new_val = pbar.get_fraction() + 0.01
    if new_val > 1.0:
        new_val = 0.0
    # Set the new value
    pbar.set_fraction(new_val)'''
    getBacnetDevice(label)
    BacnetListDevice(pbar,label)

    # As this is a timeout function, return TRUE so that it
    # continues to get called
    print "State %s and finish %s  " % (state,finish) 
    if state:
        pbar.set_fraction(1)
        return False
    else:
        return True

    
def progress_set_text(label,list):
    global state
    global end_  
    print list[0]['object-type']
    if end_:
        #pbar.set_fraction(1)
        return False
    else:
        return True
    
def getBacnetDevice2(label):
        global state
        print "Bacnet get device ! "
        cmd = "./bacgetid.sh"# + " 1 "+str(self.id) 
        result = os.popen(cmd)
        list = []
        for i in result.readlines():
            #i = str(i) + " from   " + str(self.id)
            #k = "Point No." +str(self.id) +" value is " + str(i) 
            
                #id = i.spilt(',')
                #print "Recive bacnet device from ",id[0][-2:]
            print i
            if i[0:1] != ';':
                if "Received I-Am Request from" in i:
                    pass
                else:
                    bacid = i[0:6].replace(' ','')
                    shwText = "Probe device : " + i[0:30]
                    label.set_text(shwText)
                    #print "len bac id ", len(bacid)
                    list.append(bacid)
        if len(list) == 0 :
            shwText = "Probe device : Not found !"
            label.set_text(shwText)
        
        state = True
        return list
    
def BacnetListDevice(pbar,label):
    global end_  
    end_  = False
    f = open(r'baclist.txt')
    readDevice = f.read()
    each_point = readDevice.split('},')
    all_list =[]
    #timer = gobject.timeout_add (100, progress_set_text,label,all_list)
    for listpoint in each_point:
        ident_obj = listpoint.split('\n')
        point_dict = {}
        for v in ident_obj:
            if ':' in v:
                k = v.split(':')
                point_dict[k[0].replace(' ','')] = k[1]
        all_list.append(point_dict)
        
            #print v
    #for i in range(4):
        #lines.append(f.readline())
    #for t in all_list:
        #print t['object-type']
    
    '''for b in all_list:
        #print b['object-name']
        shwText = "object device found : " + b['object-name']
        print shwText
        time.sleep(0.5)
        label.set_text(shwText)'''

    end_  = True
    f.close()
    return all_list

class OPCThread(Thread):
    def __init__ (self,widgetPack):
        Thread.__init__(self)
        self.state = widgetPack
        
        
    def run(self):
        self.getOPCDevice(self.state)
        
    def getOPCDevice(self,widgetPack):
        
        print "Get OPC device on network! "
        
        print "Start Read OPC"
        
        
        #print success
        '''for i in range(10):
            time.sleep(1)
            widgetPack['progress'].set_text('Complete '+str(i*10)+'%....')
            widgetPack['label'].set_text(str(i))'''
            
        #print widgetPack
        widgetPack['finish'] = False         # when 'False' is stop  pulse progress bar
        widgetPack['progress'].set_fraction(1) # progress bar
        #widgetPack[2].set_text('Found device complete...') # label under progress bar
        #{'finish':True,'progress':self.pbar,'label':label,'getDevice':device_found}
        
        return True
    
    def warning_dialog(self,MESSAGE):
        dialog = gtk.MessageDialog(None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,MESSAGE)
        dialog.run()
        dialog.destroy()
    
    def checkTagExist(self,list_data,result_device):
        for j in list_data:
            if j == result_device[0]:
                #Show dialog warning 
                message = "Can't add new device because  %s exist." % (j)
                print message
                #self.warning_dialog(message)
                return False
            if list_data[j]['device_id'] == result_device[1]:
                message = "Can't add new device because ID %s exist." % (result_device[1])
                print message
                #self.warning_dialog(message)
                return False
                #end of dialog warning
        return True
    
    def addDeviceInTreeview(self,treeview,treestore,getdevice):
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_parent = tree_model.get_value(iter, 0)
        #print selected_parent
       
        if selected_parent == 'Bacnet IP':
            if iter:
                #result_device =  self.add_dialog(treeview)
                #if result_device is not None:
                #    if self.checkExistTag(result_device):
                #        print "%s pass"% (result_device[0])
                mypiter1 = treestore.append(iter,[getdevice[0]])


class load_opc_server(Thread):
    # This method rotates the position of the tabs

    def __init__ (self):
        Thread.__init__(self)
        '''if list_data is not None:
            print list_data
            print type(list_data)
            title = server_name+' Loading...'
            #for t in data:
            #    title = t + 'OPC Loading...'''

        title = 'Server Unknow Loading...'
        print title
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.connect("delete_event", self.delete)
        #window.connect("destroy", self.delete)
        window.set_border_width(10)
        window.set_title(title)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        window.set_default_size (550, 100)
        window.set_destroy_with_parent(True)
        vbox = gtk.VBox(False, 5)
        
        hbox = gtk.HBox(False, 2)
        
        
        hbox.show()
        vbox.pack_start(hbox, False, False, 5)
        
        
        
        # Create the ProgressBar
        self.pbar = gtk.ProgressBar()
        self.pbar.show()
        self.pbar.set_text('Finding server...')
        hbox.add(self.pbar)
        
        #hbox = gtk.HBox(True, 2)
        #hbox.show()
        self.label = gtk.Label('Browe OPC Server on network: ')
        self.label.show()
        #hbox.add(label)
        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 5)
        layout=gtk.BUTTONBOX_START
        bbox.set_layout(layout)
        bbox.set_spacing(5)
        bbox.add(self.label)
        bbox.show()
        
        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_SPREAD
        bbox.set_layout(layout)
        bbox.set_spacing(10)
        
        self.device_found = []
        self.widgetPack = {'finish':True,'progress':self.pbar,'label':self.label,'getDevice':self.device_found}
        buttonClose = gtk.Button(stock='gtk-close')
       #vbox.pack_start(buttonClose, True, True, 5)
        def close_dialog(self,window,widgetPack):
            #itemPropertySelect.window = None
            widgetPack['finish']= False
            window.destroy()

        buttonClose.connect("clicked", close_dialog,window, self.widgetPack)
        bbox.add(buttonClose)
        buttonClose.show()
        bbox.show()
        
        txt_load =""
        self.finish = False
        state = False
        #timer = gobject.timeout_add (1200, progress_timeout, pbar,label,self.finish)
        
        window.add(vbox)
        vbox.show()
        window.set_modal(True)
        window.show()
        
        print "Window Show"
        # Widget pack send to other class
        
        
        #self.OPCProbe(None,None,1)
    def run(self):
        self.OPCProbe()

    def OPCProbe(self):
        pass
        #timer = gobject.timeout_add (1200, progress_timeout, pbar,label,self.finish)
        #timer = gobject.timeout_add (200, self.pulse_progress, self.label,self.widgetPack)
        #timer1 = gobject.timeout_add (1200, self.getBacnetDevice, label,self.pbar)
        
        #task = self.ReadObject(self.pbar,label)
        #gobject.idle_add(task.next)
        
        
        
        #f = running()
        #print ' OPC Retun Value = ', f.main_read()
        '''time.sleep(1.5)
        getDevcie = OPCThread(widgetPack)
        getDevcie.start()
        time.sleep(1.5)'''
        
        #result = webclient.testCalculator()
        #print 'From response',result

        '''retry = 3
        while retry > 0:
            time.sleep(1)
            f = running()
            ret = f.main_read()
            
            if ret != None:
                print ' OPC Retun Value = ', ret
                break
            else:
                retry = retry -1
            
            print "Retry connect "
                
        if retry == 0 :
            print "Timeout connect"'''
        #print 'return devcie is ',widgetPack['getDevice']
        #return widgetPack['getDevice'] # return list of deivce
    

    def pulse_progress(self,label,widgetPack):
        self.pbar.pulse()
        print "TEST"
        
        if widgetPack['finish'] == False:
            self.pbar.set_fraction(1)
            
        return widgetPack['finish']
        
    def getBacnetDevice(self,label,pbar):
        self.state = True
        print "Get OPC on network! "
        
        #timer1 = gobject.timeout_add (200, self.pulse_progress, label,pbar,self.state)
        
        cmd = "./bacgetid.sh"#run command script for find BACnet device
        result = os.popen(cmd)
        list = []
        for i in result.readlines():
            print i
            if i[0:1] != ';':
                if "Received I-Am Request from" in i:
                    pass
                else:
                    bacid = i[0:6].replace(' ','')
                    shwText = "BACnet device : " + i[0:30]
                    label.set_text(shwText)
                    #print "len bac id ", len(bacid)
                    list.append(bacid)
        if len(list) == 0 :
            shwText = "Probe device : Not found !"
            label.set_text(shwText)
        
        else:
            self.state = False
            
            #time.sleep(3)
            
            #task = self.ReadObject(pbar,label)
            #gobject.idle_add(task.next)
        
        return False
    
    def warning_dialog(self,MESSAGE):
        dialog = gtk.MessageDialog(None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,MESSAGE)
                                    
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.run()
        dialog.destroy()
        
    def ReadObject(self,pbar,label):
        cnt = 0
        
        while cnt<3:
            time.sleep(0.1)
            cnt += 1
            try:
                result = webclient.testCalculator()
                print 'From response',result
            except Exception,e:
                result = e
                self.warning_dialog(str(e))
            label.set_text(str(result))
            yield True
        
        yield False
            
        #return True
        
    

if __name__ == "__main__":
    #label = None
    #getBacnetDevice(label)
    getDevcie = load_opc_server()
    getDevcie.start()
    gtk.main ()
    

    