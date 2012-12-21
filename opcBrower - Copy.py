#!/usr/bin/env python
#'This OPC and BACnet Browser service'
#Version 0.1 update 17.7.2011

import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pickle
import os
import string
import global_var
import webclient #load ladon web service
import pyroweb_client
import time
import sqlite3 as lite
import sys

import opcBrower
import global_var

from bacnet_find_device import bacnet_device
from progress_bacnet import progress_bacnet
from progress_find_opc import load_opc_server

if os.name == 'nt':
    import OpenOPC
    
'''
Read first
Tag database keep in "self.tagList"
This format support list 

self.tagList is type dictionary for keep all data opc tag

self.tagList
            |---selected_parent
                              |---selected_item
                                               |--property 
                                                          |--ip


selected_parent = [Bacnet IP,OPC,Local,Modbus,Simulate,XML]


example:
self.tagList[selected_parent][selected_item]['property']['ip']

'''

widgetPack = {}
tagItem = ['Command Door Unlock ','Disable Push Button'
                ,'Door Left  Alarm','Door Status','Force Door Alarm'
                ,'Open Time Alarm Delay','Output Lock State','Push Button Status']
                
tagItem.sort()
currentPath = os.getcwd()
subItem1={}
for j in range(20):
    if j<10:
        d = 'FL2-Door0'+str(j)
    else:
        d = 'FL2-Door'+str(j)
    subItem1[d] = tagItem

subItem2 = {}
for j in range(20,40):
    d = 'FL3-Door'+str(j)
    subItem2[d] = tagItem

device = {} 
device['PLC Bldg A FL2'] = subItem1
device['PLC Bldg A FL3'] = subItem2
device['PLC Bldg B FL2'] = subItem1
device['PLC Bldg B FL3'] = subItem2

(
    COLUMN_FIXED,
    COLUMN_DESCRIPTION
) = range(2)

global select_server_opc
select_server_opc = []


