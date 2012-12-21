#!/usr/bin/python

# ZetCode PyGTK tutorial 
#
# This example shows a menu with
# images, accelerators and a separator
#
# author: jan bodnar
# website: zetcode.com 
# last edited: February 2009

import gtk
import goocanvas, cairo
import glob,os
from layer import *
import global_var
import undo
import drawItem
from displayProperty import *
import nepohmi
import pango
import socket
import threading
import getopt, string, re, sys,gobject
import sqlite3 as lite
from threading import *#Thread
import threading
import multiprocessing

import pickle ,time
import random
from datetime import datetime
from opc_service import opcservice,read_from_socket
from bacnet_client import bacnet_read_tag
from on_running import update_item
from animation import * #animationColor,animationPicker
from group_item import * # from group_item.py
from popup_menu import check_item_raise_below
import pyroweb_client
#from ToolbarTop import open_file
#For wxModule XP,7 Stlye

currentPath = os.getcwd()

if os.name == 'nt':
    from wxPython.wx import *
    import wx
    import OpenOPC

class addAppMenu():
    
    

    def __init__(self,canvas,scrolled_win):
        #super(addAppMenu, self).__init__()
        print "add menu select... get current path is %s " %currentPath 
        #self.set_title("MiniBAS Viewer")
        #self.set_size_request(250, 200)
        #self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(6400, 6400, 6440))
        #self.set_position(gtk.WIN_POS_CENTER)
    def build_main_menu(self,window):
        print 'Set window title '
        window.set_title("Nepo HMI Version 0.0.1 Alpha1 built 1")
        window.set_position(gtk.WIN_POS_CENTER)
    
    def zoom_in(self,widget):
        #global canvas
        #canvas = goocanvas.Canvas ()
        print 'on mouse click zoom in'
        print canvas.get_scale()
        
    def show_Hscroll(self,scrolled_win):
        #global scrolled_win
        #scrolled_win.set_policy(gtk.POLICY_NEVER,gtk.POLICY_NEVER)
        print 'scroll toggle'
        
    def show_font_dialog(self):
        fdia = gtk.FontSelectionDialog("Select font name")
        font = ''
        response = fdia.run()

        if response == gtk.RESPONSE_OK:
           font = fdia.get_font_name()
        
        fdia.destroy()
        return font
    
    def show_about(self):
        about = gtk.AboutDialog()
        about.set_program_name("NepoHMI xGraphic _09.2011 ")
        about.set_version("0.1a")
        about.set_copyright("(c)Sompoch Thuphom , E-mail: mjko68@hotmail.com")
        about.set_comments("SVG xGraphic editor for SCADA System")
        about.set_website("http://nepohmi.sourceforge.net")
        about.set_logo(gtk.gdk.pixbuf_new_from_file("images/icon.png"))
        about.run()
        about.destroy()
        
    def OpenSaveFile(self,type,button):
        if os.name == 'nt':
            
            application = wxPySimpleApp()
            filters = 'xgd files (*.xgd)|*.xgd|All files (*.*)|*.*'

            dialog = wxFileDialog ( None, message = 'Save as XGraphic....', wildcard = filters, style = wxSAVE)

            if dialog.ShowModal() == wxID_OK:
                Files = dialog.GetPaths()
                FileSelect = Files[0]
            else:
               FileSelect = None

            dialog.Destroy()
            
            
        else:
            dialog = gtk.FileChooserDialog("Save as..",
                                           None,
                                           type,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                            button, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            #gtk.FILE_CHOOSER_ACTION_OPEN
            filter = gtk.FileFilter()
            filter.set_name("xgd files")
            filter.add_pattern("*.xgd")
            dialog.add_filter(filter)

            filter = gtk.FileFilter()
            filter.set_name("SVG files")
            filter.add_pattern("*.svg")
            filter.add_pattern("*.SVG")
            dialog.add_filter(filter)
            FileSelect = None
            response = dialog.run()
            if response == gtk.RESPONSE_OK:
                FileSelect = dialog.get_filename()
                FileSelect = FileSelect.replace('.xgd','')
                FileSelect = FileSelect + ".xgd"
            elif response == gtk.RESPONSE_CANCEL:
                print 'Closed, no files selected'
                FileSelect = None
            dialog.destroy()

        return FileSelect
    
    def press_menu_Format(self,addMenu,Data,canvas,scrolled_win):
        if Data =='Display Property':
            print 'Display press'
            print canvas.get_scale()
            showDisplay = displayProperty(canvas,scrolled_win)
    
        
    def file_press(self,addMenu,Data,canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom):
        print 'press' + Data
        if Data == 'New':
            nepohmi.delete_all(canvas)
            global_var.current_doc = "Untitle*"
            global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
            global_var.parent_active = None
            bg = drawItem.startWithBG(canvas)
            
        if Data == 'Save':
            print 'Prepare save document'
            saveAsFile = ToolbarTop()
            #list1 = [widgetPack['canvas']]
            if global_var.current_doc == 'Untitle*':
                global_var.current_doc =  self.OpenSaveFile(gtk.FILE_CHOOSER_ACTION_SAVE,gtk.STOCK_SAVE)
                if global_var.current_doc == None:
                    global_var.current_doc = 'Untitle*'
                    print "Save file cancel"
                else:
                    saveAsFile.save_document(canvas) #call save document
                    global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
                    
            else:
                saveAsFile.save_document(canvas)
                print "Save path file as ",global_var.current_doc
            
        if Data == 'Export':
            print 'Export file export_Xgraphic.svg'
            surface = cairo.SVGSurface ("export_Xgraphic.svg", 5 * 72, 5 * 72)
            cr = cairo.Context (surface)
            ''' Place it in the middle of our 9x10 page. '''
            #cr.translate (20, 130)
            canvas.render (cr, None, 1.0)
            cr.show_page ()
        
        if Data == 'Layer':
            editLayer = LayerPoperty()
        if Data == 'Font':
            font_select = self.show_font_dialog()
            print "Select New Font" + font_select
        if Data == 'About':
            self.show_about()
        if Data =='Open...':
            openDialog = ToolbarTop()
            op = openDialog.open_file()
            if op != None:
                global_var.current_doc = op
                print global_var.current_doc
                nepohmi.delete_all(canvas)
                Itemobject = nepohmi.openGraphicFile(global_var.current_doc)
                nepohmi.loadItemFromFile(canvas,Itemobject,None)
                global_var.parent_active = None
                global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
            
        if Data =='Save as...' :
            global_var.current_doc =  self.OpenSaveFile(gtk.FILE_CHOOSER_ACTION_SAVE,gtk.STOCK_SAVE)
            print "save path file as ",global_var.current_doc
            saveAsFile = ToolbarTop()
            saveAsFile.save_document(canvas)
            global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
        
        if Data == 'Run':
            print 'RUN..'
            if os.name == 'nt':
                global_var.win.unmaximize()
            global_var.mode_run = True
            global_var.menu_run.set_sensitive(False)
            global_var.dialogItemValue['dialog_pos'] =  global_var.dialogProperty.get_position()
            global_var.dialogProperty.hide() # hide dialog box property 
            self._run(canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom)
            #global_var.win.maximize() #set wndow maximize on running
            
                
        
        if Data == 'Stop':
            print 'Stop..'
            if os.name == 'nt':
                global_var.win.unmaximize()
            
            if global_var.mode_run == True:
                
                x0 = global_var.dispProp['cvSizeWidth']
                y0 = global_var.dispProp['cvSizeHeight']- global_var.offset_hsize
                canvas.set_size_request(x0-105,y0) # set size canvas
                
                canvas.props.has_tooltip = False # disable tooltip 
                global_var.mode_run = False
                global_var.menu_run.set_sensitive(True)
                global_var.dialogProperty.show() # show dialog box property 
                last_x = int(global_var.dialogItemValue['dialog_pos'][0])
                last_y = int(global_var.dialogItemValue['dialog_pos'][1])
                global_var.dialogProperty.set_uposition(last_x,last_y) # restore last position of dialog item property
                toolbarTop.show()   
                toolbarLeft.show()
                toolbarButtom.show()
                global_var.mypalette.show()
                global_var.statusbar1.show()
                global_var.toolBarButtom.show()
                scrolled_win.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC) 
                # TODO : when stop reset canvas size to org
                
                self.reset_item_props() # reset defualt item value before run
                global_var.opc_tmp_value.clear()
                #Restore Window Maximize
                #global_var.win.maximize()
                
                
                
            
        if Data == 'Copy':
            drawItem.copyItem_byKey()
        if Data == 'Cut':
            drawItem.copyItem_byKey()
            nepohmi.deleteSelected()
            global_var.bt['Paste'].set_sensitive(True)
        if Data == 'Paste':
            drawItem.pasteItem_byKey(canvas)
            
    def reset_item_props(self):
        for t in global_var.list_item_obj:
            itemData = t.get_data ("itemProp")
            if itemData.has_key('dynamic'):
                pointDynamic = itemData['dynamic']
                if pointDynamic.has_key('Color'):
                    itemSelect = pointDynamic['Color']
                    typeItem =  str(type(itemSelect))
                    if typeItem == '<class \'animation.animationColor\'>':
                        '''if global_var.opc_tag_value.has_key(itemSelect.tag):
                            print itemSelect.chg_fill_color_state,
                            print global_var.opc_tag_value[itemSelect.tag][0]
                            if itemSelect.chg_fill_color_state == global_var.opc_tag_value[itemSelect.tag][0]:
                                t.props.fill_color = itemSelect.fill_color
                            else:'''
                        t.props.fill_color = itemSelect.color_default
                        
                if pointDynamic.has_key('Flash'):
                    itemSelect = pointDynamic['Flash']
                    typeItem =  str(type(itemSelect))
                    if typeItem == '<class \'animation.animationFlash\'>':
                        t.props.fill_color = itemSelect.color_default
                        print 'reset flash item color to defualt ',itemSelect.color_default
                
                if pointDynamic.has_key('Pick'):
                    itemSelect = pointDynamic['Pick']
                    #print 'pre disconnect signal'
                    typeItem =  str(type(itemSelect))
                    if typeItem == '<class \'animation.animationPicker\'>':
                        print 'pre disconnect signal'
                        #t.emit_stop_by_name("leave_notify_event")
                        #t.emit_stop_by_name("enter_notify_event")
                        #global_var.item_signal[list_item] = {}
                        #global_var.item_signal[list_item]['connect']
                        '''t.disconnect(global_var.item_signal[t]['enter_notify_event'])# disable temp for test BACnet
                        t.disconnect(global_var.item_signal[t]['leave_notify_event'])'''
                        #t.disconnect(global_var.item_signal[t]['on_button_press'])
                    
            
        global_var.item_signal.clear()
                 
        return True
    
    
            
    def color_set_cb(colorbutton):
        #global boxcolor
        boxcolor = colorbutton.get_color()
        return boxcolor
            
    def _run(self,canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom):
        scrolled_win.set_policy(gtk.POLICY_NEVER,gtk.POLICY_NEVER)
        toolbarTop.hide() 
        toolbarLeft.hide()
        toolbarButtom.hide()
        #Hide pallete
        global_var.mypalette.hide()
        #Hide scroll window
        global_var.statusbar1.hide()
        global_var.toolBarButtom.hide()
        
        x0 = global_var.dispProp['cvSizeWidth']
        y0 = global_var.dispProp['cvSizeHeight']
        canvas.set_size_request(x0,y0) # set size canvas
        #canvas.set_size_request(1020, 698) 
        #canvas.set_size_request(1024, 722)# auto hide menu ubuntu
        #clear all selection before
        self.clearSelection()
        #get item property when running
        self.get_item_property_before_run(canvas)
        
        
        
        
        
    def get_item_property_before_run(self,canvas):
        #Load prerequsite data before running 
        #TODO : get_item_property_before_run
        #print 'get item property before run...'
        canvas.props.has_tooltip = True # Enable tooltip
        start_point = (canvas.props.x1, canvas.props.y1)
        end_point = (canvas.props.x2, canvas.props.y2)
        bounds = goocanvas.Bounds(*(start_point + end_point))
        overlaped_items = canvas.get_items_in_area(bounds, True, True, True)
        #print start_point,end_point
        #print overlaped_items
        loadItem = []
        typeGrid = '<type \'goocanvas.Grid\'>'
        typeGroup = '<type \'goocanvas.Group\'>'
        
        overlaped_items.reverse()
        opc_get_all = {}
        get_server_from_db = {} #Load temp server name from SQLite tag.db
        #----------------------------------------------------------------
        #Select interface
        type_interface = 'OPC'
        get_server_from_db[type_interface]= {}
        #Load from database
        if type_interface.lower() == 'opc': # If select type interface opc
            #Example: get_server_from_db['OPC']= {}
            query = "SELECT * FROM HOST;"
            host_info = self.connect_db(query,'fetchall')
            for t in host_info:
                #t[0]=id ,t[1] = server alias name , t[2] = server_ip ,t[3] = server_port
                get_server_from_db[type_interface][t[1]] = {}
                get_server_from_db[type_interface][t[1]]['ip'] =  t[2]
                get_server_from_db[type_interface][t[1]]['port'] =  t[3]
                get_server_from_db[type_interface][t[1]]['opc_server_list']=[] # define opc server list 
                #get_server_from_db[type_interface][t[1]]['tag']={}
                
                 
                query = "SELECT OPC_NAME FROM OPC_SERVER_NAME WHERE HOST_ID="+str(t[0])+";"
                find_opc_server = self.connect_db(query,'fetchall')
                for g in find_opc_server:
                    get_server_from_db[type_interface][t[1]]['opc_server_list'].append(g[0])
                    
            
            
        
        #----------------------------------------------------------------
        #
        list0 = []
        full_tag = []
        self.device_net = None # load temp data for bacnet
        #print 'Init Load Item Property...'
        for item_dyn in overlaped_items:
            #print item_dyn
            if str(type(item_dyn)) != typeGrid and str(type(item_dyn)) != typeGroup:
                #don't use grid and group
            #print 'item save...is'
                
                itemData = item_dyn.get_data ("itemProp")
                if itemData.has_key('dynamic'):
                    
                    pointDynamic = itemData['dynamic']
                    if pointDynamic.has_key('Color'):
                        itemSelect = pointDynamic['Color']
                        typeItem =  str(type(itemSelect))
                        if typeItem == '<class \'animation.animationColor\'>':
                            itemSelect.color_default = itemData['color']
                            global_var.list_item_obj.append(item_dyn)
                            if itemSelect.opc_server_name is not None:
                                full_tag.append(itemSelect.tag)
                                self.bind_tag(opc_get_all,itemSelect,item_dyn,typeItem,get_server_from_db)
                                
                    if pointDynamic.has_key('Flash'):
                        itemSelect = pointDynamic['Flash']
                        
                        #print "Flash color read",
                        itemSelect.color_default = itemData['color']
                        typeItem =  str(type(itemSelect))
                        if typeItem == '<class \'animation.animationFlash\'>':
                            #print item_dyn
                            global_var.list_item_obj.append(item_dyn)
                            if itemSelect.opc_server_name is not None:
                                full_tag.append(itemSelect.tag)
                                self.bind_tag(opc_get_all,itemSelect,item_dyn,typeItem,get_server_from_db)

                    if pointDynamic.has_key('Pick'):
                        itemSelect = pointDynamic['Pick']
                        typeItem =  str(type(itemSelect))
                        print "item select"
                        print typeItem
                        if typeItem == '<class \'animation.animationPicker\'>':
                            global_var.list_item_obj.append(item_dyn) # add item on run 
                            # Use tempory for test bacnet
                            print itemSelect.tag
                            if 'Bacnet IP' in itemSelect.tag :
                                if self.device_net == None:
                                    #load bacnet database file:
                                    if os.name == 'nt':# check window os
                                        pathImage = currentPath+ '\\configure\\bacnet_tag.bac'
                                        myload = open(pathImage,'r')
                                    else: # other os , linux
                                        myload = open('configure/bacnet_tag.bac','r')
                                        
                                    self.device_net = pickle.load(myload)
                                    myload.close()
                                else:
                                    print "Bacnet Tag : ",itemSelect.tag
                                    
                                self.bind_bacnet_tag(opc_get_all,itemSelect.tag,item_dyn,typeItem,get_server_from_db)
                                #    bind_bacnet_tag(self,opc_get_all,tag_name,item_dyn):
                            else:
                            #---------------------------------------
                                if itemSelect.opc_server_name is not None:
                                    full_tag.append(itemSelect.tag)
                                    self.bind_tag(opc_get_all,itemSelect,item_dyn,typeItem,get_server_from_db)
                                    name = 'Item has picker'
                                    global_var.item_signal[item_dyn] = {}
                                    global_var.item_signal[item_dyn]['enter_notify_event'] = item_dyn.connect("enter_notify_event", self.on_enter_notify,canvas,name)
                                    global_var.item_signal[item_dyn]['leave_notify_event'] = item_dyn.connect("leave_notify_event", self.on_leave_notify,canvas,name)
                                    #global_var.item_signal[item_dyn]['on_button_press'] = item_dyn.connect("button_press_event", self.on_button_press,canvas)
                            
                    
                    
                        
        #print '#End if load item property'

        refresh_time = 1 # second
        #self.loadOPC_from_local(opc_get_all) # get OPC tag and read from 'localhost'
        
        #older
        '''timer = gobject.timeout_add (refresh_time*2000, self.loadOPC_gateway,opc_get_all)# load opc new value
        timer2 = gobject.timeout_add (refresh_time*1000, self.update_item_on_run,opc_get_all,canvas) # update item tag property
        
        #timer3_bacnet =  gobject.timeout_add (refresh_time*2000, self.bacnetService,opc_get_all)# load opc new value
        #new'''
        
        service_tag = {}
        
        self.bundle_tag(get_server_from_db,service_tag)
        
        # Create tempory database before run
        #-------Service Tag---------------------------
        print "Service tag the comunication to server"
        for s in service_tag:
            for t in service_tag[s]['opc_server']:
                host = service_tag[s]['ip']
                port = service_tag[s]['port']
                
                
        #start run database to read opc process
        
        
        crdb = createRunningDB(full_tag)
        start_temp_db = crdb.create_temp_db()
        
        #----Read current value from database
        database_name = global_var.current_doc.replace(".xgd",'') + "_temp.db"
        con = lite.connect(database_name)
        cur = con.cursor() 
        
        timer = gobject.timeout_add (refresh_time*1000, self.loadOPC_from_local,con,cur)
        #timer2 = gobject.timeout_add (refresh_time*1000, self.update_item_on_run,opc_get_all,canvas)
       
        print 'ON RUN ADD SERVICE ITEM..'
        
        #Disable when bacnet running
        '''for u in opc_get_all:
            print u
            for v in opc_get_all[u]:
                print '       --->',v
                for w in opc_get_all[u][v]:
                    print '             |__',w
                    for x in opc_get_all[u][v][w]:
                        print '                     |__',x'''
        
        return True
    def bind_bacnet_tag(self,opc_get_all,tag_name,item_dyn,typeItem):
        #opc_get_all[tag_name] = item_dyn
        if opc_get_all.has_key(tag_name) == True:
            opc_get_all[tag_name][item_dyn] = typeItem
        else:
        #if  opc_get_all[itemSelect.opc_server_name] == None:
            opc_get_all[tag_name] = {} #OPC_GET_ALL --> OPC_TAG
            opc_get_all[tag_name][item_dyn] = typeItem
            
        return True
        
    def bacnetService(self,opc_get_all):
        if global_var.mode_run:
            #bac = bacnet_read_tag()
            #result = bac.read_tag('test_bacnet sevice')
            #print result
            '''try:
                time.sleep(1)
                print 'connection at %s ' % (time.ctime() ),
                client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
                client.connect ( ( 'localhost', 2728 ) )
                #connect
                #tag_Addr = '3'
                #tag_M =   random.randrange(28,31)
                #tag_Bit = random.randrange(0,8)
                #tag_type = 'BOOL'
                #tag_state = 'W'
                #tag_val = random.randrange(0,2)
                
                #setTag = str(tag_Addr)+',M'+str(tag_M)+'.'+str(tag_Bit)+','+tag_type+','+tag_state+','+str(tag_val)#'3,M30.1,BOOL,W,1'
               
                tag_ =   random.randrange(1,155)
                tag_val = random.randrange(0,2)
                #setTag = 'CoDeSys.OPC.02,PLC_PRG.SW96,R,ALL'
                #setTag = 'CoDeSys.OPC.02,PLC_PRG.SW%s,W,%s' % (tag_,tag_val)
                #setTag = 'S7200.OPCServer$3:0.0.0.0:0000:0000,M30.0,BOOL$R$Reg'
                #print 'OPC Command : %s\n'%setTag,
                #client.send (setTag)
                tag_read = ['Channel_1.Device_2.Bool_0','Channel_1.Device_2.Bool_2']
                
                pack_send = ['KEPware.KEPServerEx.V4',tag_read,'R','None']
                
                pickledList = pickle.dumps (pack_send)
                client.sendall ( pickledList )
                
                
                
                Rinput = True
                data = ''
                
                timeout = False
                set_count = 50
                #while timeout == False:
                while Rinput:
                    if not data: # if end of data, leave loop
                        break
                    Rinput = client.recv (4096)
                    data += Rinput
                    

                list =  pickle.loads(data)
                
                #print list[23]
                for rd in list:
                    print list
                    print type(list)
                    #print type(rd)
                client.close()
                #print '...close'
                
            except Exception,e:
                print 'error ',e'''
                
            for tag in opc_get_all:
                #load any item in tag
                for animationItem in opc_get_all[tag]:
                    t1 = tag.split('.')
                    print 'tag before read  ',t1
                    if self.device_net.has_key(t1[1]):
                        # call bacnet server
                        
                        bac_id = str(self.device_net[t1[1]]['device_id'])
                        tag_id = self.device_net[t1[1]][t1[2]]
                        cmd = "./readValue.sh " + bac_id + " " + tag_id[0] + " " + tag_id[1] + " 85"
                        print cmd
                        result = os.popen(cmd)
                        value = result.read()
                        #value = []
                        #for i in result.readlines():
                        #    print str(i)
                        #    value.append(str(i))
                        #print result
                        animationItem.props.text = value
                
            print 'bacnet service running'
        else:
            
            for tag in opc_get_all:
                for animationItem in opc_get_all[tag]:
                    animationItem.props.text = '?????' # reset value
            print 'bacnet service stop...'
            self.device_net = None
            
        return global_var.mode_run
    
    def connect_db(self,query,fetch):
        database_name = "tag.db"
        con = lite.connect(database_name)
        cur = con.cursor() 

        #get opc server id 
        #query = "SELECT Id FROM OPC_SERVER_NAME WHERE OPC_NAME=\'"+opc_name+"\' AND HOST_ID="+str(host_id)+";"
        print query
        cur.execute(query)
        if fetch == 'fetchone':
            result = cur.fetchone()
        else:
            result = cur.fetchall()
            
        return result
        
        
    
    def bind_tag(self,opc_get_all,itemSelect,item_dyn,typeItem,get_server_from_db):
        
        #TODO : bind_tag
        #Bing tag structor 
        #OPC----|{OPC Alias Name No1}-|--opc_server_list={}
        #                             |--server_ip
        #                             |--server_port
        #
        #
        #BACnet-|{Device Name}--------|--device_id
        
        
        
        
        
        #
        
        select_ = itemSelect.tag.split('.')
        if len(select_)>2:
            '''print "--------------------------------------------------------"
            print "Full tag ",itemSelect.tag
            print "TYPE INTERFACE    \t: " ,select_[0]
            print "SERVER ALIAS NAME \t: ",select_[1]'''
            #print "TAG ITEM = ",select_[2]
            type_interface = select_[0] #Etc OPC,BAcnet,Modbus,XML,Other
            server_alias_name = select_[1] #The server alias name must exist from tag.db
            str_opc_alias = type_interface+'.'+server_alias_name
            sep_tag =  itemSelect.tag.replace(str_opc_alias,"")
            
            if get_server_from_db.has_key(type_interface): #Check type interface has exist?
                if get_server_from_db[type_interface].has_key(server_alias_name): # Check dictionary has server alias name
                    if type_interface.lower() == 'opc':
                        #print "Server name is ",server_alias_name
                        
                        '''print "SERVER IP     \t\t\t\t\t: ",get_server_from_db[type_interface][server_alias_name]['ip'] 
                        print "SERVER PORT   \t\t\t\t\t: ",get_server_from_db[type_interface][server_alias_name]['port'] '''
                        list_server = get_server_from_db[type_interface][server_alias_name]['opc_server_list']
                        for n in list_server:
                            if n in sep_tag:
                                
                                real_tag = sep_tag.split(n+".")
                                '''print "OPC SERVER NAME   \t: \t",n
                                print "TAG               \t: \t",real_tag[1]'''
                                if get_server_from_db[type_interface][server_alias_name].has_key(n):#Found opc server name key
                                    print "opc sever name \'%s\' not exist try to add to dictionary " % (n)
                                else:
                                    #type_interface     = Interface driver such as OPC,Backnet,XML,Modbus and Oher by user custom protocol driver.
                                    #server_alias_name  = The name of host you can modifier for easy to remember
                                    #n                  = opc servername : etc KEPware , PCAccess , and Other
                                    #'tag'              = keep all opc tag in server has found on opcBrowe.py and save it into tag.db before use them.
                                    #item_dyn           = Item dynamic 
                                    #typeItem           = Class dynamic such as Flash , Picker , Color 
                                    
                                    get_server_from_db[type_interface][server_alias_name][n]={}
                                    get_server_from_db[type_interface][server_alias_name][n]['tag']={}
                                    
                                if get_server_from_db[type_interface][server_alias_name][n]['tag'].has_key(real_tag[1]):
                                    if get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]].has_key(item_dyn):
                                        get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]].append(typeItem)
                                    else:
                                        get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]][item_dyn]=[]
                                        get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]][item_dyn].append(typeItem)
                                    
                                else:
                                    
                                    get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]] = {}
                                    get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]][item_dyn]=[]
                                    get_server_from_db[type_interface][server_alias_name][n]['tag'][real_tag[1]][item_dyn].append(typeItem)
                else:
                    print "Can't add server alias name to dictionary because not found on database"
                    #get_server_from_db[type_interface][server_alias_name]
                
            else: # Create new dictionary for type_interface OPC,BAcnet,Modbus,XML,Other
                print "Not found !"
                            #get_server_from_db[type_interface][t[1]]['tag'][real_tag[1]][item_dyn].append(typeItem)
                            
        
        
        '''if opc_get_all.has_key(itemSelect.opc_server_name) == True:
            if opc_get_all[itemSelect.opc_server_name].has_key(itemSelect.tag) == True:
                if opc_get_all[itemSelect.opc_server_name][itemSelect.tag].has_key(item_dyn) == True:
                    opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn].append(typeItem)
                    
                else:
                    opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn] = []
                    opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn].append(typeItem)
                    
            else:
                opc_get_all[itemSelect.opc_server_name][itemSelect.tag] = {}#ADD OPC TAG FIRST
                opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn] = []
                opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn].append(typeItem) 
        else:
        #if  opc_get_all[itemSelect.opc_server_name] == None:
            opc_get_all[itemSelect.opc_server_name] = {} #OPC_GET_ALL --> OPC_TAG
            opc_get_all[itemSelect.opc_server_name][itemSelect.tag] = {}#ADD OPC TAG FIRST
            print "Tag use opc name ",itemSelect.tag
            opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn] = []
            opc_get_all[itemSelect.opc_server_name][itemSelect.tag][item_dyn].append(typeItem)'''
            
        #return True
    
    def on_button_press (self,item, target, event,canvas):
        print 'item press'
    
    def on_enter_notify(self,item, target, event,canvas,name):
        #on_enter_notify(item, target, event,canvas,cursor_name):
        item.props.stroke_color = "yellow"
        item.props.line_width = 3
        #print 'Item Focus IN na ja!'
        
    def on_leave_notify(self,item, target, event,canvas,name):
        item.props.stroke_color = "black"
        item.props.line_width = 1
        #print 'Item Focus OUT na ja!'
    
    def update_item_on_run(self,item_dyn_obj,canvas):
        #print 'List item to update'
        #print 'Lenght of item ',len(item_dyn_obj)
        #for u in item_dyn_obj:
        #    print u
        current_update = update_item()#on_running.py
        _on_update = current_update.update_on_running(item_dyn_obj,canvas)
        return _on_update
        
    def loadOPC_gateway(self,opc_get_all):#load OPC gateway for linux ,win32
        #print 'Load test opc...'
        for opc in opc_get_all:
            #print opc,
            opcservice(opc,opc_get_all[opc],'R').start() # call opcservice from opc_service.py
            
            #mysck = read_from_socket()
            #t = mysck.readOPCSocket(opc,opc_get_all[opc])
            
            
            #for u in opc_get_all[opc]:
            #    print '     |--->',u
        #display opc value
        '''print '####### Display Loading OPC Data ##########'
        opc_val = global_var.opc_tag_value
        for i in opc_val:
            print '%-40s : %-s' % (i,opc_val[i])'''
            
        return global_var.mode_run # return false when mode stop
        # For continouse repeat time return True
        
    def bundle_tag(self,tag_from_db,service_tag):
        
        for type_interface in tag_from_db:
            print "*******************************************"
            print "INTERFACE NAME \t: ",type_interface#tag_from_db[type_interface]
            for y in tag_from_db[type_interface]:
                print "Alias Name     \t: ",y#tag_from_db[type_interface][y]
                print "IP             \t: ",tag_from_db[type_interface][y]['ip']
                print "Port           \t: ",tag_from_db[type_interface][y]['port']
                print "Bind tag       \t: "

                for k in tag_from_db[type_interface][y]['opc_server_list']:
                    if tag_from_db[type_interface][y].has_key(k):
                        if service_tag.has_key(y):
                            pass
                        else:
                            service_tag[y]={}
                            service_tag[y]['ip'] = tag_from_db[type_interface][y]['ip']
                            service_tag[y]['port'] = tag_from_db[type_interface][y]['port']
                            service_tag[y]['opc_server'] = {}
                            
                        if service_tag[y]['opc_server'].has_key(k):
                            pass
                        else:
                            service_tag[y]['opc_server'][k] = {}
                            service_tag[y]['opc_server'][k]['tag'] = []
                            
                        
                        
                        for x in tag_from_db[type_interface][y][k]['tag']:
                            print "OPC NAME       \t: ",k
                            print "               \t\t\t\t|--> ",x
                            
                            service_tag[y]['opc_server'][k]['tag'].append(x)
                            
                            for h in tag_from_db[type_interface][y][k]['tag'][x]:
                                print "               \t\t\t\t   |--> ",h
                                for p in tag_from_db[type_interface][y][k]['tag'][x][h]:
                                    print "               \t\t\t\t      |--> ",p
                                    print " "
        
    def loadOPC_from_local(self,con,cur):
        #opc_get_all= (type interface[OPC,Bacnet,Etc] , {tag:{goocavas.object.class_animation}})
        #this service to read OPC item from server every 1-2 second 
        #pyro is remote object use in this section 
        #print "Len opc get all ",len(opc_get_all)
        #TODO : load OPC from local
        #Tag bunch of them together before sending the data to the OPC server. 
        

        
        print "************************"
        start_read = time.clock()
        query = "SELECT * FROM ITEM"
        cur.execute(query)
        read_tag = cur.fetchall()
        for t in read_tag:
            print t
            
        query = "SELECT time_refresh FROM TIMEOUT"
        cur.execute(query)
        process_alive = cur.fetchone()
        print "Time alive ",process_alive[0]
        if process_alive == None or process_alive[0]<5:
            query = "UPDATE TIMEOUT SET time_refresh=?"
            print query
            cur.execute(query,(str(10),))
            con.commit()
        else:
            print "Process time alive = ",process_alive
            
        print "Time use =  ",(time.clock()-start_read)
        
                
                #p = multiprocessing.Process(target=pyroweb_client.opc_read(host,port,t,service_tag[s]['opc_server'][t]['tag'],10,global_var.opc_tag_value))
                #p.daemon = True
                #p.start()
        
                #start_service = ThreadService(host,port,t,service_tag[s]['opc_server'][t]['tag'],10,global_var.opc_tag_value)
                #start_service.setName("Thread_OPC")
                #start_service.start()
                #data_result =  pyroweb_client.opc_read(host,port,t,service_tag[s]['opc_server'][t]['tag'])
        '''if data_result != "Time out":
            for rd in data_result:
                tagRead = 'OPC.'+s+'.'+rd[0]
                tag_val = (str(rd[1]),rd[2],rd[3])
                global_var.opc_tag_value[tagRead]=tag_val'''
        #for t in global_var.opc_tag_value:
            #print "Tag : %s Value % s " % (t,global_var.opc_tag_value[t])
            #print opc_get_all[opchost]
            
            
            
            
        '''opc = OpenOPC.client() # set opc client mode
        opc.connect(opchost) # set connect opc
        opcTagList = opc_get_all[opchost]
        tag_data = []
        for u in opcTagList:
            tag_data.append(u)
        try:
            data= opc.read(tag_data,group = 'group_tag')
            for rd in data:
                tagRead = rd[0]
                tag_val = (str(rd[1]),rd[2],rd[3])
                global_var.opc_tag_value[tagRead]=tag_val
                print  global_var.opc_tag_value[tagRead]
            print data
        except Exception ,e:
            print e
        #while global_var.mode_run:'''
        ''' try:
                #time.sleep(2)
                data= opc.read(group = 'group_tag')
                print 'data'
            except Exception ,e:
                print e'''
                    
            #opc.close
            #print 'opc service stop...',opchost
            #read_opc_local(opc,opc_get_all[opc],'R').start() # call opcservice from opc_service.py
        if global_var.mode_run == False:
            con.close()
        return global_var.mode_run
        #return True
    
    def clearSelection(self):
        print 'Clear all selection before RUN mode'
        lenMultiBox = len(global_var.multiBoxMoveSelect)
        #This function like press key ESCAPE on nepohmi define on  on_key_press
        if lenMultiBox ==0:
            for t in global_var.multiSelect:
                for j in range(8):
                    global_var.itemSelect8Cursor[t][j].remove()
                    
            lenGroup = len(global_var.multiSelect)
            del global_var.multiSelect[0:(lenGroup)]

            # cancle to move item
            global_var.box_select = None
            global_var.itemSelectActive = None
        else:
            for k in range(lenMultiBox):
                global_var.multiBoxMoveSelect[k].remove()
            del global_var.multiBoxMoveSelect[0:len(global_var.multiBoxMoveSelect)]
    
    def create_menu(self,canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom):
        print 'Create menu'
        
        #global item_select # value of select item
        #print 'print select item staus = ',item_select 
        mb = gtk.MenuBar()

        filemenu = gtk.Menu()
        filem = gtk.MenuItem("File")
        filem.set_submenu(filemenu)
        menuList = ['New','Open...','Save','Save as...','sep','Export','sep',
                            'Print','Print Preview','Print Setup','sep']
        for j in menuList:
            if j != 'sep':
                addMenu = gtk.MenuItem(j)
                addMenu.connect("activate", self.file_press,j,canvas,None,None,None,None)
                filemenu.append(addMenu)
            else:
                sep = gtk.SeparatorMenuItem()
                filemenu.append(sep)
        
        exit = gtk.MenuItem("Exit")
        exit.connect("activate", nepohmi.exit_,None)#gtk.main_quit
        filemenu.append(exit)
        #----------------------------------------------------
        # Create Edit menu
        submenu = gtk.Menu()
        EditMenu = gtk.MenuItem("Edit")
        EditMenu.set_submenu(submenu)
        menuList = ['Undo','Redo','sep',
                            'Cut','Copy','Paste','Delete','sep',
                            'Select All','Delete All','sep',
                            'Find','Replace','Report']
        for j in menuList:
            if j != 'sep':
                addMenu = gtk.MenuItem(j)
                addMenu.connect("activate", self.file_press,j,canvas,None,None,None,None)
                submenu.append(addMenu)
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
        #----------------------------------------------------
        filemenuView= gtk.Menu()

        menuView = gtk.MenuItem("View")
        menuView.set_submenu(filemenuView)
        
        mZoomIn = gtk.MenuItem("Zoom In")
        #mZoomIn.connect("activate",show_Hscroll)
        filemenuView.append(mZoomIn)
        
        mZoomOut = gtk.MenuItem("Zoom Out")
        mZoomOut.connect("activate", gtk.main_quit)
        filemenuView.append(mZoomOut)
        
        mHorizontal = gtk.CheckMenuItem("Show HScroll")
        mHorizontal.connect("activate", self.show_Hscroll)
        filemenuView.append(mHorizontal)
        
        mVertical = gtk.CheckMenuItem("Show VScroll")
        #mZoomOut.connect("activate", gtk.main_quit)
        filemenuView.append(mVertical)
        
        showDialog = gtk.CheckMenuItem("Property Window")
        showDialog.connect("activate", self.showDialogWindow)
        filemenuView.append(showDialog)
        
        #--------------------------------------------------------
        #----------------------------------------------------
        # Create Format menu
        submenu = gtk.Menu()
        FormatMenu = gtk.MenuItem("Format")
        FormatMenu.set_submenu(submenu)
        menuList = ['Template','Layer','Password','sep',
                            'Background Color','Fill Color','Line Color','Line width','Line Style','Toggle Fill','Toggle Fressze','Font','sep',
                            'Display Property','Reset Defualt Display Property','sep',
                            'Application Preference','Reset Application Preference']
        for j in menuList:
            if j != 'sep':
                addMenu = gtk.MenuItem(j)
                addMenu.connect("activate", self.press_menu_Format,j,canvas,scrolled_win)
                submenu.append(addMenu)
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
                
        #----------------------------------------------------
        
        
        
        # Create Arrange menu
        submenu = gtk.Menu()
        ArrangeMenu = gtk.MenuItem("Arrange")
        ArrangeMenu.set_submenu(submenu)
        menuList = ['Group Item','Ungroup Item','sep',
                            'Bring To Front','Send To Back','Bring Forward','Send Backward','sep',
                            'Rotate/Flip','Free Rotate','sep',
                            'Align','Space']
        for j in menuList:
            if j != 'sep':
                if j == 'Rotate/Flip':
                    addMenu = gtk.MenuItem(j)
                    rotateMenu =  gtk.Menu()
                    addMenu.set_submenu(rotateMenu)
                    
                    listrotate = ['Rotate Left','Rotate Right','Flip Vertical','Flip Horizontal']
                    for k in listrotate:
                        rotate = gtk.MenuItem(k)
                        rotate.connect("activate", self.file_press,k)
                        rotateMenu.append(rotate)
            
                    rotateMenu.show()
                    submenu.append(addMenu)   
                    
                else:
                    addMenu = gtk.MenuItem(j)
                    addMenu.connect("activate", self.file_press,j)
                    submenu.append(addMenu)                    

            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
        #----------------------------------------------------
        #--------------------------------------------------------
        # Create Draw menu
        submenu = gtk.Menu()
        DrawMenu = gtk.MenuItem("Draw")
        DrawMenu.set_submenu(submenu)
        menuList = ['Select Item','sep',
                            'Rectangle','Ellipse','Curve','Polyline','Text','Line','Image Insert','Pan','sep']
                         
        st = None
        groupItem = [st]
        v =0
        for j in menuList:
            if j != 'sep':
                addMenu = gtk.RadioMenuItem(groupItem[v],j,True)
                groupItem.append(addMenu)
                addMenu.connect("activate", self.file_press,j)
                submenu.append(addMenu)
                v = v+1
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
        
        addMenu = gtk.MenuItem("Import")
        addMenu.connect("activate",self.file_press,"Import")
        submenu.append(addMenu)
        
        addMenu = gtk.MenuItem("Export")
        addMenu.connect("activate",self.file_press,"Export")
        submenu.append(addMenu)
        #----------------------------------------------------
        # Create Dynamic menu
        submenu = gtk.Menu()
        DynamicMenu = gtk.MenuItem("Dynamic")
        DynamicMenu.set_submenu(submenu)
        menuList = ['Action','Seclector','sep',
                            'Local Variables']
        for j in menuList:
            if j != 'sep':
                if j == 'Action':
                    addMenu = gtk.MenuItem(j)
                    actionMenu =  gtk.Menu()
                    addMenu.set_submenu(actionMenu)
                    
                    listaction = ['Size','Location/Slider','Rotation','Hide/Disable','Color','Analog Color','Flash','Pick']
                    for k in listaction:
                        action = gtk.MenuItem(k)
                        action.connect("activate", self.action_dynamics,k)
                        actionMenu.append(action)
                    submenu.append(addMenu)
                
                else:
                    if j == 'Seclector':
                        addMenu = gtk.MenuItem(j)
                        actionMenu =  gtk.Menu()
                        addMenu.set_submenu(actionMenu)
                        
                        listaction = ['Digital Selector','Analog Selector','Animator']
                        for k in listaction:
                            action = gtk.MenuItem(k)
                            action.connect("activate", self.file_press,k)
                            actionMenu.append(action)
                        submenu.append(addMenu)
                        
                    else:
                        addMenu = gtk.MenuItem(j)
                        addMenu.connect("activate", self.file_press,j)
                        submenu.append(addMenu)
                    
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
                
        #----------------------------------------------------
        # Create Tool menu
        submenu = gtk.Menu()
        ToolMenu = gtk.MenuItem("Tool")
        ToolMenu.set_submenu(submenu)
        menuList = ['Allias','Script','Export HTML','sep',
                            'Symbol','sep']
        for j in menuList:
            if j != 'sep':
                addMenu = gtk.MenuItem(j)
                addMenu.connect("activate", self.file_press,j)
                submenu.append(addMenu)
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
                
        #----------------------------------------------------
        # Create Run menu
        submenu = gtk.Menu()
        RunMenu = gtk.MenuItem("Run")
        RunMenu.set_submenu(submenu)
        menuList = ['Run','Stop','Pause','sep']
        for j in menuList:
            if j != 'sep':
                
                addMenu = gtk.MenuItem(j)
                if j == 'Run':
                    global_var.menu_run = addMenu
                addMenu.connect("activate", self.file_press,j,canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom)
                submenu.append(addMenu)
            else:
                sep = gtk.SeparatorMenuItem()
                submenu.append(sep)
        #------------Help----------------------------------------
        menuHelp = gtk.Menu()
        
        mHelp = gtk.MenuItem('Help')
        mHelp.set_submenu(menuHelp)
        
        mAbout = gtk.MenuItem("About")
        mAbout.connect("activate", self.file_press,'About',canvas,scrolled_win,None,None,None)
        #file_press(self,addMenu,Data,canvas,scrolled_win,toolbarTop,toolbarLeft,toolbarButtom):
        menuHelp.append(mAbout)
        #filem = gtk.MenuItem("View")
        #filem.set_submenu(filemenu)

        mb.append(filem)
        mb.append(EditMenu)
        mb.append(menuView)
        mb.append(FormatMenu)
        mb.append(ArrangeMenu)
        mb.append(DrawMenu)
        mb.append(DynamicMenu)
        mb.append(ToolMenu)
        mb.append(RunMenu)
        mb.append(mHelp)
        
        return mb
    
    def showDialogWindow(self,widget):
        print "click show dialog window"
        global_var.dialogProperty.show()
        last_x = int(global_var.dialogItemValue['dialog_pos'][0])
        last_y = int(global_var.dialogItemValue['dialog_pos'][1])
        global_var.dialogProperty.set_uposition(last_x,last_y) # restore last position of dialog item property
    
    def action_dynamics(self,widget,Data):
        itemprop = global_var.itemSelectActive.get_data ('itemProp')
        dynamic = itemprop['dynamic'] # {}dictionary keep item action when run mode
        # ['Size','Location/Slider','Rotation','Hide/Disable','Color','Analog Color','Flash','Pick']
        if dynamic.has_key(Data):
            print '%s is already exist'
        else:
            itemprop['dynamic'][Data] = self.dynamicDataProperty(Data,itemprop)
            global_var.itemSelectActive.set_data ('itemProp',itemprop)
            #print 'pre add color...'
            
    def dynamicDataProperty(self,Data,itemprop):
        dyndata = None
        if Data == 'Color':
            dyndata = animationColor(name = 'myname',
                                        tag = 'OPC_DA2.0',
                                        fill_color = '#cc3300',
                                        color_default = itemprop['color'],
                                        line_color = 'black') # link to data structure [animation.py]
                                        
        if Data == 'Flash':
            dyndata = animationFlash(name = 'Flash Item',
                                        tag = 'OPC_DA2.0',
                                        fill_color = '#cc3300',
                                        refresh_rate = 100) # millisecond to refresh Bilnk

        if Data == 'Pick': # item pressing 
            dyndata = animationPicker(name = 'item_press',
                                        tag = 'OPC_DA2.0',
                                        type = 'Toggle')
                                        
        return dyndata
        
    
