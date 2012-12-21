#!/usr/bin/env python
# -*- coding:utf-8 -*-

#  notebook.py

import pygtk
pygtk.require('2.0')
import gtk,gobject
import os

(
    COLUMN_FIXED,
    COLUMN_NUMBER,
    COLUMN_SEVERITY,
    COLUMN_DESCRIPTION
) = range(4)

data = ((False, False, 'Primary', 'scrollable notebooks and hidden tabs'),
 (False, False, 'Second',
  'gdk_window_clear_area(gdkwindow-win32.c) is not thread-safe'),
 (False, False, 'New Layer', 'Xft support does not clean up correctly'),
 (True,  False, 'New Layer', 'GtkFileSelection needs a refresh method. '),
 (False, False, 'New Layer', "Can't click button after setting in sensitive"),
 (True,  True, 'New Layer', 'GtkLabel - Not all changes propagate correctly'),
 (False, False, 'New Layer', 'Rework width/height computations for TreeView'))

dataRead = []



class DialogPoperty:
    global CURRENT_LAYER
    CURRENT_LAYER = 0
    def add_icon_to_button(self,button,iconpath):
    #"Function that add the icon to the button"
    #Hbox creation
        iconBox = gtk.HBox(False, 0)
    #Empty image creation
        image = gtk.Image()
    #Let's get the default gtk close button
        #image.set_from_stock(gtk.STOCK_CLOSE,gtk.ICON_SIZE_BUTTON) #gtk.ICON_SIZE_MENU
        image.set_from_file(iconpath)
    #set the relief off
        gtk.Button.set_relief(button,gtk.RELIEF_NONE)
    #Get the settings of the button
        settings = gtk.Widget.get_settings(button)
    #w and h dimensions of the button
        (w,h) = gtk.icon_size_lookup_for_settings(settings,gtk.ICON_SIZE_BUTTON)
    #modification of the dimensions
        gtk.Widget.set_size_request(button, w + 15, h + 15)
        image.show()
    #pack the image in the box
        iconBox.pack_start(image, True, False, 0)
    #add the box in the button
        button.add(iconBox)
        iconBox.show()
        return

    def create_custom_tab(self,text, notebook, frame,id,iconpath):
        "Create a custom tab with a label and the button"
    #eventbox creation
        eventBox = gtk.EventBox()
    #Hbox creation
        tabBox = gtk.HBox(False, 2)
    #"text" label creation
        #tabLabel = gtk.Label(text)
    #creation of a button
        tabButton=gtk.Button()
    #connect to the "remove_book" function
        #tabButton.connect('clicked',self.remove_book, notebook, frame)
        tabButton.connect('clicked',self.set_active_book, notebook, frame,id)

        #add the icon with the previously defined add_icon_to_button
        self.add_icon_to_button(tabButton,iconpath)

        eventBox.show()
        tabButton.show()
        #tabLabel.show()
    #add label and button
        #tabBox.pack_start(tabLabel, False)
        tabBox.pack_start(tabButton, True)

        tabBox.show_all()
    #add the box to the eventox
        eventBox.add(tabBox)
        return eventBox

    def set_active_book(self, button, notebook, frame,id):
        notebook.set_current_page(id)
        print 'notebook current id = '+str(id)

    def remove_book(self, button, notebook, frame):
    #"Function to remove the page"
    #suppress the page. You must give the child widget of the page
        notebook.remove(frame)
        # you call the previous page
        notebook.queue_draw_area(0,0,-1,-1)

    def delete(self, widget, event=None):
        print 'close main window layer'
        global dataRead
        print 'show data len ' + str(len(dataRead ))
        lendata = len(dataRead )
        del dataRead[:lendata]
        widget.destroy()
        #del model#gtk.main_quit()
        return True
    
    def on_activated(self, widget,data):
        '''selection = treeview.get_selection()
        model, iter = selection.get_selected()'''
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_user = tree_model.get_value(iter, 2)

        '''row = 0
        model = widget.get_model()
        text = str(model[row][0]) + ", " + str(model[row][1]) + ", " + model[row][2]'''
        print selected_user
        #self.statusbar.push(0, text)
    def double_click_tree(self,widget,model,iter):
        selection = widget.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_layer = tree_model.get_value(iter, 2)
        print selected_layer
        print 'edit name press to set new value'
        selection = widget.get_selection()
        model, iter = selection.get_selected()
        if iter:
            label = gtk.Label("  Edit layer name")
            entry = gtk.Entry()
            entry.set_text(selected_layer)
            dialog = gtk.Dialog("Edit layer name",
                               None,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                                gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                                
            hbox = gtk.HBox(False,0)
            hbox.show()
            hbox.pack_start(label,False,False,0)
            dialog.vbox.pack_start(hbox)
            dialog.vbox.pack_start(entry)
            dialog.set_resizable(False)
            label.show()
            entry.show()
            response = dialog.run()
            if response == -2:
                layer_name = entry.get_text()
                if len(layer_name) >0 and selected_layer != 'Primary' :
                    model.set_value(iter,2,layer_name)
                    #self.treeview_refresh(treeview_refresh,treeview,model,iter,combobox) # call refresh new value
                
            dialog.destroy()    
                    
        #self.treeview_refresh(treeview_refresh,treeview,model,iter,combobox)
        return
    
    def addList(self):
        print 'start list' 
        vbox = gtk.VBox(False, 0)
        sw = gtk.ScrolledWindow()
        sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
        sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)#gtk.POLICY_NEVER
        sw.set_size_request(250, 180)
        vbox.pack_start(sw,False,True,0)

        # create tree model
        model = self.__create_model()
        data = None
        # create tree view
        treeview = gtk.TreeView(model)
        treeview.set_rules_hint(True)
        treeview.set_search_column(COLUMN_DESCRIPTION)
        treeview.connect("row-activated", self.double_click_tree)
        treeview.connect("button_release_event", self.on_activated)



        sw.add(treeview)

        # add columns to the tree view
        self.__add_columns(treeview)
        sw.show()
        treeview.show()
        vbox.show()
        
        return vbox,treeview,model
    
    def rename_layer(self,treeview_refresh,treeview,model,iter,combobox):    
        
        selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_layer = tree_model.get_value(iter, 2)
        print selected_layer
        print 'edit name press to set new value'
        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            label = gtk.Label("  Edit layer name")
            entry = gtk.Entry()
            entry.set_text(selected_layer)
            dialog = gtk.Dialog("Edit layer name",
                               None,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                                gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                                
            hbox = gtk.HBox(False,0)
            hbox.show()
            hbox.pack_start(label,False,False,0)
            dialog.vbox.pack_start(hbox)
            dialog.vbox.pack_start(entry)
            dialog.set_resizable(False)
            label.show()
            entry.show()
            response = dialog.run()
            if response == -2:
                layer_name = entry.get_text()
                if len(layer_name) >0 and selected_layer != 'Primary' :
                    model.set_value(iter,2,layer_name)
                    self.treeview_refresh(treeview_refresh,treeview,model,iter,combobox) # call refresh new value
                
            dialog.destroy()    
                    
        #self.treeview_refresh(treeview_refresh,treeview,model,iter,combobox)
        return
        
    def on_key_press(self,widget, event,data):#, *args
        
        #event = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
        global keyEnter
        if event.keyval == 65293:
            print 'key press enter'
            keyEnter = True
            return True
        return False
    
    
    def add_layer(self,treeview_refresh,treeview,model,iter,combobox):
        print 'add layer press'
        layer_name = ''
        #addNew = EntryLayer()
        event = gtk.gdk.Event(gtk.gdk.KEY_PRESS)
        label = gtk.Label("  Add new layer")
        entry = gtk.Entry()
        entry.connect("key-press-event", self.on_key_press,event)

        dialog = gtk.Dialog("Add new layer dialog",
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_OK, gtk.RESPONSE_REJECT,
                            gtk.STOCK_CANCEL, gtk.RESPONSE_ACCEPT))
                            
        hbox = gtk.HBox(False,0)
        hbox.show()
        hbox.pack_start(label,False,False,0)
        dialog.vbox.pack_start(hbox)
        dialog.vbox.pack_start(entry)
        dialog.set_resizable(False)
        label.show()
        entry.show()
        '''checkbox = gtk.CheckButton("Useless checkbox")
        dialog.action_area.pack_end(checkbox)
        checkbox.show()'''
        global keyEnter
        keyEnter = False
        response = dialog.run()
        print keyEnter
        if response == -2:
            layer_name = entry.get_text()
            if len(layer_name) >0 :
                model.append([True,False,layer_name])
                self.treeview_refresh(treeview_refresh,treeview,model,iter,combobox) # call refresh new value
            
        dialog.destroy()
        #return layer_name
        
        
    
    def addButton(self,treeview,model,iter,combobox):
        global CURRENT_LAYER
        hbox = gtk.HBox(False, 0)
        listButton = [gtk.STOCK_ADD,gtk.STOCK_REMOVE,gtk.STOCK_EDIT,gtk.STOCK_REFRESH]
        buton_tooltip = ['add layer','delete layer','rename layer','refresh layer list']
        lenlist = len(listButton)
        for i in range(lenlist):
            image = gtk.Image()
            image.set_from_stock(listButton[i],gtk.ICON_SIZE_MENU)
            button = gtk.Button()
            button.add(image)
            button.set_tooltip_text(buton_tooltip[i])
            buttonType = listButton[i]
            if buttonType == gtk.STOCK_ADD : # Create Button remove only
                button.connect("clicked",self.add_layer,treeview,model,iter,combobox)
            
            if buttonType == gtk.STOCK_REMOVE : # Create Button remove only
                button.connect("clicked",self.clear_selected,treeview,model,iter,combobox)
                
            if buttonType == gtk.STOCK_EDIT : # Create Button remove only
                button.connect("clicked",self.rename_layer,treeview,model,iter,combobox)
            
            if buttonType == gtk.STOCK_REFRESH : # Create Button remove only
                button.connect("clicked",self.treeview_refresh,treeview,model,iter,combobox)    
            
            button.show()
            button.set_size_request(27,27)
            hbox.pack_start(button,False,True,0)
            image.show()
        hbox.show()
        return hbox
    def combo_select(self,widget):
        global CURRENT_LAYER
        index  = widget.get_active()
        if index != -1:
            CURRENT_LAYER = index
            print 'Current layer id =' + str(CURRENT_LAYER)


    def __init__(self,win):
        
        #window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window = gtk.Dialog(parent=win, flags=0)
        #window.set_border_width(1)
        #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.set_size_request(200, 320)
        window.set_title("Layer Property")
        window.set_resizable(False)
        #window.set_modal(True)
        window.set_destroy_with_parent(True)
        
        #window.set_skip_taskbar_hint(False)
        #window.set_decorated(False)

        #book generation
        global CURRENT_LAYER
        notebook = gtk.Notebook()
        #vbox = gtk.VBox(False, 5)
        #vbox.show()
        #vbox.pack_start(notebook,False,False,0)
        window.vbox.pack_start(notebook)
        current_dir = os.getcwd()
        notebook.show()
        #layerLabel = ['Layer']
        if os.name == 'nt':# check window os
            #pathImage = currentPath+ '\\images\\'
            path = current_dir+'\\images\\'
            pathLayer = current_dir+'\\configure\\layer.cfg'
        else: 
            #pathImage = currentPath+ '/images/'
            path = current_dir+'/images/'
            pathLayer = current_dir+'/configure/layer.cfg'
        # some pages
        
        iconTab = ['layer.gif','gradient_linear.gif']
        tooltip = ['Layer','Gradiant']
        #Load file layer.conf
        
        f = open(pathLayer,'r')
        #f.readline()
        #dataRead = []
        for rd in f:
            rawData = rd.replace('\n','') # read real data line
            filterData = rawData.split(',')
            dataRead.append(filterData)
        
        for i in range(2):
            
            vbox = gtk.VBox(False, 5)
            page_number = i + 1
            frame = gtk.Frame(tooltip[i])
            frame.set_border_width(0)
            frame.set_size_request(200, 400)
            frame.show()
            label = gtk.Label("Set current layer")
            label.show()
            
            hbox = gtk.HBox(False,0)
            hbox.pack_start(label,False,True,0)
            hbox.show()
            
            vbox.pack_start(hbox,False,True,0)
            
            combobox = gtk.combo_box_new_text()

            #combobox = gtk.ComboBox()
            combobox.set_size_request(100, 25)
            combobox.connect('changed',self.combo_select)
            #liststore = gtk.ListStore(str)

            for k in dataRead:
                #liststore.append([k[2]])
                combobox.append_text(k[2])
                

            
            combobox.set_active(CURRENT_LAYER)
            vbox.pack_start(combobox,False,True,0)
            
            
            listBox,treeview,model = self.addList()
            vbox.pack_start(listBox,False,False,0)
            bt = self.addButton(treeview,model,iter,combobox)
            vbox.pack_start(bt,False,False,0)
            #label.show()
            frame.add(vbox)
            combobox.show()
            vbox.show()
            iconpath = path + iconTab[i]
            eventBox = self.create_custom_tab("Tab   number  %d" % page_number,
            notebook, frame,i,iconpath)
            notebook.append_page(frame, eventBox)
        # page you see at the opening
        notebook.set_current_page(0)
        window.connect("destroy", self.delete)
        window.show()
        
    def changeToBool (self,input):
        if input == 'True':
            return True
        else:
            return False
        
    def __create_model(self):
        lstore = gtk.ListStore(
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_BOOLEAN,
            gobject.TYPE_STRING)
            #gobject.TYPE_STRING)

        for item in dataRead:
            iter = lstore.append()
            lstore.set(iter,
                COLUMN_FIXED, self.changeToBool(item[COLUMN_FIXED]),
                COLUMN_NUMBER, self.changeToBool(item[COLUMN_NUMBER]),
                COLUMN_SEVERITY, item[COLUMN_SEVERITY])
                #COLUMN_DESCRIPTION, item[COLUMN_DESCRIPTION])
        return lstore

    def fixed_toggled(self, cell, path, model):
        # get toggled iter
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, COLUMN_FIXED)

        # do something with the value
        fixed = not fixed

        # set new value
        model.set(iter, COLUMN_FIXED, fixed)
        
    def lock_toggled(self, cell, path, model):
        iter = model.get_iter((int(path),))
        fixed = model.get_value(iter, COLUMN_NUMBER)
        # do something with the value
        fixed = not fixed
        # set new value
        model.set(iter, COLUMN_NUMBER, fixed)
        
    def on_error(self, widget):
        md = gtk.MessageDialog(None, 
            gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, 
            gtk.BUTTONS_CLOSE, "The primary layer can't delete!")
        md.run()
        md.destroy()

        
    def clear_selected(self, button,treeview,model,iter,combobox):
        print 'Clear Press'
        '''selection = treeview.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        tree_model, iter = selection.get_selected()
        selected_layer = tree_model.get_value(iter, 2)
        print selected_layer'''
        selection = treeview.get_selection()
        model, iter = selection.get_selected()
        selected_layer = model.get_value(iter, 2)
        
        if selected_layer == 'Primary':
            self.on_error(self)
            return
        #Creat dialog confirm delete
        label = gtk.Label()
        text_waring = 'If you delete this layer the inner item will be transfer to primary layer.\nDo you want to continue?'
                            
        label.set_text(text_waring)
        dialog = gtk.Dialog("Delete layer..."+selected_layer,
                           None,
                           gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                           (gtk.STOCK_YES, gtk.RESPONSE_REJECT,
                            gtk.STOCK_NO, gtk.RESPONSE_ACCEPT))
                            
        hbox = gtk.HBox(False,0)
        hbox.show()
        hbox.pack_start(label,False,False,0)
        dialog.vbox.pack_start(hbox)
        #dialog.vbox.pack_start(entry)
        dialog.set_resizable(False)
        label.show()
                

        response = dialog.run()
        if response == -2:# Press OK Button
            if iter :
                model.remove(iter)
                self.treeview_refresh(button,treeview,model,iter,combobox) # refresh in combobox
        dialog.destroy()
        return

    def treeview_refresh(self, button,treeview,model,iter,combobox):
        print 'Press refresh and layer index = ' + str(CURRENT_LAYER)
        comboModel = combobox.get_model()
        lencm = len(comboModel)
        # Clear all list combobox model
        #while lencm !=0:
        comboModel = combobox.get_model()
        
        #comboModel.clear()
        lencm = len(comboModel)
        print 'combo len = ' + str(lencm)
        
        while lencm != 0:
            comboModel = combobox.get_model()
            lencm = len(comboModel)
            for v in range(lencm):
                combobox.remove_text(v)
            
        '''combobox.clear()
        combobox.set_model(None)'''
        
        
        model = treeview.get_model()
        lenModel = len(model)
        print 'treview item count = ' + str(lenModel)
        '''ls = gtk.ListStore(str) 
        for g in range(3):
            ls.append([str(g)])
            
        combobox.set_model(ls)'''
        combobox.set_active(0)
        text = ''
        for k in range(lenModel):
            #print model[k][2]
            #ls.append([model[k][2]])
            combobox.append_text(model[k][2])
            #combobox.insert_text(0,model[k][2])
            text = text + str(model[k][0]) + "," + str(model[k][1]) + "," + model[k][2]+'\n'
            
        combobox.set_active(CURRENT_LAYER)
        f = open(r'/home/sompoch/pro/minibas/configure/layer.cfg', 'w')
        f.write(text)
        f.close()
            #print text
        #print ls
        #combobox.set_model(ls)
        #combobox.set_text_column(0) 
        
        

    def __add_columns(self, treeview):
        model = treeview.get_model()

        # column for fixed toggles
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.fixed_toggled, model)

        column = gtk.TreeViewColumn('View', renderer, active=COLUMN_FIXED)

        # set this column to a fixed sizing(of 50 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(40)

        treeview.append_column(column)

         # column for bug numbers
        renderer = gtk.CellRendererToggle()
        renderer.connect('toggled', self.lock_toggled, model)

        column = gtk.TreeViewColumn('Lock', renderer, active=COLUMN_NUMBER)
        # set this column to a fixed sizing(of 50 pixels)
        column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_fixed_width(40)

        treeview.append_column(column)

        # columns for severities
        renderer = gtk.CellRendererText()
        #renderer.column.set_property( 'editable', True )
        column = gtk.TreeViewColumn('Name',renderer ,
                                    text=COLUMN_SEVERITY)
        
        #column.set_sort_column_id(COLUMN_SEVERITY)
        #column.connect("clicked", self.select_data)
        column.set_fixed_width(50)
        treeview.append_column(column)

        '''# column for description
        column = gtk.TreeViewColumn('Description', gtk.CellRendererText(),
                                     text=COLUMN_DESCRIPTION)
        column.set_sort_column_id(COLUMN_DESCRIPTION)
        treeview.append_column(column)'''
        
'''
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    win = gtk.Window()
    win.set_icon(None)
    win.connect("delete-event",gtk.main_quit)
    win.show()
    DialogPoperty(win)
    main()'''