class getOpcItem(object):
    # This method rotates the position of the tabs
    # call from dynamic.py 
    def delete(self, window):
        gtk.main_quit()
        return False
    
    

    def __init__(self,item,widget_pack_ret):

        self.opcWindow(item,widget_pack_ret)

    def add_child_tag(self,iter,treestore,list,type_tag):
        for v in list:
            print v
            iter1 = treestore.append(iter, [v])
            
            if str(type(list)) != '<type \'str\'>':
                if list[v] is not None and type_tag == 'OPC':
                    print 'add opc'
                    self.loadOPCtoTreeView(iter1,None,treestore,list[v])
                    
                if list[v] is not None and type_tag == 'Bacnet IP':
                    self.loadBacnettoTreeView(iter1,None,treestore,list[v])
                    
                if list[v] is not None and type_tag == 'Local':
                    self.loadLocaltoTreeView(iter1,None,treestore,list[v])
                    
        return True
    
    def add_device_manual(self,widget,treeview, treestore):
        #print self.device_net
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_parent = tree_model.get_value(iter, 0)
        #print selected_parent
       
        if selected_parent == 'Bacnet IP':
            if iter:
                result_device =  self.add_dialog(treeview)
                if result_device is not None:
                    if self.checkTagExist(result_device):
                        print "%s pass"% (result_device[0])
                        mypiter1 = treestore.append(iter,[result_device[0]])
                        self.tagList['Bacnet IP'][result_device[0]] = {}
                        self.tagList['Bacnet IP'][result_device[0]]['device_id'] = result_device[1]
                        self.buttonApply.set_sensitive(True)
                        #mypiter1 = treeStore.append(None, result_device[1])
                        # refresh list 
                        #for h in self.device_net:
                        #    print h
                    else:
                        print "not pass"
                        
        if selected_parent == 'OPC':
            if iter:
                init_  = {}
                init_['opc server name'] = 'PC1'
                init_['ip'] = 'localhost'
                init_['port'] = '7540'
                
                add_result =  self.add_dialog_opc(treeview,init_)
                if add_result is not None:
                    print add_result
                    if self.tagList['OPC'].has_key(add_result[0]) == False:
                        print "add OK ",add_result[0]
                        mypiter1 = treestore.append(iter,[add_result[0]])
                        self.tagList['OPC'][add_result[0]] = {}
                        self.tagList['OPC'][add_result[0]]['property'] = {}
                        self.tagList['OPC'][add_result[0]]['property']['ip']= add_result[1]
                        self.tagList['OPC'][add_result[0]]['property']['port']= add_result[2]
                        self.buttonApply.set_sensitive(True)
                        
                    else:
                        message = 'OPC name %s is already exist..' % (add_result[0])
                        self.warning_dialog(message)
                        
    def add_dialog(self,treeview):

        result = None
        label = gtk.Label("Insert device name")
        entry = gtk.Entry()
        entry.set_text('Device Name')
        dialog = gtk.Dialog("Add new device by manual:",
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                            
        hbox = gtk.HBox(False,0)
        hbox.show()
        hbox.pack_start(label,False,False,0)
        dialog.vbox.pack_start(hbox)
        dialog.vbox.pack_start(entry)
        
        # Label ID 
        id_label = gtk.Label("Device ID(1-46788):")
        id_label.show()
        dialog.vbox.pack_start(id_label)
        # Entry Bacnet ID
        id_entry = gtk.Entry()
        id_entry.set_text('')
        id_entry.set_size_request(30,24)
        id_entry.show()
        dialog.vbox.pack_start(id_entry)
        
        
        dialog.set_resizable(False)
        label.show()
        entry.show()
        response = dialog.run()
        if response == -2: # Click OK button
            # Check input is valid
            id = id_entry.get_text()
            a =0
            try:
                a=int(id)
            except:
                message =  'Please enter a valid integer'
                self.warning_dialog(message)
                
            if a>0 and len(entry.get_text())>0:
                result =  entry.get_text(),id_entry.get_text()
            dialog.destroy()  
            
        else: # Cancel button
            result = None
            dialog.destroy()  
                    
                    
        return result
                        
    def add_dialog_opc(self,treeview,defualt):
        global result
        result = None
        self.size_group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        
        label = gtk.Label("Server name")
        label.show()
        self.size_group.add_widget(label)
        
        entry = gtk.Entry()
        entry.set_text(defualt['opc server name'])
        entry.set_size_request(242,24)
        
        dialog = gtk.Dialog("Add OPC server by manual:",
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                            
        vbox = gtk.VBox(False,10)
        vbox.show()
        dialog.vbox.pack_start(vbox)
                            
        hbox = gtk.HBox(False,5)
        hbox.show()
        vbox.pack_start(hbox)
        
        hbox.pack_start(label,False,False,0)
        hbox.pack_start(entry,False,False,0)
        
        
        def ip_key_press(self, event):
            global result
            keyname = gtk.gdk.keyval_name(event.keyval)
            #print "Key press ",keyname
            if keyname == 'Return':
                print "Close by Enter Key"
                result =  entry.get_text(),ip_entry.get_text(),port_entry.get_text()
                #print "result by key press ",result
                dialog.destroy()
                #return result
            if keyname =='Escape':
                dialog.destroy()
                #return None
        #Horizontal 
        hbox_ip = gtk.HBox(False,5)
        hbox_ip.show()
        vbox.pack_start(hbox_ip)
        #hbox.pack_start(label,False,False,0)
        #----------------------------------
        # Label ID 
        ip_label = gtk.Label("IP Address:  ")
        ip_label.show()
        self.size_group.add_widget(ip_label)
        
        hbox_ip.pack_start(ip_label,False,False,0)
        #dialog.vbox.pack_start(ip_label)
        # Entry Bacnet ID
        ip_entry = gtk.Entry()
        ip_entry.set_text(defualt['ip'])
        ip_entry.set_size_request(130,24)
        hbox_ip.pack_start(ip_entry,False,False,0)
        
        label = gtk.Label('Port')
        label.show()
        hbox_ip.pack_start(label,False,False,0)
        
        port_entry = gtk.Entry()
        port_entry.show()
        port_entry.set_text(defualt['port'])
        port_entry.set_size_request(70,24)
        hbox_ip.pack_start(port_entry,False,False,0)
        port_entry.connect("key_press_event",ip_key_press)
        
        # key event
        ip_entry.connect("key_press_event",ip_key_press)
        entry.connect("key_press_event",ip_key_press)
        
        ip_entry.show()
        #dialog.vbox.pack_start(ip_entry)
        
        print "Set dialog center"
        dialog.set_position(gtk.WIN_POS_CENTER )
        dialog.set_resizable(False)
        label.show()
        entry.show()
        response = dialog.run()
        if response == -2 or response == -1: # Click OK button [-1 ] exit bby key Enter/Escape
            if response == -2:
                ip = ip_entry.get_text()
                port = port_entry.get_text()
                a =0
                try:
                    a=int(port)
                except:
                    #print 'Please enter a valid port integer.'
                    a = 0
                    message = 'Please enter a valid port integer.'
                    self.warning_dialog(message)
                    
                if a>0:
                    result =  entry.get_text(),ip_entry.get_text(),port_entry.get_text()
                    dialog.destroy()  
            
        else: # Cancel button
            result = None
            dialog.destroy()  
 
        return result

        
    def add_tag_item(self,widget,widget_pack_ret,tagEntry,window):
        #select_Tag  = tagEntry.get_text()
        textbuffer = tagEntry.get_buffer()
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        select_Tag = textbuffer.get_text(start_iter,end_iter)
        select_Tag = select_Tag.replace('\r','')
        select_Tag = select_Tag.replace('\n','')
        print select_Tag
        print window
        widget_pack_ret['entry'].set_text(select_Tag) # return update opc tag
        window.destroy()
        
    def add_local_item(self,widget,treeview, treestore,default,state):
        global result
        
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_item = tree_model.get_value(iter, 0)
        print selected_item
        parent_item = tree_model.iter_parent(iter)
        if parent_item is not None:
            selected_parent = tree_model.get_value(parent_item, 0)
        else:
            selected_parent = None
        print 'selected  parent from list',selected_parent
        
        if state == 'edit':
            default = selected_item,'None'
            title = "edit local item"
        else:
            title = "add local item"
            
        
        
        label_header = gtk.Label("Item")
        label_header.show()
        #self.size_group.add_widget(label)
        
        entry = gtk.Entry()
        entry.set_text(default[0])
        entry.set_size_request(242,24)
        
        dialog = gtk.Dialog(title,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                            
        vbox = gtk.VBox(False,10)
        vbox.show()
        dialog.vbox.pack_start(vbox)
                            
        hbox = gtk.HBox(False,5)
        hbox.show()
        vbox.pack_start(hbox)
        
        hbox.pack_start(label_header,False,False,0)
        hbox.pack_start(entry,False,False,0)
        
        
        def _key_press(self, event):
            global result
            keyname = gtk.gdk.keyval_name(event.keyval)
            #print "Key press ",keyname
            if keyname == 'Return':
                print "Close by Enter Key"
                if entry.get_text() == "":
                    result = None
                else:
                    result =  entry.get_text(),type_entry.get_text()
                dialog.destroy()
                return result
            
            if keyname =='Escape':
                result = None
                dialog.destroy()
                return None
        #Horizontal 
        hbox_ip = gtk.HBox(False,5)
        hbox_ip.show()
        vbox.pack_start(hbox_ip)
        #hbox.pack_start(label,False,False,0)
        #----------------------------------
        # Label ID 
        label = gtk.Label("Type")
        
        #self.size_group.add_widget(ip_label)
        
        hbox_ip.pack_start(label,False,False,0)
        #dialog.vbox.pack_start(ip_label)
        # Entry Bacnet ID
        type_entry = gtk.Entry()
        type_entry.set_text(default[1])
        type_entry.set_size_request(130,24)
        hbox_ip.pack_start(type_entry,False,False,0)
        
        
        
        # key event
        type_entry.connect("key_press_event",_key_press)
        entry.connect("key_press_event",_key_press)
        
        print selected_parent,selected_item
        if selected_parent == 'Local' and state == 'edit':
            if str(type(self.tagList['Local'][selected_item])) == '<type \'dict\'>': # found group type
                type_entry.hide()
                label.hide()
                label_header.set_text('New Group name')
            else:
                type_entry.show()
                label.show()
                label_header.set_text('Item')
                
        
        
        #dialog.vbox.pack_start(ip_entry)
        
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.set_resizable(False)
        
        entry.show()
        response = dialog.run()
        if response == -2 or response == -1: # Click OK button [-1 ] exit bby key Enter/Escape
            if response == -2:
                if entry.get_text() == "":
                    result = None
                else:
                    result =  entry.get_text(),type_entry.get_text()
            
            dialog.destroy()  
            
        else: # Cancel button
            result = None
            dialog.destroy()  
 
        if result is not None:

            #--------------------ADD NEW ITEM--------------------
            if state == 'add':
                if selected_item == 'Local':
                    if iter:
                        if self.checkTagLocalExist(self.tagList['Local'],result[0]):
                            iter2 = treestore.append(iter,[result[0]])
                            self.tagList['Local'][result[0]] = [] #add item
                        #self.tagList['Local'][result]['device_id'] = result_device[1]

                else:
                    
                    if selected_parent == 'Local':
                        if iter:
                            if self.checkTagLocalExist(self.tagList['Local'][selected_item],result[0]):
                                iter2 = treestore.append(iter,[result[0]])
                                self.tagList['Local'][selected_item][result[0]] = [] #add item
                        
            #--------------EDIT ITEM----------------------------
            if state == 'edit':
                print "edit of ",selected_item,selected_parent
                if selected_item != result[0]:
                    
                    print "edit pass"
                    if selected_parent == 'Local':
                        if iter:
                            if self.checkTagLocalExist(self.tagList['Local'],result[0]):
                                backup = self.tagList['Local'][selected_item] 
                                del self.tagList['Local'][selected_item]
                                #delete current seletc item before edit
                                tree_model.remove(iter)
                                
                                iter2 = treestore.append(parent_item,[result[0]])
                                self.tagList['Local'][result[0]] = backup
                                self.loadLocaltoTreeView(iter2,None,treestore,self.tagList['Local'][result[0]])
                            #self.tagList['Local'][result]['device_id'] = result_device[1]
                    else:
                        if self.checkTagLocalExist(self.tagList['Local'][selected_parent],result[0]):
                            backup = self.tagList['Local'][selected_parent][selected_item] 
                            del self.tagList['Local'][selected_parent][selected_item] 
                                #delete current seletc item before edit
                            tree_model.remove(iter)
                            
                            iter2 = treestore.append(parent_item,[result[0]])
                            self.tagList['Local'][selected_parent][result[0]] = backup

                   
                                
                else:
                    print "item not change"
                
                    
                    
                    
            self.buttonApply.set_sensitive(True)
        
    def add_local_group(self,widget,treeview, treestore,default):
        global result
        label = gtk.Label("Group Name")
        label.show()
        #self.size_group.add_widget(label)
        
        entry = gtk.Entry()
        entry.set_text(default)
        entry.set_size_request(180,24)
        
        dialog = gtk.Dialog("Add Group Local:",
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                            
        vbox = gtk.VBox(False,10)
        vbox.show()
        dialog.vbox.pack_start(vbox)
                            
        hbox = gtk.HBox(False,5)
        hbox.show()
        vbox.pack_start(hbox)
        
        hbox.pack_start(label,False,False,0)
        hbox.pack_start(entry,False,False,0)
        
        
        def _key_press(self, event):
            global result
            keyname = gtk.gdk.keyval_name(event.keyval)
            #print "Key press ",keyname
            if keyname == 'Return':
                print "Close by Enter Key"
                result =  entry.get_text()
                #print "result by key press ",result
                dialog.destroy()
                return result
            if keyname =='Escape':
                result = None
                dialog.destroy()
                return None
        
        entry.connect("key_press_event",_key_press)
        
        
        #dialog.vbox.pack_start(ip_entry)
        
        
        dialog.set_resizable(False)
        label.show()
        entry.show()
        response = dialog.run()
        if response == -2 or response == -1: # Click OK button [-2 ] ,exit by key Enter/Escape [-1 ]
            if response == -2:
                result =  entry.get_text()
            if result == "":
                result = None
            dialog.destroy()  
            
        else: # Cancel button
            result = None
            dialog.destroy()  

        if result is not None:
            selection = treeview.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            tree_model, iter = selection.get_selected()
            selected_item = tree_model.get_value(iter, 0)
            print selected_item
            if selected_item == 'Local':
                if iter:
                    print 'add group'
                    for t in self.tagList['Local']:
                        print t,result
                    if self.checkTagLocalExist(self.tagList['Local'],result):
                        iter2 = treestore.append(iter,[result])
                        self.tagList['Local'][result] = {} #add group
                        #self.tagList['Local'][result]['device_id'] = result_device[1]
                        self.buttonApply.set_sensitive(True)
 
        return result

        
    def apply_change(self,button):
        print "Apply change"
        self.buttonApply.set_sensitive(False)
        currentPath = os.getcwd()
        #Save bacnet to file 
        if os.name == 'nt':# check window os
            pathImage = currentPath+ '\\configure\\tag.db'
            savefile = open(pathImage,'wb')
        else: # other os , linux
            savefile = open('configure/tag.db','wb')
            
        pickle.dump(self.tagList, savefile)
        print "Save new change database !"
        savefile.close()
        
    def bacnetListDevice(self):
        f = open(r'baclist.txt')
        readDevice = f.read()
        each_point = readDevice.split('},')
        all_list =[]
        
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
        for b in all_list:
            print b['object-name']
        f.close()
        return all_list
    
    def browe_device(self,widget,treeview,treestore):
        self.buttonApply.set_sensitive(True)
        getB =  bacnet_device()
        getB.probBacnet(treeview,treestore,self.tagList['Bacnet IP'])
        #v = getB.probBacnet()
        print "Click browser bacnet progress window "
        
    def check_hide_tag(self,tag,cnt):
        i = 0
        for g in tag:
            if g == '.':
                i +=1
        #print 'show count ',i
        if cnt == i:
            return True
        else:
            return False
        
    def checkTagExist(self,result_device):
        #if self.tagList['OPC'].has_key(add_result[0]) == False:
        for j in self.tagList['Bacnet IP']:
            if j == result_device[0]:
                #Show dialog warning 
                message = "Can't add new device because  %s exist." % (j)
                print message
                self.warning_dialog(message)
                return False
            if self.tagList['Bacnet IP'][j]['device_id'] == result_device[1]:
                message = "Can't add new device because ID %s exist." % (result_device[1])
                print message
                self.warning_dialog(message)
                return False
                #end of dialog warning
        return True
    
    def checkTagLocalExist(self,tag,input_check):
        for j in tag:
            if j == input_check:
                #Show dialog warning 
                message = "Error to add new tag [local],%s is already exist" % (j)
                self.warning_dialog(message)
                return False
        return True
        
    def click_treeview(self):
        print 'Click Tree'
        
    def clear_selected(self, widget,tree_view):
        selection = tree_view.get_selection()
        model, iter = selection.get_selected()
        if iter:
            model.remove(iter)
        return
    
    def _click_press_tree(self,widget,event, treestore,widget_pack_ret,tagEntry,window):
        #print "tree view button click ",event.button
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        
        if event.button == 3 : # on right click
            
            parent_item = tree_model.iter_parent(iter)
            if iter is not None:
                selected_item = tree_model.get_value(iter, 0)
                if selected_item == 'Bacnet IP':
                    print "Popup menu Browe Bacnet Device"
                    self.popupMenu(event,'find_bacnet',widget, treestore)
                    
                if selected_item == 'OPC':
                    #print "Popup menu Browe Device"
                    self.popupMenu(event,'find_opc_server',widget, treestore)
                    
                if selected_item == 'Local':
                    #print "Popup menu Browe Device"
                    self.popupMenu(event,'add_local',widget, treestore)
                    
                if parent_item is not None:
                    root_parent =  tree_model.get_value(parent_item, 0)
                    if root_parent == 'Bacnet IP': 
                        self.popupMenu(event,'refresh_bacnet',widget, treestore)
                        
                    if root_parent == 'OPC':
                        self.popupMenu(event,'refresh',widget, treestore)
                        
                    if root_parent == 'Local':
                        if str(type(self.tagList[root_parent][selected_item])) == '<type \'list\'>':
                            self.popupMenu(event,'add_local_sub2',widget, treestore)
                        else:
                            self.popupMenu(event,'add_local_sub',widget, treestore)
                    
                    
                    parent_item = tree_model.iter_parent(parent_item)
                    if parent_item is not None:
                        root_parent =  tree_model.get_value(parent_item, 0)
                        if root_parent == 'Local':
                            self.popupMenu(event,'add_local_sub2',widget, treestore)
        if iter is not None:
            if tree_model.iter_has_child(iter) == False and event.type == gtk.gdk._2BUTTON_PRESS:
                print "double click treeview"
                
                self.add_tag_item(None,widget_pack_ret,tagEntry,window) # add item to parent window
                        

    def _click_tree(self,widget,data,tagEntry,widget_pack_ret):
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        
        if iter is not None:
            
            if tree_model.iter_has_child(iter) == False: # check item havn't child(the last item select)
                #The last item select ill show in entry
                selected_item = tree_model.get_value(iter, 0)
                parent_item = tree_model.iter_parent(iter)
                root_parent = None
                if parent_item is not None:
                    tag = []
                    p = ''
                    while (parent_item != None):
                        if parent_item is not None:
                            root_parent =  tree_model.get_value(parent_item, 0)
                            tag.append(root_parent)
                            p = root_parent+'.'+p
                        parent_item = tree_model.iter_parent(parent_item)
                        
                    selected_item = p+selected_item
                    if root_parent == 'Bacnet IP':
                        tag.reverse()
                        get_all_tag = ''
                        for j in tag:
                            get_all_tag = get_all_tag +j + '.'
                        get_all_tag = get_all_tag +selected_item
                        print get_all_tag
                    #print 'Bacnet tag ',(tag+selected_item)
                else:
                    root_parent = selected_item
                    print 'OPC Server Name: ',root_parent
                    
                widget_pack_ret['opc_server_name'] = root_parent

                '''tag = []
                while iter != None:
                    iter = tree_model.iter_parent(iter)
                    if iter is not None:
                        value = tree_model.get_value(iter, 0)
                        tag.insert(0,value)
                #insert all root -->child
                add_tag = ''
                for val in tag:
                    add_tag +=val
                    add_tag +='.'
                add_tag = add_tag + selected_item'''
                #if root_parent != 'Bacnet IP':
                    #tagEntry.set_text(selected_item)
                textbuffer = tagEntry.get_buffer()
                '''start_iter = textbuffer.get_start_iter()
                end_iter = textbuffer.get_end_iter()
                print textbuffer.get_text(start_iter,end_iter)'''
                textbuffer.set_text(selected_item)
                
                
                    
        
                #else:
                    #tagEntry.set_text(get_all_tag)
                    
                        
            #print selected_user,
            
            
        #print 'click treeview'
        
    def connect(self,widget,tree_view,treestore):

        widgetPack['connect'].set_sensitive(False)
        widgetPack['refresh'].set_sensitive(True)
        #widgetPack['disconnect'].set_sensitive(True)
        widgetPack['ip'].set_sensitive(False)
        widgetPack['find'].set_sensitive(True)
        print "Connect press"
            
        return True
        
    
    
    def deleteDevice(self,widget,treeview, treestore):
        selection = treeview.get_selection()
        result = selection.get_selected()
        #print "delete selection ",result
        if result: #result could be None
            tree_model, iter = result
            selected_item = tree_model.get_value(iter, 0)
            
            print 'delete device from list',selected_item
            parent_item = tree_model.iter_parent(iter)
            selected_parent = tree_model.get_value(parent_item, 0)
            print 'delete device parent from list',selected_parent
            del self.tagList[selected_parent][selected_item] # delete select device item
            tree_model.remove(iter)
            self.buttonApply.set_sensitive(True)
            
    def deleteLocalItem(self,widget,treeview, treestore):
        selection = treeview.get_selection()
        result = selection.get_selected()
        #print "delete selection ",result
        if result: #result could be None
            tree_model, iter = result
            selected_item = tree_model.get_value(iter, 0)
            
            print 'delete device from list',selected_item
            parent_item = tree_model.iter_parent(iter)
            selected_parent = tree_model.get_value(parent_item, 0)
            print 'delete device parent from list',selected_parent
            if selected_parent == 'Local':
                del self.tagList[selected_parent][selected_item]
            else:
                del self.tagList['Local'][selected_parent][selected_item] # delete select device item
            tree_model.remove(iter)
            self.buttonApply.set_sensitive(True)
            
            
    def dialogProperty(self,widget,treeview, treestore):
        #label = gtk.Label("\r\n\r\nServer name and property")
        #label.show()
       
        selection = treeview.get_selection()
        result = selection.get_selected()
        MESSAGE = "Property : None"
        #print "delete selection ",result
        if result: #result could be None
            tree_model, iter = result
            selected_item = tree_model.get_value(iter, 0)
            
            print 'selected server from list',selected_item
            parent_item = tree_model.iter_parent(iter)
            selected_parent = tree_model.get_value(parent_item, 0)
            print 'selected server parent from list',selected_parent
            if selected_parent == 'OPC':
                if self.tagList[selected_parent][selected_item].has_key('property') ==True:
                    ip = self.tagList[selected_parent][selected_item]['property']['ip']
                    port = self.tagList[selected_parent][selected_item]['property']['port']
                    MESSAGE = 'OPC Server Name :'+ selected_item + '\r\n'
                    MESSAGE = MESSAGE + 'IP Address   : ' + ip +'\r\n'
                    MESSAGE = MESSAGE + 'Connection Port  : ' + port +'\r\n'
                    
            if selected_parent == 'Bacnet IP':
                id = self.tagList[selected_parent][selected_item]['device_id']
                MESSAGE = 'Bacnet Device Name :'+ selected_item + '\r\n'
                MESSAGE = MESSAGE + 'Device ID   : ' + id +'\r\n'
                
            if selected_parent == 'Local':
                MESSAGE = 'Variable Name :'+ selected_item + '\r\n'
                if str(type(self.tagList[selected_parent][selected_item])) == '<type \'list\'>':
                    MESSAGE = MESSAGE + 'Type   : Item' +'\r\n'
                else:
                    MESSAGE = MESSAGE + 'Type   : Group' +'\r\n'
                
                    
        
        
        
        
        
        
        
        dialog = gtk.MessageDialog(self.window,
                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                    gtk.MESSAGE_INFO, gtk.BUTTONS_OK,MESSAGE)
                            
                            
        #vbox = gtk.VBox(True,30)
        #vbox.show()
        #vbox.pack_start(label,False,False,0)
        #dialog.vbox.pack_start(vbox)
        dialog.run()
        dialog.destroy()
        
    def disconnect(self,widget,tree_view):

        widgetPack['connect'].set_sensitive(True)
        widgetPack['refresh'].set_sensitive(False)
        widgetPack['disconnect'].set_sensitive(False)
        widgetPack['ip'].set_sensitive(True)
        widgetPack['find'].set_sensitive(True)
        print 'disconnect press'
        return True
      
    
    def edit_opcserver(self,widget,treeview, treestore):
        #print self.device_net
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_item = tree_model.get_value(iter, 0)
        print "edit opc server name ",selected_item
        parent_item = tree_model.iter_parent(iter)
        selected_parent = tree_model.get_value(parent_item, 0)
        print 'edit opc parent from list',selected_parent
            
        '''if selected_parent == 'Bacnet IP':
            if iter:
                result_device =  self.add_dialog(treeview)
                if result_device is not None:
                    if self.checkTagExist(result_device):
                        print "%s pass"% (result_device[0])
                        mypiter1 = treestore.append(iter,[result_device[0]])
                        self.device_net[result_device[0]] = {}
                        self.device_net[result_device[0]]['device_id'] = result_device[1]
                        self.buttonApply.set_sensitive(True)
                        #mypiter1 = treeStore.append(None, result_device[1])
                        # refresh list 
                        #for h in self.device_net:
                        #    print h
                    else:
                        print "not pass"'''
                        
        if selected_parent == 'OPC':
            if iter:
                defualt = {}
                defualt['opc server name'] = selected_item
                defualt['ip'] = None
                defualt['port'] = None
                if self.tagList[selected_parent][selected_item].has_key('property') == True:
                    defualt['ip'] = self.tagList[selected_parent][selected_item]['property']['ip']
                    defualt['port'] = self.tagList[selected_parent][selected_item]['property']['port']

                add_result =  self.add_dialog_opc(treeview,defualt)
                print add_result
                if add_result is not None:
                    tree_model.set_value(iter, 0, add_result[0])
                    backup_opc = self.tagList[selected_parent][selected_item]
                    backup_opc['property']['ip'] = add_result[1]
                    backup_opc['property']['port'] = add_result[2]
                    
                    del self.tagList[selected_parent][selected_item]
                    self.tagList[selected_parent][add_result[0]] = backup_opc
                    self.buttonApply.set_sensitive(True)
                    
                '''if add_result is not None:
                    print add_result
                    if self.tagList['OPC'].has_key(add_result[0]) == False:
                        print "add OK ",add_result[0]
                        mypiter1 = treestore.append(iter,[add_result[0]])
                        self.tagList['OPC'][add_result[0]] = {}
                        self.tagList['OPC'][add_result[0]]['property'] = {}
                        self.tagList['OPC'][add_result[0]]['property']['ip']= add_result[1]
                        self.tagList['OPC'][add_result[0]]['property']['port']= add_result[2]
                        self.buttonApply.set_sensitive(True)
                        
                    else:
                        message = 'OPC name %s is already exist..' % (add_result[0])
                        self.warning_dialog(message)'''
        
    def exportFile(self,item,treeview,treestore,file_type):
        print 'export file'
        
        file_selected = self.save_file(file_type)
        if file_selected is not None:
            
            file_selected = file_selected.replace(file_type[1][1:],'') #remove custom file type
            file_selected += file_type[1][1:]
            print file_selected 
            selection = treeview.get_selection()
            
            result = selection.get_selected()
            #print "delete selection ",result
            if result: #result could be None
                tree_model, iter = result
                selected_item = tree_model.get_value(iter, 0)
                parent_item = tree_model.iter_parent(iter)
                selected_parent = tree_model.get_value(parent_item, 0)
                server_net = self.tagList[selected_parent][selected_item] # delete select device item
                #Save database to file 
                savefile = open(file_selected,'wb')
                pickle.dump(server_net, savefile) 
                savefile.close()
                
    def find_children_tree(self,treestore,iter,new_children):
        # This def for check exist children in tree view 
        item_iter = treestore.iter_children(iter)
        iter_pack = []
        while item_iter:
            iter_pack.append(item_iter)
            value = treestore.get_value(item_iter, 0)
            if new_children == value:
                return True # the children has exist
            item_iter = treestore.iter_next(item_iter)
        return None
                
    def find_opc_server(self,widget,treeview,treestore):
        self.buttonApply.set_sensitive(True)
        print "Click Find OPC Server on network... "
        
    
        
    
    def getBacnetDevice(self):
        print "Bacnet get device ! "
        '''cmd = "./bacgetid.sh"# + " 1 "+str(self.id) 
        result = os.popen(cmd)
        list = []
        for i in result.readlines():
            #i = str(i) + " from   " + str(self.id)
            #k = "Point No." +str(self.id) +" value is " + str(i) 
            
                #id = i.spilt(',')
                #print "Recive bacnet device from ",id[0][-2:]
            if i[0:1] != ';':
                if "Received I-Am Request from" in i:
                    pass
                else:
                    bacid = i[0:6].replace(' ','')
                    #print "len bac id ", len(bacid)
                    list.append(bacid)
        #BY PASS DEMO'''
        list =['11']
        return list


    def getTaglist(self):
        self.treestore = gtk.TreeStore(str)
        self.load_new_item(self.treestore,False)
        # we'll add some data now - 4 rows with 3 child rows each
        #root device 
        '''OpcDevice = ['Device','Local Variable','Simulate']
        OpcDevice[0] = self.treestore.append(None, ['%s' % OpcDevice[0] ])
        OpcDevice[1] = self.treestore.append(None, ['%s' % OpcDevice[1] ])
        OpcDevice[2] = self.treestore.append(None, ['%s' % OpcDevice[2] ])
        
        arrang_device = device.keys()
        arrang_device.sort()
            
        for parent in arrang_device:
            piter = self.treestore.append(OpcDevice[0], ['%s' % parent])
            lange = device[parent].keys()
            lange.sort()
            for child in lange:
                #print child
                mypiter2 = self.treestore.append(piter, [child])
                #child2 = device[parent][child].keys()
                #child2.sort()
                for child2 in device[parent][child]:
                    mypiter3 = self.treestore.append(mypiter2,[child2])# [None,gtk.STOCK_NEW,'%s' % child2,True]
        '''
        return self.treestore
    
    def getTaglist_local(self):
        #read all OPC tag
        #self.treestore = gtk.TreeStore(str)
        gateway = 'localhost'
        opchost = 'localhost'
        opc = OpenOPC.client()
        opclist = opc.servers()
        allTag = []
        server_tag ={}
        for listOpcServer in opclist:
            #treeOpcServer = self.treestore.append(None, ['%s' % listOpcServer ])
            server_tag[listOpcServer]={} # Keep All OPC Server Name 
            try:
                opc.connect(listOpcServer)
                listItem = opc.list()
                for j in listItem:
                    server_tag[listOpcServer][j]={}
                    #mypiter2 = self.treestore.append(treeOpcServer, [j])
                    print j
                    print '---'
                    subList = opc.list(j)
                    for k in subList:
                        server_tag[listOpcServer][j][k]={}
                        #mypiter3 = self.treestore.append(mypiter2, [k])
                        print '   ' + k
                        find_sub = k.find('.')
                        if find_sub == -1:
                            tag = j+'.'+k
                            list2 = opc.list(tag)
                            #Check hide item
                            tag_hide = tag+'*'
                            hideItem = opc.list(tag_hide,flat = True)
                            for hd in hideItem :
                                result_hide = self.check_hide_tag(hd,2)
                                if result_hide:
                                    print  '           +- ',hd
                                    server_tag[listOpcServer][j][k][hd]={}
                                    allTag.append(hd)
                            #End hide item
                            for v in list2:
                                server_tag[listOpcServer][j][k][v]={}
                                #mypiter4 = self.treestore.append(mypiter3, [v])
                                print '           +- ',
                                print v
                                find_sub2 = v.find('.')
                                if find_sub2 ==-1:
                                    tag3 = tag+'.'+v
                                    list3 = opc.list(tag3)
                                    #Check hide item
                                    tag_hide = tag3+'*'
                                    hideItem = opc.list(tag_hide,flat = True)
                                    for hd in hideItem :
                                        result_hide = self.check_hide_tag(hd,2)
                                        if result_hide:
                                            print  '                 +- ',hd
                                            server_tag[listOpcServer][j][k][v][hd]={}
                                            allTag.append(hd)
                                    #End hide item
                                    for t in list3:
                                        server_tag[listOpcServer][j][k][v][t]={}
                                        #mypiter5 = self.treestore.append(mypiter4, [t])
                                        print '                 +- ',
                                        print t
                                        find_sub3 = t.find('.')
                                        if find_sub3 ==-1:
                                            tag4 = tag3+'.'+t
                                            list4 = opc.list(tag4)
                                            for b in list4:
                                                server_tag[listOpcServer][j][k][v][t][b]={}
                                                #mypiter6 = self.treestore.append(mypiter5, [b])
                                                allTag.append(b)
                                        else:
                                            allTag.append(t)
                                else:
                                    allTag.append(v)
                        else:
                            allTag.append(k) 
                opc.close()
            except Exception,e:
                print e
                
        #OpcDevice_1= self.treestore.append(None, ['Local Variable' ])
        #OpcDevice_2 = self.treestore.append(None, ['Simulation'])
        '''file_name = open('servertag.opc', 'wb') 
        pickle.dump(server_tag, file_name) 
        print 'Save pickle...'
        file_name.close()'''
        
        return server_tag
    
    def importBacnetFromFile(self,item,treeview,treestore):
        fileType = "bacnet file","*.bac"
        file_selected = self.open_opc_file(fileType)
        if file_selected is not None:
            
            myload = open(file_selected,'r')
            device_net = pickle.load(myload)
            myload.close()
            #print "load bacnet list from file ",device_net
            
            selection = treeview.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            tree_model, iter0 = selection.get_selected()
            if iter0 is not None:
                #if tree_model.iter_has_child(iter0) == False: # check item havn't child(the last item select)
                selected_item = tree_model.get_value(iter0, 0)
                print selected_item
                parent_item = tree_model.iter_parent(iter0)
                selected_parent = tree_model.get_value(parent_item, 0)
                print 'add parent name is ',selected_parent
                
                #id = self.tagList[selected_parent][selected_item]
                _device = None,device_net['device_id']
                if self.checkTagExist(_device): #Check exist device  
                    for h in device_net:
                        self.tagList[selected_parent][selected_item]=device_net
                        self.loadBacnettoTreeView(iter0,treeview,treestore,device_net)
     
                    self.buttonApply.set_sensitive(True)
                return device_net
        
    def importOPCFromFile(self,item,treeview,treestore):
        
        fileType = "opc file","*.opc"
        file_selected = self.open_opc_file(fileType)
        
        if file_selected is not None:
            '''myload = ''
            if os.name == 'nt':# check window os
                path = currentPath+ '\\configure\\opc_server_db.opc'
                myload = open(path,'r')
            else: # other os , linux
                myload = open('configure/opc_server_db.opc','r')'''
            
            myload = open(file_selected,'r')
            device_tag = pickle.load(myload)
            myload.close()
            print "load OPC list from file "
            
            selection = treeview.get_selection()
            selection.set_mode(gtk.SELECTION_SINGLE)
            tree_model, iter0 = selection.get_selected()
            if iter0 is not None:
                #if tree_model.iter_has_child(iter0) == False: # check item havn't child(the last item select)
                selected_item = tree_model.get_value(iter0, 0)
                print selected_item,
                parent_item = tree_model.iter_parent(iter0)
                selected_parent = tree_model.get_value(parent_item, 0)
                print 'add parent name is ',selected_parent
                
                #Copy item load to main database
                #TODO : Add treeview
                item_iter = tree_model.iter_children(iter0)
                print '|----print child treeview of ',selected_item
                #for iter_c in file_iter:
                
                temp_iter = []
                while item_iter:
                    temp_iter.append(item_iter)
                    print tree_model.get_value(item_iter, 0)
                    item_iter = tree_model.iter_next(item_iter) 
                    
                #remove older iter before load new
                
                for it in temp_iter:
                    tree_model.remove(it)   
                    
                #delete sub tag before 
                property = self.tagList[selected_parent][selected_item]['property'] # save property before delete all tag
                del self.tagList[selected_parent][selected_item]
                
                self.tagList[selected_parent][selected_item] ={}
                self.tagList[selected_parent][selected_item]['property'] = property
                        
                del temp_iter # remove temp list
                
                
                for h in device_tag:
                    self.tagList[selected_parent][selected_item][h] = device_tag[h]
                #add item to treeview
                self.loadOPCtoTreeView(iter0,treeview,treestore,device_tag)
                self.buttonApply.set_sensitive(True) # enable apply button
            
        return True
                    
    def load_new_item(self,treestore,local):
        #TODO : Add tag to treeview 
        myload = ''
        self.tagList = None
        if local == True:
            #opcList = self.getTaglist()
            self.tagList = self.getTaglist_local()
        else:
            if os.name == 'nt':# check window os
                pathImage = currentPath+ '\\configure\\tag.db'
                myload = open(pathImage,'r')
            else: # other os , linux
                myload = open('configure/tag.db','r')
            
            self.tagList = pickle.load(myload)
            myload.close()
            
        '''#TEST LOAD OPC and spilt with '.'
        self.opc_root = {}
        tag = 'opc.node1.node2.node3.node4'
       
        for i in self.opcList:
            #print i
            self.opc_root[i]={}
            #iter1 = treeStore.append(None, [i])
            #cnt = 0
            
            for k in self.opcList[i]:
                #print k
                #cnt += 1
                #mypiter2 = treeStore.append(iter1, [k])
            #mypiter2 = treeStore.append(iter1, ['Count item = '+ str(cnt)])
                tag_sp = k.split('.')
                #print tag_sp
                if self.opc_root[i].has_key(tag_sp[0]) == False:
                    self.opc_root[i][tag_sp[0]] = []
                    
                
                self.opc_root[i][tag_sp[0]].append(tag_sp[1:len(tag_sp)])
                
            self.opc_root[i][tag_sp[0]].sort()
                #self.spiltOPCParent(opc_root,tag_sp,None,treestore)
                
        iter0 = treeStore.append(None, ['OPC'])
        
        for j in self.opc_root:
            #print j
            iter1 = treeStore.append(iter0, [j])
            #opc_root[j].sort()
            #print 'type lis opc_root[j] ',type(opc_root[j])
            for h in sorted(self.opc_root[j].iterkeys()):#for key in sorted(mydict.iterkeys()):  #print "%s: %s" % (key, mydict[key])
                if h != 'info':
                    #print '-----',h
                    iter2 = treeStore.append(iter1, [h])
                    for f in self.opc_root[j][h]: #.sort():#for key in sorted(mydict.iterkeys()):  #print "%s: %s" % (key, mydict[key])
                        #print '-----',f
                        val = ''
                        for v in f:
                            val = val +v + '.'
                            
                        val = val[:len(val)-1]
                        iter3 = treeStore.append(iter2, [val])'''
                
       
            
        '''for t in opcList:
            print t
            iter1 = treeStore.append(None, [t])
        
            for i in opc_root:
                mypiter1 = treeStore.append(iter1, [i])
                #print i
                for j in opc_root[i]:
                    #print '----',j
                    mypiter2 = treeStore.append(mypiter1, [j])
                    for k in opc_root[i][j]:
                        mypiter3 = treeStore.append(mypiter2, [k])
                        #print '        ----',k
                        for l in opc_root[i][j][k]:
                            mypiter4 = treeStore.append(mypiter3, [l])
                            #print '                ----',l
                            for m in opc_root[i][j][k][l]:
                                mypiter5 = treeStore.append(mypiter4, [m])
                                #print '                     ----',m
                                for n in opc_root[i][j][k][l][m]:
                                    mypiter6 = treeStore.append(mypiter5, [n])'''
        
        OpcDevice = ['Bacnet IP','Local Variable','Simulate']
        for t in sorted(self.tagList.iterkeys()):
            print t
            tag_iter = treestore.append(None, [t])
            print "Child ",self.tagList[t]
            self.add_child_tag(tag_iter,treestore,self.tagList[t],t)
            
        
        '''
        listDevice = self.getBacnetDevice()
        # Get bacnet from file 'configure/bacnet_tag.bac'
        self.device_net = self.getBacnetFromFile()
        print self.device_net
        #Add bacnet device to treeview 
        for b in self.device_net:
            mypiter1 = treeStore.append(self.BacDevice, [b])
            for t in self.device_net[b]:
                tag = t#self.device_net[b][t]
                mypiter2 = treeStore.append(mypiter1, [tag])
                for prop in bacnet_list_prop:
                    mypiter3 = treeStore.append(mypiter2,[prop])'''
        '''
        all_list = self.BacnetListDevice()
        #Get bacnet point...
        
        if len(all_list)>0:
            name = all_list[0]['object-name']+ "_" + listDevice[0]
            name = name.replace('"',"")
            name = name.replace('\r',"")
            name = name.replace('\n',"")
            #for v in listDevice:
               # print '----',v
            mypiter1 = treeStore.append(BacDevice, [name])
            for y in all_list[1:]:
                name = y['object-name']
                name = name.replace('"',"")
                name = name.replace('\r',"")
                name = name.replace('\n',"")
                mypiter2 = treeStore.append(mypiter1, [name])
                for prop in bacnet_list_prop:
                    mypiter3 = treeStore.append(mypiter2,[prop])'''
                
        return True
    
    def loadBacnettoTreeView(self,iter0,treeview,treestore,device_tag):
        bacnet_list_prop = ['object-identifier','object-name','object-type','present-value','units','out-of-service','description']
    
        for j in sorted(device_tag.iterkeys()):
            if j != 'property':
                iter1 = treestore.append(iter0, [j])
                for prop in bacnet_list_prop:
                    iter2 = treestore.append(iter1,[prop])
                    
    def loadLocaltoTreeView(self,iter0,treeview,treestore,device_tag):
        if str(type(device_tag)) != '<type \'list\'>':
            for j in sorted(device_tag.iterkeys()):
                if j != 'property':
                    iter1 = treestore.append(iter0, [j])
                    if str(type(device_tag[j])) != '<type \'list\'>':
                        for k in sorted(device_tag[j].iterkeys()):
                            iter2 = treestore.append(iter1, [k])
    
    def loadOPCtoTreeView(self,iter0,treeview,treestore,device_tag):
        for j in device_tag:
            if j != 'property':
                iter1 = treestore.append(iter0, [j])
                for h in sorted(device_tag[j].iterkeys()):
                    if h != 'info' :
                        #print '-----',h # display all tag
                        sepTag = h.split('.')
                        #print sepTag[0]
                        # Group _ 1 
                        if len(sepTag)>2: 
                            if self.find_children_tree(treestore,iter1,sepTag[0]) == None:
                                iter2 = treestore.append(iter1, [sepTag[0]])
                            else:
                                # Group_ 2
                                if len(sepTag[1:])>1:
                                    if self.find_children_tree(treestore,iter2,sepTag[1]) == None:
                                        iter3 = treestore.append(iter2, [sepTag[1]])
                                    else:
                                        # Group_ 3
                                        if len(sepTag[2:])>1:
                                            if self.find_children_tree(treestore,iter3,sepTag[2]) == None:
                                                iter4 = treestore.append(iter3, [sepTag[2]])
                                            else:
                                                t = ''
                                                for v in sepTag[3:]:
                                                    t = t+ v +'.'
                                                iter5 = treestore.append(iter4, [t[:-1]])

                                        else:
                                            t = ''
                                            for v in sepTag[2:]:
                                                t = t+ v +'.'
                                            iter4 = treestore.append(iter3, [t[:-1]])
                                else:
                                    t = ''
                                    for v in sepTag[1:]:
                                        t = t+ v +'.'
                                    iter3 = treestore.append(iter2, [t[:-1]])
                                
                        else:# The item hasn't group
                            iter2 = treestore.append(iter1, [h])
                            
    def local_property(self,widget,treeview, treestore):
        pass
  
    def match_func(self,model, iter, data):
       column, key = data # data is a tuple containing column number, key
       value = model.get_value(iter, column)
       return value == key

    
    
    def open_opc_file(self,file_tpye):
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_OPEN,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name(file_tpye[0])
        filter.add_pattern(file_tpye[1])
        dialog.add_filter(filter)
        FileSelect = None
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            FileSelect = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
            FileSelect = None
        dialog.destroy()

        return FileSelect
    
    def opcWindow(self,item,widget_pack_ret):
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.size_group_0 = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        #self.window.connect("delete_event", self.delete) # enable to close all event,destroy
        #self.window.connect("destroy", self.delete)
        self.window.set_border_width(10)
        self.window.set_title('TAG BROWSER')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        self.window.set_default_size (700, 400)
        self.window.set_destroy_with_parent(True)
        global_var.dialogOPCbrowe = self.window
        
        vbox = gtk.VBox(False, 5)
        
        self.window.add(vbox)
        vbox.show()
        self.window.set_modal(True)
        
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        #vbox.add(scrolled_window)
        '''HEADER 1 LABEL, INPUT IP SERVER , BUTTON CONNECT ,Disconnect , refresh'''
        
        hbox = gtk.HBox(False,5)
        label_s = gtk.Label('   Server IP :')
        self.size_group_0.add_widget(label_s)
        hbox.pack_start(label_s,False, False, 0)

        
        server_ip= 'localhost' # connection Host IP
        HostIP = gtk.Entry()
        HostIP.set_text (server_ip)
        HostIP.set_editable(True)
        HostIP.set_size_request(190, 24)
        HostIP.set_sensitive(False)
        hbox.pack_start(HostIP,False, False, 0)
        #Browe OPC Server 
        buttonFind = gtk.Button('Find..')
        buttonFind.set_size_request(60, 24)
        buttonFind.set_sensitive(True)
       
        
        hbox.pack_start(buttonFind,False, False, 0)
        
        # create Button Connect
        buttonConnect = gtk.Button('Connect')
        buttonConnect.set_size_request(70, 24)
        buttonConnect.set_sensitive(False)
        
        hbox.pack_start(buttonConnect,False, False, 0)
        
        '''buttonDisconnect = gtk.Button('Disconnect')
        buttonDisconnect.set_size_request(70, 24)
        buttonDisconnect.set_sensitive(True)
        #buttonConnect.connect("clicked", self.connect)
        hbox.pack_start(buttonDisconnect,False, False, 0)'''
        
        buttonRefresh = gtk.Button('Refresh')
        buttonRefresh.set_size_request(70, 24)
        buttonRefresh.set_sensitive(True)
        
        #Connect signal 
        widgetPack['ip'] = HostIP
        widgetPack['find'] = buttonFind 
        widgetPack['connect'] = buttonConnect
        #widgetPack['disconnect'] = buttonDisconnect
        widgetPack['refresh'] = buttonRefresh
        
        #buttonConnect.connect("clicked", self.connect)
        #buttonDisconnect.connect("clicked", self.disconnect)
        
        #buttonConnect.connect("clicked", self.connect)
        hbox.pack_start(buttonRefresh,False, False, 0)
        
        vbox.pack_start(hbox, True)
        #tagEntry.show()
        
        #Add frame 
        frame = gtk.Frame('Refresh')
        frame.set_border_width(5)
        frame.set_size_request(650, 280)
        #frame.show()
        frame.add(scrolled_window)
        
        
        
        hbox = gtk.HBox(False,5)
        
        label = gtk.Label('  Select Tag :\r\n')
        self.size_group_0.add_widget(label)
        hbox.pack_start(label,False, False, 0)
        
        tagEntry = gtk.TextView()#gtk.Entry()
        widgetPack['tagEntry'] = tagEntry
        widgetPack['refresh'] = buttonRefresh
        textbuffer = tagEntry.get_buffer()
        
        txt = widget_pack_ret['entry'].get_text()
        textbuffer.set_text(txt)
        #entryDisp.set_max_length(100)
        #entryDisp.set_size_request(100, 20)
        
        '''tagEntry.set_text (txt)
        tagEntry.set_editable(True)'''
        tagEntry.set_size_request(560, 36)
        tagEntry.set_wrap_mode(gtk.WRAP_CHAR)
        #tagEntry.show()
        hbox.pack_start(tagEntry,False, False, 0)
        
        vbox.pack_start(hbox,True)#False, False, 0)
        
        
        
        vbox.pack_start(frame, True)
        
        #model = MyTreeModel()
        #model = model.filter_new()
        # create a TreeStore with one string column to use as the model
        
        treestore =self.getTaglist() # load opc tag list function
        # create the TreeView using treestore
        self.treeview = gtk.TreeView(treestore)

        # create the TreeViewColumn to display the data
        self.tvcolumn = gtk.TreeViewColumn('')

        # add tvcolumn to treeview
        self.treeview.append_column(self.tvcolumn)

        # create a CellRendererText to render the data
        self.cell = gtk.CellRendererText()

        # add the cell to the tvcolumn and allow it to expand
        self.tvcolumn.pack_start(self.cell, True)

        # set the cell "text" attribute to column 0 - retrieve text
        # from that column in treestore
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        # make it searchable
        self.treeview.set_search_column(-1)
        
        #self.treeview.set_enable_tree_lines(True)
        # Allow sorting on the column
        #self.tvcolumn.set_sort_column_id(0)

        # Allow drag and drop reordering of rows
        self.treeview.set_reorderable(False)
        #self.treeview.row_expanded(20)
        #self.treeview.expand_all()
        '''tree_view = gtk.TreeView(model)
        cell = gtk.CellRendererText()
        # the text in the column comes from column 0
        column = gtk.TreeViewColumn("OPC Server", cell, text=0)
        tree_view.append_column(column)'''
        
        
        
        scrolled_window.add(self.treeview)
        
        
        

        
        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_END
        bbox.set_layout(layout)
        bbox.set_spacing(10)
        

        buttonAdd = gtk.Button(stock='gtk-add')
        bbox.add(buttonAdd)
        buttonAdd.connect("clicked", self.add_tag_item,widget_pack_ret,tagEntry,self.window)
        buttonAdd.show()
        bbox.show()
        
        buttonConnect.connect("clicked", self.connect,self.treeview,treestore)
        buttonFind.connect("clicked", self.startSearch,self.treeview,treestore)
        #buttonDisconnect.connect("clicked", self.disconnect,self.treeview)
        buttonRefresh.connect("clicked", self.refresh,self.treeview,treestore)#gtk.ListStore.clear, self.liststore
        #buttonRefresh.connect_object("clicked", gtk.TreeStore.clear, treestore)
        #self.treeview.connect("row-activated", self.double_click_tree)
        #self.treeview.add_events(gtk.gdk.BUTTON_PRESS_MASK )
        self.treeview.connect("button-press-event", self._click_press_tree, treestore,widget_pack_ret,tagEntry,self.window)
        self.treeview.connect("button_release_event", self._click_tree,tagEntry,widget_pack_ret)
        #self.treeview.connect("clicked",self.click_treview)

        #Apply Button 
        self.buttonApply = gtk.Button(stock='gtk-apply')
        self.buttonApply.connect("clicked",self.apply_change)
        bbox.add(self.buttonApply)
        self.buttonApply.show()
        self.buttonApply.set_sensitive(False) # enable when update new bacnet point
        
        def close_dialog(self,window,tagEntry):
            #itemPropertySelect.window = None
            print "close dialog"
            #global_var.dialogOPCbrowe.hide()
            window.destroy()
            gtk.main_quit() # enable for delete all signal 
            return False
            
            #window.destroy()
            
        buttonClose = gtk.Button(stock='gtk-close')
        buttonClose.connect("clicked",close_dialog,self.window,tagEntry)
        bbox.add(buttonClose)
        buttonClose.show()
        self.window.set_resizable(False)
        # start search and auto expandded treeview match item on text view
        self.startSearch(None,self.treeview,treestore)
        self.window.show_all()
        
    def popupMenu(self,event,state,treeview, treestore):
        print "Popup menu on treeview"
        menu = gtk.Menu()
        
        if state == 'find_bacnet':
            browe = gtk.MenuItem("Browe device")
            browe.connect("activate",self.browe_device,treeview,treestore)
            browe.show()
            
            add = gtk.MenuItem("Add device")
            add.connect("activate",self.add_device_manual,treeview, treestore)# add devcie by manual 
            add.show()
            
            menu.append(add)
            menu.append(browe)
            
        if state == 'find_opc_server':
            browe = gtk.MenuItem("Find OPC Server")
            browe.connect("activate",self.find_opc_server,treeview,treestore)
            browe.show()
            
            add = gtk.MenuItem("Add")
            add.connect("activate",self.add_device_manual,treeview, treestore)# add devcie by manual 
            add.show()
            
            menu.append(add)
            menu.append(browe)
        
        if state == 'add_local_sub2':
            edit_item = gtk.MenuItem("Edit")
            edit_item.connect("activate",self.add_local_item,treeview, treestore,None,'edit')# edit devcie by manual 
            edit_item.show()
            
            menu.append(edit_item)
            
            delete_item = gtk.MenuItem("Delete")
            delete_item.connect("activate",self.deleteLocalItem,treeview, treestore)# add devcie by manual 
            delete_item.show()
            
            menu.append(delete_item)
            
            sep1 = gtk.SeparatorMenuItem() # separate
            sep1.show()
            menu.append(sep1)
            
            prop = gtk.MenuItem("Property")
            prop.connect("activate",self.dialogProperty,treeview, treestore)
            prop.show()
            menu.append(prop)
            
            
        if state == 'add_local_sub':

            add = gtk.MenuItem("Add Item")
            default = "Item name","None"
            add.connect("activate",self.add_local_item,treeview, treestore,default,'add')# add devcie by manual 
            add.show()
            menu.append(add)
            
            sep1 = gtk.SeparatorMenuItem() # separate
            sep1.show()
            menu.append(sep1)
            
            edit_item = gtk.MenuItem("Edit")
            edit_item.connect("activate",self.add_local_item,treeview, treestore,None,'edit') 
            edit_item.show()
            
            menu.append(edit_item)
            
            delete_item = gtk.MenuItem("Delete")
            delete_item.connect("activate",self.deleteDevice,treeview, treestore)# add devcie by manual 
            delete_item.show()
            
            menu.append(delete_item)
            
            sep1 = gtk.SeparatorMenuItem() # separate
            sep1.show()
            menu.append(sep1)
            
            prop = gtk.MenuItem("Property")
            prop.connect("activate",self.dialogProperty,treeview, treestore)
            prop.show()
            menu.append(prop)
            
        if state == 'add_local':
            
            add_group = gtk.MenuItem("Add Group")
            #add_local_group(self,treeview, treestore):
            add_group.connect("activate",self.add_local_group,treeview, treestore,"Group")# add devcie by manual 
            add_group.show()
            menu.append(add_group)
            
            add = gtk.MenuItem("Add Item")
            default = "Item name","None"
            add.connect("activate",self.add_local_item,treeview, treestore,default,'add')# add devcie by manual 
            add.show()
            menu.append(add)
            
        if state == 'refresh_bacnet':
            refresh = gtk.MenuItem("Connect")
            refresh.connect("activate",self.refresh_bacnet_tag,treeview, treestore)
            refresh.show()
            menu.append(refresh)
            
            file = gtk.MenuItem("Load from file..")
            file.connect("activate",self.importBacnetFromFile,treeview, treestore)
            file.show()
            menu.append(file)
            
            export = gtk.MenuItem("Export to..")
            file_type = "bacnet file","*.bac"
            export.connect("activate",self.exportFile,treeview, treestore,file_type)
            export.show()
            menu.append(export)
            
            
            sep1 = gtk.SeparatorMenuItem() # separate
            sep1.show()
            menu.append(sep1)
            
            delete = gtk.MenuItem("Delete")
            delete.connect("activate",self.deleteDevice,treeview, treestore)
            delete.show()
            menu.append(delete)
            
            prop = gtk.MenuItem("Property")
            prop.connect("activate",self.dialogProperty,treeview, treestore)
            prop.show()
            menu.append(prop)
            
            
        if state == 'refresh':
            refresh = gtk.MenuItem("Probe")
            refresh.connect("activate",self.read_opc_all,treeview, treestore)
            refresh.show()
            menu.append(refresh)
            
            file = gtk.MenuItem("Load from file..")
            file.connect("activate",self.importOPCFromFile,treeview, treestore)
            file.show()
            menu.append(file)
            
            export = gtk.MenuItem("Export to..")
            file_type = "opc file","*.opc"
            export.connect("activate",self.exportFile,treeview, treestore,file_type)
            export.show()
            menu.append(export)
            
            
            edit  = gtk.MenuItem("Edit")
            edit.show()
            edit.connect("activate",self.edit_opcserver,treeview, treestore)
            menu.append(edit)
            
            sep1 = gtk.SeparatorMenuItem() # separate
            sep1.show()
            menu.append(sep1)
            
            delete = gtk.MenuItem("Delete")
            delete.connect("activate",self.deleteDevice,treeview, treestore)
            delete.show()
            menu.append(delete)
            
            prop = gtk.MenuItem("Property")
            prop.connect("activate",self.dialogProperty,treeview, treestore)
            prop.show()
            menu.append(prop)
            #refresh.connect("activate",self.browe_device,treeview)
            
        menu.popup(None, None, None, event.button, event.time, None)
        
    # Read OPC Server From Configure
    #TODO: Read OPC ALL
    def read_opc_all(self,widget,tree_view,treestore):
        selection = tree_view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_item = tree_model.get_value(iter, 0)
        print "get opc server name ",selected_item
        parent_item = tree_model.iter_parent(iter)
        selected_parent = tree_model.get_value(parent_item, 0)
        #print "Read all opc server",selected_parent
        ip = self.tagList[selected_parent][selected_item]['property']['ip']
        port = self.tagList[selected_parent][selected_item]['property']['port']
        print "connect server address %s port %s " %(ip,port)
        
        #Popup OPC browser 
        #Load from progress_find_opc.py 
        #getOPC =  load_opc_server()
        #getOPC.start()
        print "OPC List ",self.tagList['OPC']
        #getOPC.OPCProbe()
        #TODO : probe opc on server
        #With ladon Webservice
        '''try:
            listOPC = webclient.getOpcServer('--all')
            #server = listOPC[0]
            print '*****************'
            result = ''
            for j in listOPC:
                result= result+j+'\r\n'
            print '*****************'
    
            #result = webclient.testCalculator()
            print 'From response',result
            self.warning_dialog(str(result))
        except Exception,e:
            result = e
            print str(result)
            self.warning_dialog(str(e))'''
            
        #With Pyro Remote Object
        #waiting cursor 
        watch = gtk.gdk.Cursor(gtk.gdk.WATCH)
        tree_view.window.set_cursor(watch)
        
        try:
            result= pyroweb_client.get_opc_all(ip,port)
        except Exception,err:
            result = str(err)
            
        if str(type(result)) == '<type \'str\'>':
            print "Error : ",result
            self.warning_dialog(result)
        else:
            for g in result:
                print g
            waiting_confirm = False
            print self.popup_opc_list(result,waiting_confirm)
            
            
        tree_view.window.set_cursor(None)

    def warning_dialog(self,MESSAGE):
        dialog = gtk.MessageDialog(None,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,MESSAGE)
                                    
        dialog.set_position(gtk.WIN_POS_CENTER)
        dialog.run()
        dialog.destroy()
        
    def popup_opc_list(self,list_server,waiting_confirm):
        print "Popup OPC List"
        '''window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.set_size_request(200, 320)
        window.set_title("OPC Server Selected")
        window.set_resizable(False)
        window.set_decorated(False)
        window.set_modal(True)
        window.show()'''
        #dia = DialogOPCList(self.window,list_server,waiting_confirm)
        result = self.opc_dialog(list_server)
        #dia =
        print "Retuen select opc server ",result
        db = TagDatabase(result)
        #db.load_db(result)
        
        #return global_var.select_server_opc
        
    def opc_dialog(self,list_server):
        #TODO : opc dialog
        dialog = gtk.Dialog("Selected OPC Server",
                   self.window,
                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_OK,gtk.RESPONSE_ACCEPT,gtk.STOCK_CANCEL,gtk.RESPONSE_REJECT))

        
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)#gtk.POLICY_NEVER
        sw.set_size_request(250, 180)
        sw.show()
        
        #Create Treeview
        # create tree model
        model = self.__create_model(list_server)
        data = None
        # create tree view
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        treeview.set_search_column(COLUMN_DESCRIPTION)
        treeview.connect("row-activated", self.double_click_tree)
        #treeview.connect("button_release_event", self.on_activated)
        # add columns to the tree view
        self.__add_columns(treeview)
        treeview.show()


        sw.add(treeview)
        dialog.vbox.pack_start(sw,False,True,0)
        

        #window.vbox.pack_start(notebook)
        
        
        
        
        
        
        

        response = dialog.run()
        server_select = []
        if response == -3:
            
            tree_model = treeview.get_model()
            iter = tree_model.get_iter_root()
            while iter:
                if tree_model.get_value(iter, 0):
                    server_select.append(tree_model.get_value(iter, 1))
                #print tree_model.get_value(iter, 1), tree_model.get_value(iter, 0)
                iter = tree_model.iter_next(iter)
        #print response
        dialog.destroy()
        
        return server_select
        
        
    def __create_model(self,list_server):
        lstore = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING)

        data = []#[[True,'TEST'],[False,'Duoble']]
        for g in list_server:
            data.append([True,g])
        
        for item in data:
            iter = lstore.append()
            lstore.set(iter,
                COLUMN_FIXED, item[COLUMN_FIXED],
                COLUMN_DESCRIPTION, item[COLUMN_DESCRIPTION])
                #COLUMN_DESCRIPTION, item[COLUMN_DESCRIPTION])
        return lstore
    
    def __add_columns(self, treeview):
        model = treeview.get_model()

        # column for fixed toggles
        
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.selected_toggled, model)

        column = gtk.TreeViewColumn('Select', renderer, active=COLUMN_FIXED)
        # set this column to a fixed sizing(of 60 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(60)

        treeview.append_column(column)

        # columns for severities
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('OPC Server Name',renderer ,
                                    text=COLUMN_DESCRIPTION)
        
        #column.set_sort_column_id(COLUMN_SEVERITY)
        #column.connect("clicked", self.select_data)
        column.set_fixed_width(50)
        treeview.append_column(column)
        
    def double_click_tree(self,widget,model,iter):
        selected_server = []
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_layer = tree_model.get_value(iter, 1)
        print selected_layer
        print 'edit name press to set new value'
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        if iter:
            pass  
            return selected_server
        return None
    
    def selected_toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, COLUMN_FIXED)
        # do something with the value
        fixed = not fixed
        # set new value
        model.set(iter, COLUMN_FIXED, fixed)

        
        
    def refresh(self,widget,tree_view,treestore):
        print 'button refresh'
        
        '''selection = tree_view.get_selection()
        model, iter = selection.get_selected()
        
        match_iter = self.search(model, model.iter_children(None), 
                            self.match_func, (0, 'PLC Bldg A FL2'))
        print 'Search result :',match_iter
        #tree_view.expand_to_path(match_iter)
        treeStore.clear()
        
        # Load new tag item
        self.load_new_item(treestore,False)'''
        exp = 1,0,2
        #tree_view.expand_row(exp, open_all=False)
        for i in range(len(exp)):
            tree_view.expand_row(exp[:i+1], open_all=False)
        
        return True
    
        
    def refresh_bacnet_tag(self,widget,treeview,treestore):
        self.buttonApply.set_sensitive(True)
        print "refresh bacnet tag"
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_device = tree_model.get_value(iter, 0)
        print "select device is ",selected_device
        print "select device id ",self.tagList['Bacnet IP'][selected_device]['device_id']
        widgetPack = {'treeview':treeview,'treestore':treestore} # send widget to class
        widgetPack['device_name'] = selected_device
        widgetPack['device_net'] = self.tagList['Bacnet IP'] # keep bacnet data base
        widgetPack['device_id'] = self.tagList['Bacnet IP'][selected_device]['device_id'] # bacnet device id
        
        tag = progress_bacnet()
        tag.get_bacnet_tag(widgetPack)
        
    def save_file(self,file_type):
        dialog = gtk.FileChooserDialog("Open..",
                                       None,
                                       gtk.FILE_CHOOSER_ACTION_SAVE,
                                       (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                        gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        dialog.set_default_response(gtk.RESPONSE_OK)
        filter = gtk.FileFilter()
        filter.set_name(file_type[0])
        filter.add_pattern(file_type[1])
        dialog.add_filter(filter)
        FileSelect = None
        response = dialog.run()
        
        if response == gtk.RESPONSE_OK:
            FileSelect = dialog.get_filename()
        elif response == gtk.RESPONSE_CANCEL:
            print 'Closed, no files selected'
            FileSelect = None
        dialog.destroy()

        return FileSelect

    def search(self,tree_view, treestore, iter, search_data):
        
        tree_children = treestore.iter_n_children(iter)
        if tree_children >0:# Check iter not last
            iter = treestore.iter_children(iter)
            while iter:
                value = treestore.get_value(iter, 0)
                path = treestore.get_path(iter)
                selected_value = treestore.get_value(iter, 0)
                if len(path)> len(search_data):
                    return True
                if selected_value == search_data[len(path)-1]:
                    print "search match ",selected_value
                    path = treestore.get_path(iter)
                    for i in range(len(path)):
                        tree_view.expand_row(path[:i+1], open_all=False) # expanded treeview on found item
                    self.search(tree_view, treestore, iter, search_data)
                    iter = treestore.iter_next(iter)
                    return True
                else:
                    self.search(tree_view, treestore, iter, search_data)
                    iter = treestore.iter_next(iter)
            
            return True
                
        else:
            return True

    def spiltOPCParent(self,opc_root,tag,iter,treestore):
        if len(tag) >0:
            t0 = tag[0] # select first parent opc group
            t1 = tag[1:len(tag)] # second to last opc group 
            if opc_root.has_key(t0) == False:
                #print t0
                opc_root[t0] = {}
            #else:
            #    iter1 = iter
                #opc_root[t0] = []
            #iter1 = treeStore.append(iter,[t0])
            
            self.spiltOPCParent(opc_root[t0],t1,iter,treestore)
        
    def startSearch(self,widget,tree_view,treestore):

        textbuffer = widgetPack['tagEntry'].get_buffer()
        start_iter = textbuffer.get_start_iter()
        end_iter = textbuffer.get_end_iter()
        select_Tag = textbuffer.get_text(start_iter,end_iter)
        # Replace unseen charector
        search_tag = select_Tag.replace('\r','')
        search_tag = search_tag.replace('\n','')
        search_tag = select_Tag.split('.')
        
        print 'you select tag entry is ',select_Tag
        iter = treestore.get_iter_first()
        print "treeview children ",treestore.iter_n_children(iter)
        print '----------------search area -----------------'
        while iter :
            selected_value =treestore.get_value(iter, 0)
            if selected_value == search_tag[0]:
                print "Search under root --> ",selected_value
                self.search(tree_view, treestore, iter, search_tag)  
            iter =treestore.iter_next(iter)
        return True
                    
    def warning_dialog(self,MESSAGE):
        dialog = gtk.MessageDialog(self.window,
                                    gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                    gtk.MESSAGE_WARNING, gtk.BUTTONS_OK,MESSAGE)
        
        dialog.run()
        dialog.destroy()
        
    
        
        
        
class DialogOPCList(gtk.Dialog):
    
    select_server_opc = []
    
    def __init__(self,win,list_server,waiting_confirm):
        
        self.waiting_confirm = waiting_confirm
        
        window = gtk.Dialog(parent=win, flags=0)
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        
        
        
        window.set_title("OPC SERVER SELECT")
        window.set_resizable(False)
        window.set_modal(True)
        window.set_destroy_with_parent(True)
        #Set Scroll windwo 
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)#gtk.POLICY_NEVER
        sw.set_size_request(250, 180)
        sw.show()
        
        #Create Treeview
        # create tree model
        model = self.__create_model(list_server)
        data = None
        # create tree view
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        treeview.set_search_column(COLUMN_DESCRIPTION)
        treeview.connect("row-activated", self.double_click_tree)
        #treeview.connect("button_release_event", self.on_activated)
        # add columns to the tree view
        self.__add_columns(treeview)
        treeview.show()


        sw.add(treeview)
        window.vbox.pack_start(sw,False,True,0)
        
        
        #Create button group ok and cancel
        bbox = gtk.HButtonBox()
        bbox.set_border_width(5)
        bbox.set_layout(gtk.BUTTONBOX_END)
        
        #Insert the O.k. button
        button = gtk.Button(stock=gtk.STOCK_OK)
        button.connect("clicked", self.confirm_button,window,treeview,model,iter)
        button.show()
        bbox.add(button)
        bbox.set_spacing(5)
        
        # Insert the Cancel button
        button = gtk.Button(stock=gtk.STOCK_CANCEL)
        button.connect("clicked", self.cancel_event,window)
        button.show()
        bbox.add(button)
        
       
        bbox.show()
        window.vbox.pack_start(bbox, False, False, 2)
        #window.vbox.pack_start(notebook)
        
        
        
        #window.add(vbox)
        window.set_size_request(-1, -1)
        window.show()
        
        
        
    def double_click_tree(self,widget,model,iter):
        selected_server = []
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_layer = tree_model.get_value(iter, 1)
        print selected_layer
        print 'edit name press to set new value'
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        if iter:
            pass  
            return selected_server
        return None
        
    def cancel_event(self,button,window):
        print "Cancel Selected OPC Server"
        self.waiting_confirm = True # send signal exit
        window.destroy()
        
    def confirm_button(self,button,window,widget,model,iter):
        print "OK Button for Add OPC Server"
        
        tree_model = widget.get_model()
        iter = tree_model.get_iter_root()
        del global_var.select_server_opc[:] #clear all item 
        while iter:
            if tree_model.get_value(iter, 0):
                global_var.select_server_opc.append(tree_model.get_value(iter, 1))
            #print tree_model.get_value(iter, 1), tree_model.get_value(iter, 0)
            iter = tree_model.iter_next(iter)

        self.waiting_confirm = True # send signal exit
        window.destroy()
        
    
    
        
        
    def __create_model(self,list_server):
        lstore = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING)

        data = []#[[True,'TEST'],[False,'Duoble']]
        for g in list_server:
            data.append([True,g])
        
        for item in data:
            iter = lstore.append()
            lstore.set(iter,
                COLUMN_FIXED, item[COLUMN_FIXED],
                COLUMN_DESCRIPTION, item[COLUMN_DESCRIPTION])
                #COLUMN_DESCRIPTION, item[COLUMN_DESCRIPTION])
        return lstore
    
    def __add_columns(self, treeview):
        model = treeview.get_model()

        # column for fixed toggles
        
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.selected_toggled, model)

        column = gtk.TreeViewColumn('Select', renderer, active=COLUMN_FIXED)
        # set this column to a fixed sizing(of 60 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(60)

        treeview.append_column(column)

        # columns for severities
        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn('OPC Server Name',renderer ,
                                    text=COLUMN_DESCRIPTION)
        
        #column.set_sort_column_id(COLUMN_SEVERITY)
        #column.connect("clicked", self.select_data)
        column.set_fixed_width(50)
        treeview.append_column(column)
        
    
    def selected_toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, COLUMN_FIXED)
        # do something with the value
        fixed = not fixed
        # set new value
        model.set(iter, COLUMN_FIXED, fixed)
        
    
