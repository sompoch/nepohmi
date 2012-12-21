
import os
import gtk, gobject
import time

global state
state = False

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

class progress_bacnet(object):
    # This method rotates the position of the tabs
    
    def delete(self,window,data =None):
        gtk.main_quit()
        return False

    def __init__(self):
        print "initial to get bacnet tag"
        self.list_id = {'Analog Input':'0','Analog Output':'1','Analog Value':'2'}
        self.list_id['Binary Input']   ='3'
        self.list_id['Binary Output']  ='4'
        self.list_id['Binary Value']   ='5'
        #self.get_bacnet_tag()

    def get_bacnet_tag(self,widgetPack):
        
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.connect("delete_event", self.delete)
        #window.connect("destroy", self.delete)
        window.set_border_width(10)
        window.set_title('OPC and Bacnet Loading...')
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        window.set_default_size (550, 100)
        window.set_destroy_with_parent(True)
        vbox = gtk.VBox(False, 5)
        
        hbox = gtk.HBox(False, 2)
        
        
        hbox.show()
        vbox.pack_start(hbox, False, False, 5)
        
        
        
        # Create the ProgressBar
        pbar = gtk.ProgressBar()
        pbar.show()
        pbar.set_fraction(0)
        hbox.add(pbar)
        
        #hbox = gtk.HBox(True, 2)
        #hbox.show()
        label = gtk.Label('Read device property')
        label.show()
        #hbox.add(label)
        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 5)
        layout=gtk.BUTTONBOX_START
        bbox.set_layout(layout)
        bbox.set_spacing(5)
        bbox.add(label)
        bbox.show()
        
        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_SPREAD
        bbox.set_layout(layout)
        bbox.set_spacing(10)
        def close_dialog(self,window):
            #itemPropertySelect.window = None
            print "close dialog"
            window.destroy()
            
        buttonClose = gtk.Button(stock='gtk-close')
       #vbox.pack_start(buttonClose, True, True, 5)
        buttonClose.connect("clicked",  close_dialog,window)
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
        
        # Find BACnet device on network 
        pbar.set_text('Start to read bacnet object...')
        timer = gobject.timeout_add (500, self.getBacnetDevice, label,pbar,widgetPack)
        
      
        
       
        
        #time.sleep(3)
        #self.getBacnetDevice(label,self.finish)
        #state = True
    def pulse_progress(self,label,pbar,state):
        pbar.pulse()
        print state
        return state
        
    def getBacnetDevice(self,label,pbar,widgetPack):
        self.state = True
        print "Get BACnet device on network! "
        
        #timer1 = gobject.timeout_add (200, self.pulse_progress, label,pbar,self.state)
        '''
        widgetPack['device_name'] = selected_device
        widgetPack['device_net'] = self.device_net # keep bacnet data base
        widgetPack['device_id'] = self.device_net[selected_device]['device_id'] # bacnet device id'''
        id =  str(widgetPack['device_id'])
        text = "Read bacnet property on " + widgetPack['device_name']
        label.set_text(text)
        cmd = "./getDeviceProperty.sh "+id + " 8 " + id +" 8 -1" #run command script for find BACnet device
        result = os.popen(cmd)
        
        print cmd
        list = []
        '''for i in result.readlines():
            if 'Error: APDU Timeout' in i:
                print "BACnet device get tag property timeout!\r\n Please retry..."
                return True
            else:
                pass#print i'''
                
        readDevice = result.read()
        if 'Error: APDU Timeout' in readDevice:
            pbar.set_text('Error: APDU Timeout')
            pbar.set_fraction(1)
            shwText =  "BACnet device read property timeout.Please check device exist on network!"
            label.set_text(shwText)
            return False
        else:
            #print readDevice
            #pbar.set_text('Error: APDU Timeout')
            #pbar.set_fraction(1)
            obj_start = readDevice.find('object-list:')
            obj_end = readDevice.find('max-apdu-length-accepted:')

            tag_read = readDevice[obj_start:obj_end].replace('\r','')
            tag_line = tag_read.split('\n')
            tag_list = []
            if len(tag_read)>0:
                for j in tag_line[1:]:
                    tag1 = j[:-1]
                    tag1 = tag1.replace(')','')
                    tag1 = tag1.replace('        (','')
                    #print tag1
                    val = self.point_id(tag1)
                    if val is not None:
                        tag_list.append(val) # object type , object number
                        
            task = self.getBacnetObject(pbar,label,tag_list,widgetPack)
            gobject.idle_add(task.next)
                
            
            #task = self.getBacnetObject(pbar,label)
            #gobject.idle_add(task.next)
                
            
        if len(list) == 0 :
            shwText = "Probe device : Not found !"
            label.set_text(shwText)
        
        else:
            self.state = False
            
            time.sleep(3)
            
            task = self.getBacnetObject(pbar,label)
            gobject.idle_add(task.next)
        
        return False
    
    def point_id(self,bacnet_tag):
        
        sp = bacnet_tag.split(',')
        if len(sp)==2:
            #print '..%s point number..%s' % (sp[0],sp[1]) 
            if self.list_id.has_key(sp[0]):
                point_id = sp[1].replace(' ','')
                return self.list_id[sp[0]],point_id
        
    def getBacnetObject(self,pbar,label,tag_list,widgetPack):
        cnt =1.00
        for v in tag_list:
            pg = float(cnt/len(tag_list))
            #pg_val = float(pg/1.00)
            cnt +=1.00
            
            #print 'progress %s value %s ' % (cnt,pg)
            #cmd = "./getDeviceProperty.sh "+id + " 8 " + id +" 8 -1" #run command script for find BACnet device
            #result = os.popen(cmd)
            id =  str(widgetPack['device_id'])
            arg = id + ' '+v[0]+' '+v[1]+' 77'
            cmd = "./getDeviceValue.sh "+arg #run command script for find BACnet device name
            print "command read bacnet name ",cmd
            result = os.popen(cmd)
            point_name = result.read()
            point_name = point_name.replace('\r\n','')
            point_name = point_name.replace('"','')
            print point_name
            widgetPack['device_net'][widgetPack['device_name']][point_name]=v
            
            pbar.set_fraction(pg)
            p = str(pg*100)[:4] + (' %')
            if p == 1.0 :
                pbar.set_text("Load Complete...")
            else:
                pbar.set_text(p)
                
            lbText = '' + point_name
            label.set_text(lbText)
            time.sleep(0.1) # delay 100 ms
                
            yield True
        
        yield False
        
        
        
        
        '''t = 0
        while t<100:
            time.sleep(0.1)
            t += 2
            v = float(t/100.00)
            pbar.set_fraction(v)
            p = str(v*100) + (' %')
            if v == 1.0 :
                pbar.set_text("Load Complete...")
            else:
                pbar.set_text(p)
            
            label.set_text(p)
            #while gtk.events_pending():
            #    gtk.main_iteration()
            print v
            yield True
        yield False'''
            
        #return True
    
    
            
        
'''
        
if __name__ == "__main__":
    item = None
    progress_bacnet()
    #label = None
    #getBacnetDevice(label)
    gtk.main ()'''
    

    