class ToolbarLeft():
    def __init__(self):
        print 'initial creat left toolbar'
        
    def builtLeftToolbar(self,canvas):
        vbox = gtk.VBox(False, 0)
        handlebox = gtk.HandleBox()
        handlebox.set_handle_position(gtk.POS_RIGHT)
        handlebox.set_shadow_type(gtk.SHADOW_OUT)
        
        '''bbox = gtk.HButtonBox()
        bbox.set_border_width(0)
        bbox.add(handlebox)
        bbox.set_layout(gtk.BUTTONBOX_START)'''
        
        vbox.pack_start(handlebox, False, False, 0)
        
        # toolbar will be horizontal, with both icons and text, and
        # with 5pxl spaces between items and finally, 
        # we'll also put it into our handlebox
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_VERTICAL)#gtk.ORIENTATION_HORIZONTAL,gtk.ORIENTATION_VERTICAL
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        toolbar.set_border_width(0)
        toolbar.set_icon_size(gtk.ICON_SIZE_BUTTON)
        handlebox.add(toolbar)

        pathImage = ''
        if os.name == 'nt':# check window os
            pathImage = currentPath+ '\\images\\'
        else: 
            pathImage = currentPath+ '/images/'
        
        #pathImage = '/home/sompoch/pro/minibas/images/'
        
        iconList1  = ['SelectionMode.gif','CreateRect.gif','CreateEllipse.gif','CreateCurve.gif','CreatePoly.gif', 
                            'line.gif','text.gif','ImportImage.gif','pan.gif']
        tooltip = ['SelectionMode','CreateRect','CreateEllipse','CreateCurve','CreatePoly',
                            'line','text','ImportImage','pan'] 
                            
        lenList = len(iconList1)
        widget = None
        
        for i in range(lenList):
            iconpath = pathImage + iconList1[i]
            #bt_data = [tooltip[i],i,canvas,window]
            bt_data = {}
            bt_data['tooltip'] = tooltip[i]
            bt_data['index'] = i
            bt_data['canvas'] = canvas
            global_var.bt_left[tooltip[i]]=self.addToolRadio(toolbar,iconpath,widget,bt_data)
            widget = global_var.bt_left[tooltip[i]]
        

        toolbar.show()
        handlebox.show()
        return vbox
    
    def open_file(self):
                
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        default_path = global_var.image_import_default_path
        dialog.set_current_folder(default_path)




        filter = gtk.FileFilter()
        filter.set_name("Images")
        filter.add_mime_type("image/png")
        filter.add_mime_type("image/jpeg")
        filter.add_mime_type("image/gif")
        filter.add_mime_type("image/bmp")
        filter.add_pattern("*.png")
        filter.add_pattern("*.jpg")
        filter.add_pattern("*.gif")
        filter.add_pattern("*.tif")
        filter.add_pattern("*.xpm")
        filter.add_pattern("*.bmp")
        dialog.add_filter(filter)
        
        filter = gtk.FileFilter()
        filter.set_name("All files")
        filter.add_pattern("*")
        dialog.add_filter(filter)
        
        FileSelect = None
        
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            FileSelect = dialog.get_filename()
            global_var.image_import_default_path = dialog.get_current_folder()
            
        elif response == gtk.RESPONSE_CANCEL:
            global_var.image_import_default_path = dialog.get_current_folder()
            print 'Closed, no files selected'
            
        dialog.destroy()

        return FileSelect
    
    def clearAllSelection(self):
        
        for t in global_var.multiSelect:
            for j in range(8):
                global_var.itemSelect8Cursor[t][j].remove()
            
        lenGroup = len(global_var.multiSelect)
        #print 'old group item select %s' %  lenGroup
        if lenGroup>0:
            del global_var.multiSelect[0:(lenGroup-1)]
        
        lenGroupCursor = len(global_var.itemSelect8Cursor)        
        if lenGroupCursor>0:
            global_var.itemSelect8Cursor.clear()
            
        '''for itemSelect in global_var.select_cursor :
                    # remove select cursor area
            global_var.select_cursor[itemSelect].remove()'''
    
    def press_event(self,widget,data):
        #if self.button2.get_active(): 
        #    "press button1 MoveOneDown"
        #print "%s was toggled %s" % (data[0], ("OFF", "ON")[widget.get_active()])
        if widget.get_active() == True:#  and data[0] == 'CreateRect' :
            global_var.cmd_draw = data['index'] 
            
            print 'Sample to Create %s and change mode index to %s ' % (data['tooltip'],str(global_var.cmd_draw))
            if data['tooltip'] == 'SelectionMode':
                data['canvas'].window.set_cursor(gtk.gdk.pointer_ungrab()) # data[3] = gtk.window
                #gtk.gdk.LEFT_PTR
                for itemSelect in global_var.select_cursor :
                    # remove select cursor area
                    global_var.select_cursor[itemSelect].remove()
                #self.clearAllSelection()
               
            if data['tooltip'] == 'CreateRect':
                if global_var.itemSelectActive is not None:
                    data['canvas'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TCROSS))
                    #tcross = gtk.gdk.Cursor(gtk.gdk.TCROSS)#change mouse cursor to move icon
                    #data[2].pointer_grab(None, # data[2] = canvas 
                    #    gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                    #    tcross, event.time)
                        
                    global_var.itemSelectActive.props.stroke_color = "black" # line color
                    
                for itemSelect in global_var.select_cursor :
                    global_var.select_cursor[itemSelect].remove()
                    
            if data['tooltip'] == 'CreateEllipse':
                if global_var.itemSelectActive is not None:
                    data['canvas'].window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TCROSS))
                    #tcross = gtk.gdk.Cursor(gtk.gdk.TCROSS)#change mouse cursor to move icon
                    #data[2].pointer_grab(None, # data[2] = canvas 
                    #    gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                    #    tcross, event.time)
                        
                    global_var.itemSelectActive.props.stroke_color = "black"
                    
                for itemSelect in global_var.select_cursor :
                    global_var.select_cursor[itemSelect].remove()
                
            
            if data['tooltip'] == 'ImportImage':
                
                pathFile =  self.open_file()
                print "Import Image Path ",pathFile
                drawItem.ImportDropImage(pathFile,data['canvas']) # call Import Image Function
                #pathFile = '/home/sompoch/pro/t_gee-power_en.gif'
                global_var.bt_left['SelectionMode'].set_active(True)
                
            if data['tooltip'] == 'text':
                data['canvas'].window.set_cursor(gtk.gdk.pointer_ungrab()) # data[3] = gtk.window
                #gtk.gdk.LEFT_PTR
                for itemSelect in global_var.select_cursor :
                    # remove select cursor area
                    global_var.select_cursor[itemSelect].remove()
        #Creat rectange 
      
    def button_press(self,widget,data=None):
        #if self.button2.get_active(): 
        #    "press button1 MoveOneDown"
        print data
    

    def addToolRadio(self,toolbar,iconPath,widget,data): # name = DATA
        iconw = gtk.Image() # icon widget
        iconw.set_from_file(iconPath)
        '''close_button = toolbar.append_item(
            "Close",           # button label
            "Create Rectangle", # this button's tooltip
            "Private",         # tooltip private info
            iconw,             # icon widget
            self.press_event) # a signal
        #toolbar.append_space() # space after item'''
        radio_button = toolbar.append_element(
            gtk.TOOLBAR_CHILD_RADIOBUTTON, # type of element
            widget,                          # widget
            "Icon",                        # label
            data['tooltip'],       # tooltip
            "Private",                     # tooltip private string
            iconw,                         # icon
            self.press_event,          # signal
            data)    
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        # now, let's make our radio buttons group...
        return radio_button
    
    def addIconBottom(self,toolbar,iconPath,widget,tooltip):
        iconw = gtk.Image() # icon widget
        iconw.set_from_file(iconPath)
        icon_button = toolbar.append_element(
            gtk.TOOLBAR_CHILD_BUTTON, # type of element
            widget,                          # widget
            "Icon",                        # label
            tooltip,       # tooltip
            tooltip,                     # tooltip private string
            iconw,                         # icon
            self.button_press,          # signal
            tooltip)  
              
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        
        # now, let's make our radio buttons group...
        return icon_button
    