class TagDatabase():
    def __init__(self,server_list):
        print "Create Tag Database use SQLite3"
        self.server_list = server_list
        
    def get_opc_on_database(self):
        rows =None
        try:
            con = lite.connect('tag.db')
            cur = con.cursor()    
            cur.execute("SELECT * FROM OPC")
            rows = cur.fetchall()
        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            
            
        finally:
            if con:
                con.close()
            
        return rows
        
    def load_db(self,server_list):
        
        con = None
        database_name = "tag.db"

        try:
            con = lite.connect('tag.db')
            
            cur = con.cursor()    
            
            cur.execute("SELECT * FROM OPC")

            rows = cur.fetchall()
            # read opc tag in database
            for row in rows:
                print row
                if row[1] in server_list:
                    print "OPC Server name %s has already exist in database can't update!" %(row[1])
                    server_list.remove(row[1]) # remove from list 
            
            with con:
            
                cur = con.cursor() 
                if not os.path.isfile(database_name):
                    print "the database already exist" 
                    print "create new database table OPC"  
                    cur.execute("CREATE TABLE OPC(Id INTEGER PRIMARY KEY,Server TEXT,Port INT)")

                #cur.execute("INSERT INTO OPC(Server,port) VALUES ('OPC_TEST',7777)")
                for j in server_list:
                    sql = "INSERT INTO OPC(Server,Port) VALUES (\'"+str(j)+"\',7777)"
                    print sql
                    cur.execute(sql)
                    
            
        except lite.Error, e:
            
            print "Error %s:" % e.args[0]
            
        finally:
            if con:
                con.close()
    

if __name__ == "__main__":
    
    item = None
    entry = gtk.Entry()
    entry.set_text("OPC item value")
    widgetPack['entry'] = entry 
    loadItem = getOpcItem(item,widgetPack)
    #myOPC = loadItem
    gtk.main ()
    
    
