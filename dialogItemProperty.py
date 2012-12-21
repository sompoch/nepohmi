#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pygtk
pygtk.require('2.0')
import gtk,gobject
import os
import global_var
import goocanvas
from layer_panel import layerPanelProperty
from color_panel import colorPanelProperty
from gradiant_panel import gradiantPanelProperty
from line_panel import linePanelProperty
from text_panel import textPanelProperty

class DialogPoperty(gtk.Dialog):
    
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
        #print 'notebook current id = '+str(id)

    def remove_book(self, button, notebook, frame):
    #"Function to remove the page"
    #suppress the page. You must give the child widget of the page
        notebook.remove(frame)
        # you call the previous page
        notebook.queue_draw_area(0,0,-1,-1)

    def close_dialog(self,widget,event=None):
        print 'close main window layer'
        '''global dataRead
        print 'show data len ' + str(len(dataRead ))
        lendata = len(dataRead )
        del dataRead[:lendata]
        widget.destroy()'''
        #del model#gtk.main_quit()
        global_var.dialogItemValue['dialog_pos'] = widget.get_position()
        widget.hide()
        return True
    
    def add_icon_tab(self,frame,notebook,icon):
        image = gtk.Image()
        #image.set_from_file("CreateRect.gif")
        image.set_from_stock(icon, gtk.ICON_SIZE_DIALOG)
        image.show_all() 
      
        tab_image = gtk.Image()
        #tab_image.set_from_stock(icon, gtk.ICON_SIZE_MENU)
        tab_image.set_from_file(icon)
        #tab_image.show_all()

        box = gtk.HBox()
        box.pack_start(tab_image, False, False)
        box.pack_start(gtk.Label(" "), True, True)
        # set tab size here
        box.set_size_request(25, 25)        
        box.show_all()
        
        notebook.append_page(frame,box)
        #notebook.set_current_page()
        #notebook.set_tab_label(image, box)
    
    
    

    def __init__(self,win):
        #super(DialogPoperty, self).__init__()
        #window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window = gtk.Dialog(parent=win, flags=0)
        #window.set_border_width(1)
        #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        window.set_size_request(200, 400)
        
        window.set_title("Item Property")
        window.set_resizable(False)
        #window.set_modal(True)
        window.set_destroy_with_parent(True)
        window.connect("delete_event", self.close_dialog)
        #window.set_skip_taskbar_hint(False)
        #window.set_decorated(False)
        dgd=gtk.gdk.display_get_default()
        gsd=dgd.get_default_screen()
        #print " current screen resolution height=",gsd.get_height(),"width=",gsd.get_width()
        desktop_width = gsd.get_width()
        desktop_height = gsd.get_height()
        #desktop_width = 1345
        window.set_uposition((desktop_width-200), 100)
        #book generation
        global CURRENT_LAYER
        notebook = gtk.Notebook()
        #vbox = gtk.VBox(False, 5)
        #vbox.show()
        #vbox.pack_start(notebook,False,False,0)
        window.vbox.pack_start(notebook)
        notebook.set_scrollable(True)
        notebook.show()
        #layerLabel = ['Layer']
        
        # some pages
        
        iconTab = ['layer.gif','fill_solid.gif','line.gif','dynamic.png'] #,'gradient_linear.gif'
        headerLabel = ['Layer','Color','Line','Text']#'Gradiant'
        #Load file layer.conf
        current_dir = os.getcwd()
        if os.name == 'nt':# check window os
            path = current_dir+'\\images\\'
        else: 
            path = current_dir+'/images/'
        
        
        for i in range(4):
            if headerLabel[i] == 'Layer':
                
                ly = layerPanelProperty()
                frame = ly.createLayerWidget() # call def layer property from layer_panel.py
                
            if headerLabel[i] == 'Color':
                cl = colorPanelProperty()
                frame = cl.createColorWidget()
            
            '''if headerLabel[i] == 'Gradiant':
                cl = gradiantPanelProperty()
                frame = cl.createGradiantWidget()'''
                
            if headerLabel[i] == 'Line':
                cl = linePanelProperty()
                frame = cl.createLineWidget()
                
            if headerLabel[i] == 'Text':
                txt = textPanelProperty()
                frame = txt.createLineWidget()
                
                
            page_number = i
            iconpath = path + iconTab[i]
            #eventBox = self.create_custom_tab("Tab   number  %d" % page_number,
            #notebook,frame,i,iconpath)
            self.add_icon_tab(frame,notebook,iconpath)
            #notebook.append_page(frame, eventBox)
            #notebook.queue_draw_area(0,0,-1,-1)
        
        # page you see at the opening
        notebook.set_current_page(1)
        notebook.show_all()
        notebook.set_show_tabs(True)
        #window.connect("destroy", self.delete)
        window.show()
        print "show dialog property "
        global_var.dialogProperty = window
   
        
    
        
    

    

        '''# column for description
        column = gtk.TreeViewColumn('Description', gtk.CellRendererText(),
                                     text=COLUMN_DESCRIPTION)
        column.set_sort_column_id(COLUMN_DESCRIPTION)
        treeview.append_column(column)'''
        

def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    win = gtk.Window()
    win.set_icon(None)
    win.connect("delete-event",gtk.main_quit)
    win.show()
    dia = DialogPoperty(win)
    print dia
    main()