class ToolbarTop():
    def __init__(self):
        print 'initial creat left bottom toolbar'
        
    def createToolbarTop(self,canvas,scrolled_win):
        print 'read scale canvas ' + str(canvas.get_scale())
        handlebox = gtk.HandleBox()
        handlebox.set_handle_position(gtk.POS_LEFT)
        handlebox.set_shadow_type(gtk.SHADOW_OUT)

        # toolbar will be horizontal, with both icons and text, and
        # with 5pxl spaces between items and finally, 
        # we'll also put it into our handlebox
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)#gtk.ORIENTATION_HORIZONTAL,gtk.ORIENTATION_VERTICAL
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        toolbar.set_border_width(0)
        toolbar.set_icon_size(gtk.ICON_SIZE_BUTTON)
        handlebox.add(toolbar)

        widget = None
        '''iconpath  ='/home/sompoch/pro/minibas/images/NewDocument.gif'
        #iconpath = icon_image.set_from_stock(gtk.STOCK_NEW,gtk.ICON_SIZE_SMALL_TOOLBAR)
        
        button1 = self.addIconTop(toolbar,iconpath,widget,"New File")
        self.button1 = button1
        iconpath = '/home/sompoch/pro/minibas/images/Open.gif'
        button2 = self.addIconTop(toolbar,iconpath,widget,"Open File")
        #MoveToBottom.gif
        iconpath = '/home/sompoch/pro/minibas/images/Save.gif'
        button3 = self.addIconTop(toolbar,iconpath,widget,"Save File")
        iconpath = '/home/sompoch/pro/minibas/images/SaveAs.gif'
        button4 = self.addIconTop(toolbar,iconpath,widget,"Save as")'''
        
        pathImage = ''
        if os.name == 'nt':# check window os
            pathImage = currentPath+ '\\images\\'
        else: 
            pathImage = currentPath+ '/images/'
        
        #pathImage = '/home/sompoch/pro/minibas/images/'
        iconList1  = ['NewDocument.gif','Open.png','SaveAs.png','printer.png','sep', 
                            'Copy.gif','Cut.gif','Paste.gif','Delete.gif','sep',
                            'Undo.gif','Redo.gif','sep', 
                            'zoom_in.png','zoom_out.png','zoom_0.png']
        tooltip = ['New File','Open File','Save File','Printer','sep',
                            'Copy','Cut','Paste','Delete','sep', 
                            'Undo','Redo','sep',
                            'ZoomIn','ZoomOut','Fit to Original Size']
        lenList = len(iconList1)

        for i in range(lenList):
            iconpath = pathImage + iconList1[i]
            if iconList1[i] != 'sep':
                global_var.bt[tooltip[i]]=self.addIconTop(toolbar,iconpath,widget,tooltip[i],canvas,scrolled_win)
            else:
                
                toolbar.append_space()
        global_var.bt['Redo'].set_sensitive(False)
        global_var.bt['Undo'].set_sensitive(False)
        global_var.bt['Paste'].set_sensitive(False)
        global_var.bt['Save File'].set_sensitive(True)
        global_var.bt['Delete'].set_sensitive(False)
        #toolbar.append_space()
        #print 'Len of bt = ' + str(len(bt))
        '''iconpath = '/home/sompoch/pro/minibas/images/SaveAs.gif'
        button4 = self.addIconTop(toolbar,iconpath,widget,"Save as")'''
        #Create Zoom Percent In Combobox
        vbox = gtk.VBox(True, 0)
        #combobox = gtk.combo_box_new_text()
        
        global_var.comboboxZoom.set_size_request(80, 25)
        style = gtk.rc_parse_string('''
                style "my-style" { GtkComboBox::appears-as-list = 1 }
                widget "*.mycombo1" style "my-style"
        ''')
        global_var.comboboxZoom.set_name('mycombo1')
        global_var.comboboxZoom.set_style(style)
        #change combo box font size 
        #font_desc = pango.FontDescription("sans 12")
        #font_desc = "sans 32"
        #global_var.comboboxZoom.modify_font(font_desc)
        vbox.pack_end (global_var.comboboxZoom, False, False, 0)  
        toolbar.append_widget(vbox,"Zoom percent","Selection")
        zoomList = [10,15,25,75,100,110,125,150,200,250,300,400,450,500,600]
        for zoom in zoomList :
            global_var.comboboxZoom.append_text(str(zoom)+'%')
            global_var.comboboxZoom.set_active(4)
        vbox.show()
        global_var.comboboxZoom.connect('changed',self.comboZoom_select,zoomList,canvas)
        
        toolbar.append_space()
        
        #creat font on combo box
        vbox = gtk.VBox(True, 0)
        combobox = gtk.combo_box_new_text()
        style = gtk.rc_parse_string('''
                style "my-style" { GtkComboBox::appears-as-list = 1 }
                widget "*.mycombo" style "my-style"
        ''')
        combobox.set_name('mycombo')
        combobox.set_style(style)
        combobox.set_size_request(160, 25)
        vbox.pack_end (combobox, False, False, 0)  
        vbox.show()
        
        if os.name != 'nt':
            # add font list for linux and other
            startfolder = '/usr/share/fonts/truetype/*'
            filelist=[]   
            filenamelist=[]
            for folder in glob.glob(startfolder):
                if os.path.isdir(folder):
                    #print "folder =", folder
                    filemask = folder + '/*.ttf'
                    #print filemask
                    for filename in glob.glob(filemask):
                        #print filename
                        filelist.append(filename)
                        filesplit = filename.rsplit('/',1)
                        filesplit[1] = filesplit[1].replace('.ttf','')
                        findResult1 = filesplit[1].find('Bold')
                        findResult2 = filesplit[1].find('Italic')
                        if findResult1 == -1 and  findResult2 == -1 :
                            filenamelist.append(filesplit[1])
        else:
            #load font from win32
            app = wx.App(False)
            e = wx.FontEnumerator()
            e.EnumerateFacenames()
            filenamelist= e.GetFacenames()
                        
        filenamelist.sort()
        lenfont = len(filenamelist)
        for i in range(lenfont):
            combobox.append_text(filenamelist[i])
                
        
        combobox.set_active(10)
        toolbar.append_widget(vbox,"Font","Selection")
        
        #Creat font size box 

        style = gtk.rc_parse_string('''
                style "my-style" { GtkComboBox::appears-as-list = 1 }
                widget "*.mycombo2" style "my-style"
        ''')
        vbox = gtk.VBox(True, 0)
        combobox = gtk.combo_box_new_text()
        combobox.set_size_request(60, 25)
        combobox.set_name('mycombo2')
        combobox.set_style(style)
        
        vbox.pack_end (combobox, False, False, 0)  
        vbox.show()
        combobox.show()
        for i in range(8,45,4):
            combobox.append_text(str(i))
        combobox.set_active(0)
        #combobox.set_relief(gtk.RELIEF_NONE)
        toolbar.append_widget(vbox,"Font Size","Selection")
        toolbar.show()
        handlebox.show()
        return handlebox
    
    def comboZoom_select(self,widget,zoomList,canvas):
        index  = widget.get_active()
        selct = widget.get_active_text()
        selct =  selct.replace('%','')
        scale_adjust = float(selct)#float(zoomList[index])
        scale_new =scale_adjust/100
        canvas.set_scale(scale_new)
        print 'new canvas scale select = ' + str(canvas.get_scale())
        print widget.get_active_text()
        model = widget.get_model()
        current_scale = canvas.get_scale()*100
        model[0][0]= str(int(current_scale))+'%'
        self.auto_cursor_scale(current_scale)
        return True
    
    def addIconTop(self,toolbar,iconPath,widget,tooltip,canvas,scrolled_win):
        widgetPack = {'canvas':canvas,'tooltip':tooltip,'scrolled_win':scrolled_win}
        iconw = gtk.Image() # icon widget
        iconw.set_from_file(iconPath)
        icon_button = toolbar.append_element(
            gtk.TOOLBAR_CHILD_BUTTON, # type of element
            widget,                          # widget
            "Icon",                        # label
            tooltip,       # tooltip
            tooltip,                     # tooltip private string
            iconw,                         # icon
            self.press_event,widgetPack)         # signal
            
              
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        
        # now, let's make our radio buttons group...
        return icon_button
    
    def press_event(self,widget,widgetPack):
        global bt
        tooltip = widgetPack['tooltip']
        #canvas = widgetPack['canvas']
        print tooltip
        
        if tooltip == 'Open File':
            op = self.open_file()
            if op != None:
                global_var.current_doc = op
            
                nepohmi.delete_all(widgetPack['canvas'])
                Itemobject = nepohmi.openGraphicFile(global_var.current_doc)
                nepohmi.loadItemFromFile(widgetPack['canvas'],Itemobject,None)
                global_var.parent_active = None
                global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
                
            else:
                print "File open cancel"

        if tooltip == 'ZoomIn':
            current_Scale =  widgetPack['canvas'].get_scale() # canvas = widgetPack['canvas']
            print current_Scale
            current_Scale = current_Scale + 0.1
            widgetPack['canvas'].set_scale(current_Scale)
            model = global_var.comboboxZoom.get_model()
            current_scale = current_Scale*100
            model[0][0]= str(int(current_scale))+'%'
            global_var.comboboxZoom.set_active(0)
            #Undo Event 
            undo.undoListStore(global_var.undoList,'ZoomIn',model[0][0],None,None)
            global_var.bt['Undo'].set_sensitive(True)
            self.auto_cursor_scale(current_Scale)
            

            
        if tooltip == 'ZoomOut':
            current_Scale =  widgetPack['canvas'].get_scale()
            #print current_Scale
            current_Scale = current_Scale - 0.1
            widgetPack['canvas'].set_scale(current_Scale)
            model = global_var.comboboxZoom.get_model()
            current_scale = current_Scale*100
            model[0][0]= str(int(current_scale))+'%'
            global_var.comboboxZoom.set_active(0)
            #Undo Event 
            undo.undoListStore(global_var.undoList,'ZoomOut',model[0][0],None,None)
            global_var.bt['Undo'].set_sensitive(True)
            self.auto_cursor_scale(current_Scale)# auto adjust cursor size on zoom button 
            
        if tooltip == 'Fit to Original Size':
            widgetPack['canvas'].set_scale(1.0)
            model = global_var.comboboxZoom.get_model()
            current_Scale = '100'
            model[0][0]= str(int(current_Scale))+'%'
            global_var.comboboxZoom.set_active(0)
            #reset scroll to zero
            hadj = widgetPack['scrolled_win'].get_hadjustment()#get_hadjustment()
            hadj.set_value(0)
            vadj = widgetPack['scrolled_win'].get_vadjustment()#get_hadjustment()
            vadj.set_value(0)
            #Undo Event 
            undo.undoListStore(global_var.undoList,'Fit to Original Size',model[0][0],None,None)
            global_var.bt['Undo'].set_sensitive(True)
            self.auto_cursor_scale(1)# auto adjust cursor size on zoom button 
            
        if tooltip == 'Undo':
            global_var.bt['Redo'].set_sensitive(True)
            index_undo = global_var.index_select_undo+1
            lenOfUndo = len(global_var.undoList)-1
            print 'Len of Undo  ' + str(lenOfUndo) + '    Undo Index Select =  ' + str(index_undo)
            if index_undo < lenOfUndo:
                print global_var.undoList[index_undo][0:4]
                global_var.index_select_undo = index_undo  # Update new value
                
            else:
                global_var.bt['Undo'].set_sensitive(False)
            
            #index_select_undo = index_select_undo + 1
            
        if tooltip == 'Redo':
            global_var.bt['Undo'].set_sensitive(True)
            index = global_var.index_select_undo -1
            lenOfundo = len(global_var.undoList)
            
            if index < lenOfundo and index >=0:
                global_var.index_select_undo = index
                print global_var.undoList[global_var.index_select_undo][0:4]
            else:
                global_var.bt['Redo'].set_sensitive(False)
                
        if tooltip == 'Delete':
            if global_var.itemSelectActive != None :
                for itemSelect in global_var.select_cursor :
                    global_var.select_cursor[itemSelect].remove()
                
                undo.undoListStore(global_var.undoList,'Delete Item',None,global_var.itemSelectActive,None)
                prop = global_var.itemSelectActive.get_data('itemProp')
                if prop['main'] == 'ImageItem':
                    imagIndex = prop['image_name']
                    list_cnt = global_var.image_use[imagIndex]
                    if list_cnt < 2:
                        del global_var.image_use[imagIndex]
                        del global_var.image_store[imagIndex]
                    else:
                        global_var.image_use[imagIndex] = list_cnt-1
                        
                #global_var.image_use[imag_name] = 1
                global_var.itemSelectActive.remove()
                print 'Delete Item from tool button'
                global_var.itemSelectActive = None
                global_var.bt['Undo'].set_sensitive(True)
                global_var.bt['Delete'].set_sensitive(False)
            
        if tooltip =='Copy':
            '''lencopy = len(global_var.clipboard)
            while lencopy:
                lencopy = len(global_var.clipboard)
                global_var.clipboard.remove(0)'''
            global_var.clipboard = None
            global_var.bt['Paste'].set_sensitive(True)
            drawItem.copyItem_byKey()
        
        if tooltip =='Cut':

            drawItem.copyItem_byKey()
            nepohmi.deleteSelected()
            global_var.bt['Paste'].set_sensitive(True)
            #global_var.itemSelectActive.remove()
            print 'Cut Item from tool button'
            #global_var.itemSelectActive = None
            #global_var.itemSelectActive.props.visibility =goocanvas.ITEM_INVISIBLE # Hide item
            #global_var.bt['Paste'].set_sensitive(True)
            
            
            
        
        if tooltip =='Paste':
            #global_var.itemSelectActive.props.visibility = goocanvas.ITEM_VISIBLE # Show item
            #global_var.bt['Paste'].set_sensitive(False)
            #print global_var.clipboard
            #drawItem.createRect(widgetPack['canvas'],global_var.clipboard)
            #global_var.itemSelectActive.props.visibility = goocanvas.ITEM_VISIBLE
            drawItem.pasteItem_byKey(widgetPack['canvas'])
            #global_var.clipboard = None
            
        if tooltip == 'New File':
            nepohmi.delete_all(widgetPack['canvas'])
            global_var.current_doc = "Untitle*"
            global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
            bg = drawItem.startWithBG(widgetPack['canvas'])
            
        if tooltip =='Printer':
            #print widgetPack['canvas'].props.y2
            hadj = widgetPack['scrolled_win'].get_hadjustment()#get_hadjustment()
            vadj = widgetPack['scrolled_win'].get_vadjustment()#get_hadjustment()
            print 'scroll adj value = %s , %s ' % (hadj.get_value(),vadj.get_value())
            print 'scroll lower value = %s , %s ' % (hadj.get_lower(),vadj.get_lower())
            print 'scroll upper value = %s , %s ' % (hadj.get_upper(),vadj.get_upper())

            #global_var.itemSelectActive.props.visibility =goocanvas.ITEM_INVISIBLE
        # TODO : Save Item 
        if tooltip == 'Save File':
            self.pre_saveDocument(widgetPack['canvas'])
            '''print 'Prepare save document'
            #list1 = [widgetPack['canvas']]
            if global_var.current_doc == 'Untitle*':
                opensavaDialog = addAppMenu(None,None)
                global_var.current_doc =  opensavaDialog.OpenSaveFile(gtk.FILE_CHOOSER_ACTION_SAVE,gtk.STOCK_SAVE)
                if global_var.current_doc == None:
                    global_var.current_doc = 'Untitle*'
                    print "Save file cancel"
                else:
                    self.save_document(widgetPack['canvas'])
                    global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
                    
            else:
                self.save_document(widgetPack['canvas'])
                print "Save path file as ",global_var.current_doc'''
            #self.save_document(widgetPack['canvas'])
            #Clear all temp
            #del saveItemList,overlaped_items,listToSave
            
            #del list1
            #widgetPack['canvas']
    def pre_saveDocument(self,canvas):
        if global_var.current_doc == 'Untitle*':
                opensavaDialog = addAppMenu(None,None)
                global_var.current_doc =  opensavaDialog.OpenSaveFile(gtk.FILE_CHOOSER_ACTION_SAVE,gtk.STOCK_SAVE)
                if global_var.current_doc == None:
                    global_var.current_doc = 'Untitle*'
                    print "Save file cancel"
                else:
                    self.save_document(canvas)
                    global_var.win.set_title('Nepo HMI  '+ global_var.current_doc)
        else:
            self.save_document(canvas)
            print "Save path file as ",global_var.current_doc
            
    def save_document(self,canvas):
        
        #watch = gtk.gdk.Cursor(gtk.gdk.WATCH)
        #global_var.win.set_cursor(watch)
        
        for itemSelect in global_var.select_cursor :
            global_var.select_cursor[itemSelect].remove()

        start_point = (canvas.props.x1, canvas.props.y1)
        end_point = (canvas.props.x2, canvas.props.y2)
        bounds = goocanvas.Bounds(*(start_point + end_point))
        overlaped_items = canvas.get_items_in_area(bounds, True, True, True)
        #print start_point,end_point
        #print overlaped_items
        saveItemList = []
        #for u in overlaped_items:
            #y = str(type(u))
            #print y
            #if y == '<type \'goocanvas.Group\'>':
                #print 'group type...'
        typeGrid = '<type \'goocanvas.Grid\'>'
        typeGroup = '<type \'goocanvas.Group\'>'
        
        overlaped_items.reverse()
        img_use = []
        for save_item in overlaped_items:
            if str(type(save_item)) != typeGrid and str(type(save_item)) != typeGroup:
                #print 'item save...is'
                parent_of_root,parent = return_parent_root(save_item)
                if parent_of_root == None : # check item is not under group 
                    #print save_item
                    # Find current posiotn of each item
                    updata = self.update_current_pos_item(save_item,img_use)
                    #print updata['x'],updata['y'],
                    #print type(updata) 
                    saveItemList.append(updata)# Add item on list
                    print "append item on group ! type" , save_item
                     
                    #print updata
                
            else:
                
                print "item save under group "
                if str(type(save_item)) == typeGroup:
                    
                    print "save group item ",save_item
                    updata = save_item.get_data('itemProp')
                    if updata is not None:
                        print updata
                        if updata['main'] == 'group Item':
                            parent_of_root,parent = return_parent_root(save_item)
                            if parent_of_root == None :
                        #--list --
                        #---------dict [0] keep group property 
                        #---------dict [1] keep item under group property 
                        #--------- .......
                                n = save_item.get_n_children()
                                if n>0:
                                    list = []
                                    updata = self.update_current_pos_item(save_item,img_use)# group 
                                    list.append(updata)
                                    self.save_group_item(save_item,list,img_use)# item on group
                                    saveItemList.append(list)
                                    print "append item on group"
            #del update
            #print saveItem[len(overlaped_items)-j]['x'],saveItem[len(overlaped_items)-j]['y']

        #print saveItemList
        #print "--------------------------"
        #for hk in saveItemList:
        #   print hk
        #del saveItemList[2]
        print 'Store Item = ' + str(len(saveItemList))
        print "save file name ",global_var.current_doc
        file_name = open(global_var.current_doc, 'wb') 
        # Save Image object to File(String)
        #pathFile = '/media/DATA/Sompoch Thuphom/My Pictures/68176-1.png'
        dic = {}
        for img in global_var.image_store:
            if img in img_use: # filter image using only for save to disk
                filename = 'tmp'
                #print 'Format image = '+global_var.image_store[img].pixbuf_get_formats()
                typImage = global_var.image_store[img][1]
                if typImage == 'png':
                    #print 'save png format'
                    global_var.image_store[img][0].save(filename, typImage)
                else:
                    if typImage == 'gif' or typImage == 'xpm' : # Change gif to png format
                        #print 'save png format from gif or xpm'
                        global_var.image_store[img][0].save(filename, 'png')
                        typImage = 'png'
                    else:
                        global_var.image_store[img][0].save(filename, typImage, {"quality":"100"})
                #"tEXt::key"
                i = open('tmp','rb')
                i.seek(0)
                w = i.read()
                #print 'length of image file = '+ str(len(w))
                i.close()
                dic[img]=[w,typImage]
        
        print "**** Print Image Dic Store *****"
        global_var.image_use.clear()
        for h in img_use:
            global_var.image_use[h] =1
            print h
            
        print "End of dic image store *******"

        listToSave = [saveItemList,dic,global_var.image_use]
        pickle.dump(listToSave, file_name) 
        file_name.close()
        
        
            
    def auto_cursor_scale(self,current_Scale):
        global_var.canvas_scale = current_Scale
        for select in global_var.itemSelect8Cursor:
            drawItem.update_new_round_item(select,current_Scale)
            
            
    def save_group_on_group(self,item,img_use):
        list1 = []
        n = item.get_n_children()
        for i in range(n):
            get_item = item.get_child(i)
            m = get_item.get_n_children()
            if m > 0:
                updata = self.update_current_pos_item(get_item,img_use)# group 
                list1.append(updata)
                list1.append(self.save_group_on_group(get_item,img_use))
            else:
                updata = self.update_current_pos_item(get_item,img_use)
                list1.append(updata)
            
        return list1
            
    def save_group_item(self,group_item,list,img_use):
        n = group_item.get_n_children()
        
        print "Child item on group is ",n 
        for i in range(n):
            item = group_item.get_child(i)
            m = item.get_n_children()
            if m > 0:
                list2 = []
                updata = self.update_current_pos_item(item,img_use)# group 
                list2.append(updata)
                self.save_group_item(item,list2,img_use)# item on group
                #list2.append(self.save_group_on_group(item))
                list.append(list2)
            else:
                updata = self.update_current_pos_item(item,img_use)
                list.append(updata)
            
        return True
            
    def update_current_pos_item(self,save_item,img_use):
        sx,sy,scale_,degree = save_item.get_simple_transform() # get current item transform 
        updata = save_item.get_data('itemProp')
        updata['x'] = save_item.props.x
        updata['y'] = save_item.props.y
        updata['width'] = save_item.props.width
        updata['height'] = save_item.props.height
        updata['line_width'] = save_item.props.line_width
        updata['transform_x'] = sx
        updata['transform_y'] = sy
        updata['scale'] = scale_
        updata['degree'] = degree
            
        if updata.has_key('image_name'):
            if updata['image_name'] in img_use:
                pass # if image aready in list
            else:
                img_use.append(updata['image_name'])
            
        if updata['main'] == 'Rect Item':
            updata['radius_x'] = save_item.props.radius_x
            updata['radius_y'] = save_item.props.radius_y
        
        if updata['main'] == 'Ellipse Item':
            #print "found ellipse item when save"
            updata['radius_x'] = save_item.props.radius_x
            updata['radius_y'] = save_item.props.radius_y
            updata['center_x'] = save_item.props.center_x
            updata['center_y'] = save_item.props.center_y
            
        if updata['main'] == 'Text Item':
            updata['buffer'] = save_item.props.text
            #print save_item,
            #print "x = %s , y = %s radius x = %s radius y = %s center x = %s  center y = %s " % (updata['x'],updata['y'],updata['radius_x'] ,updata['radius_y'] ,updata['center_x'],updata['center_y']  )
            
        return updata
        
        
    def open_file(self):
        if os.name == 'nt':
            application = wxPySimpleApp()
            filters = 'xgd files (*.xgd)|*.xgd|All files (*.*)|*.*'

            dialog = wxFileDialog ( None, message = 'Open XGraphic....', wildcard = filters, style = wxOPEN)

            if dialog.ShowModal() == wxID_OK:
               Files = dialog.GetPaths()
               FileSelect = Files[0]
            else:
               FileSelect = None

            dialog.Destroy()
            
        else:
            dialog = gtk.FileChooserDialog("Open..",
                                           None,
                                           gtk.FILE_CHOOSER_ACTION_OPEN,
                                           (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                            gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            dialog.set_default_response(gtk.RESPONSE_OK)
            filter = gtk.FileFilter()
            filter.set_name("XGD|SVG files")
            filter.add_pattern("*.xgd")
            filter.add_pattern("*.svg")
            dialog.add_filter(filter)
            FileSelect = 'no file selected'
            response = dialog.run()
            
            if response == gtk.RESPONSE_OK:
                FileSelect = dialog.get_filename()
            elif response == gtk.RESPONSE_CANCEL:
                print 'Closed, no files selected'
                FileSelect = None
            dialog.destroy()

        return FileSelect
        
    #return gtk.Window
class ToolbarBottom():
    def __init__(self):
        print 'initial creat left bottom toolbar'
        
    def createToolbarBottom(self):
        
        handlebox = gtk.HandleBox()
        handlebox.set_handle_position(gtk.POS_LEFT)
        handlebox.set_shadow_type(gtk.SHADOW_OUT)

        # toolbar will be horizontal, with both icons and text, and
        # with 5pxl spaces between items and finally, 
        # we'll also put it into our handlebox
        toolbar = gtk.Toolbar()
        toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)#gtk.ORIENTATION_HORIZONTAL,gtk.ORIENTATION_VERTICAL
        toolbar.set_style(gtk.TOOLBAR_ICONS)
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        toolbar.set_border_width(0)
        toolbar.set_icon_size(gtk.ICON_SIZE_BUTTON)
        handlebox.add(toolbar)

        
        pathImage = ''
        if os.name == 'nt':# check window os
            pathImage = currentPath+ '\\images\\'
        else: 
            pathImage = currentPath+ '/images/'
            
        toolbar.append_space()
        iconpath = pathImage + 'MoveOneDown.gif'
        widget = None
        button1 = self.addIconBottom(toolbar,iconpath,widget,"MoveOneDown")
        self.button1 = button1
        iconpath = pathImage + 'MoveOneUp.gif'
        button2 = self.addIconBottom(toolbar,iconpath,widget,"MoveOneUp")
        #MoveToBottom.gif
        iconpath = pathImage + 'MoveToBottom.gif'
        button3 = self.addIconBottom(toolbar,iconpath,widget,"MoveToBottom")
        iconpath =pathImage +'MoveToTop.gif'
        button4 = self.addIconBottom(toolbar,iconpath,widget,"MoveToTop")
        toolbar.append_space()
        
        '''combobox = gtk.combo_box_new_text()
        combobox.append_text('Select a pie:')
        combobox.append_text('Apple')
        combobox.append_text('Cherry')
        combobox.append_text('Blueberry')
        combobox.append_text('Grape')
        combobox.append_text('Peach')
        combobox.append_text('Raisin')
        #combobox.connect('changed', self.changed_cb)
        combobox.set_active(0)
        toolbar.append_widget(combobox,"Rotate","Selection")'''
        
        toolbar.show()
        handlebox.show()
        return handlebox
    
    def addIconBottom(self,toolbar,iconPath,widget,tooltip):
        iconw = gtk.Image() # icon widget
        iconw.set_from_file(iconPath)
        icon_button = toolbar.append_element(
            gtk.TOOLBAR_CHILD_BUTTON, # type of element
            widget,                          # widget
            "Icon",                        # label
            tooltip,       # tooltip
            tooltip,                     # tooltip private string
            iconw,                         # icon
            self.press_event,          # signal
            tooltip)  
              
        toolbar.set_icon_size(gtk.ICON_SIZE_SMALL_TOOLBAR)
        
        # now, let's make our radio buttons group...
        return icon_button
    
    def press_event(self,widget,data = None):
        #print data,
        print '   toolbar press bottom !'
        if data == 'MoveToBottom':
            check_item_raise_below(None,global_var.itemSelectActive2,'below') # call def popup_menu.py 
        if data == 'MoveToTop':
            check_item_raise_below(None,global_var.itemSelectActive2,'raise')
        if data == 'MoveOneUp':
            check_item_raise_below(None,global_var.itemSelectActive2,'oneUp')
        if data == 'MoveOneDown':
            check_item_raise_below(None,global_var.itemSelectActive2,'oneDown')




class read_opc_local():
    def __init__(self,opc_server_name,tag,opt):
        print '****initial read OPC Local service****'
        
        self.options = {}
        self.options['opc_server_name'] = opc_server_name
        self.options['tag'] = tag
        self.options['state'] = opt
        #print 'initial opc service running...'
        #threading.Thread.__init__ (self)
        
    def run ( self ):
        print 'running opc...'
        self.myopc()
        
    def myopc(self):
        print 'my opc'
        opchost = self.options['opc_server_name'] # read local opc
        opc = OpenOPC.client() # set opc client mode
        opc.connect(opchost) # set connect opc
        opcTagList = self.options['tag'] 
        tag_data = []
        for u in opcTagList:
            tag_data.append(u)
        print 'type opc tag ',type(tag_data)
        data= opc.read(tag_data,group = 'group_tag')
       
        #while global_var.mode_run:
        ''' try:
                #time.sleep(2)
                data= opc.read(group = 'group_tag')
                print 'data'
            except Exception ,e:
                print e'''
                
        opc.close
        print 'opc service stop...'
        #return True
#addAppMenu()
#gtk.main()

class ThreadService(Thread):
    def __init__ (self,host,port,opc_server_name,tag_read,time_out,opc_get_value):
        Thread.__init__(self)
        self.host = host
        self.port = port
        self.opc_server_name = opc_server_name
        self.tag_read = tag_read
        self.time_out = time_out
        self.opc_get_value = opc_get_value
        
    #def start(self):
    #    """Start the thread."""
    #    threading.Thread.start(self)
    #    print "Thread read service with pyro start"
        
    def run(self):
        data_result =  pyroweb_client.opc_read(self.host,self.port,self.opc_server_name,self.tag_read,self.time_out,self.opc_get_value)
        
class createRunningDB():
    def __init__(self,list_tag):
        print "create running database..."
        self.list_tag = list_tag

        
    def create_temp_db(self):
        
        database_name = global_var.current_doc.replace(".xgd",'') + "_temp.db"
        if not os.path.isfile(database_name):
            print "File temporary database is not exist ",database_name
            
        con = lite.connect(database_name)
        cur = con.cursor() 
        query ="SELECT name FROM sqlite_master WHERE type='table' AND name='ITEM';"
        cur.execute(query)
        result = cur.fetchall()
        print result
        
        if len(result) == 0 :#table name has not exist
            print "Create temp file when project running"
            cur.execute("CREATE TABLE ITEM(id INTEGER PRIMARY KEY,tag text,value text,time_stamp text,quality text,timeout int);")
            cur.execute("CREATE TABLE TIMEOUT(id INTEGER PRIMARY KEY,time_refresh int);")
            query = "INSERT INTO TIMEOUT(time_refresh) VALUES (10);"
            cur.execute(query)
        else:
            query = "DELETE FROM ITEM;"
            cur.execute(query)
            con.commit()
            con.close()
            
        # Insert new item
        self.insert_item(self.list_tag)
        
    def insert_item(self,list_tag):
        database_name = global_var.current_doc.replace(".xgd",'') + "_temp.db"
        con = lite.connect(database_name)
        cur = con.cursor() 
        for t in list_tag:
            print "Insert tag value >> ",t
            query = "INSERT OR REPLACE INTO ITEM(tag,timeout,value) VALUES (\'"+t+"\',10,\"\");"
            cur.execute(query)
        con.commit()
        con.close()
            
    
        
            #Create new table

        
