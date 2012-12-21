#!python.exe
import site

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#NepoHMI version 0.1 Built 10-07-2011
#Writer by : Sompoch Thuphom , E-mail : mjko68@hotmail.com
#Development under linux ubuntu version 10.04,10.10,11.04
#Support python2.6.x , 2.7.x
#For windowxp,win7 or other platform this script need to 
#1.GTK+ Runntime 2.22 and pygtk 2.6
#2.python 2.6.5 for window
#3.PIL 1.6 (Python Image Libraty)
#4.OpenOPC the OPC opensource for python and window
'''------History of NepoHMI-----------
  29-11-2010  update multi selection and key item copy with CTRL + drag action
  09-12-2010  update selection , cursor pointer , move item to smooth
  24-12-2010 update OPC Brower
  29-12-2010 change project name from minibas to openhmi
  10-12-2010 create opc connecting via tcp/ip
  13-02-2011 update flassh item
  12-06-2011 update transform item and move new item by transform
  15-06-2011 changne project name from openhmi to NepoHMI 
  02-07-2011 update file system , save ,save as , new and support *.xgd format 
             for svg format can support on next version of nepohmi[may be NepoHMI v 0.2 or later].
  10-07-2011 update group item , copy ,cut ,past item  
  21-12-2012 Update project to http://github.com/sompoch/nepohmi
'''

import sys
import os
if os.name =='nt':
    sys.path.append('C:\\Python26\\Lib\\site-packages\\gtk-2.0')
import goocanvas
#import gtk

#import subprocess
import math
import colorsys
import time
import re
import pickle,StringIO,Image

#import gobject
import gtk.gdk
import gtk.keysyms
import cairo
import pango
import pangocairo
import global_var
import drawItem

from build_menu import *
from createCanvas import *
from itemProperty import *
from ui import *
from selectBox import *
from  colorPalette import *
from opcBrower import getOpcItem
from group_item import *
from popup_menu import * #call popup_menu.py on right click
#from on_running import item_pick_on_run
from dialogItemProperty import DialogPoperty


def on_motion_notify_canvas(canvas,area, event):
        #self.drag_action.on_motion_notify(event)
        #print 'motion'
        #print event.x,event.y
        
    if global_var.sel_press == True:
        global x1
        global y1
        '''w = event.x - x1
        h = event.y - y1
        global_var.sel_area.props.width = w
        global_var.sel_area.props.height = h'''
        print 'Refresh area selection'
    return True

def setup_canvas (canvas, units, units_name):
    data = [
    [100, 100, 200, 20, 10, 200, 310, 24],
    [100, 100, 200, 20, 10, 200, 310, 24],
    [1, 1, 3, 0.5, 0.16, 3, 4, 0.3],
    [30, 30, 100, 10, 5, 80, 60, 10]
    ]

    d = data[0]

    root = canvas.get_root_item ()

    item = goocanvas.Rect (parent = root,
                           x = d[0],
                           y = d[1],
                           width = d[2],
                           height = d[3])
    
    #item.connect ("motion_notify_event", on_motion_notify_canvas)

    buffer = "This is %gx%g %s" % (d[2], d[3], units_name)
    font_desc = "Sans %gpx" % d[4]
    
    item = goocanvas.Text (parent = root,
                           text = buffer,
                           x = d[0] + d[2] / 2,
                           y = d[1] + d[3] / 2,
                           width = -1,
                           anchor = gtk.ANCHOR_CENTER,
                           font = font_desc)
    buffer = "This is %g %s high" % (d[7], units_name)
    font_desc = "Sans %gpx" % d[7]
    
    '''item.connect ("focus_in_event", on_focus_in)
    item.connect ("focus_out_event", on_focus_out)
    item.connect ("button_press_event", on_button_press)
    item.connect ("button_release_event", on_button_release)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)'''
    
    item = goocanvas.Text (parent = root,
                           text = buffer,
                           x = d[5],
                           y = d[6],
                           width = -1,
                           anchor = gtk.ANCHOR_CENTER,
                           font = font_desc)
                        
    '''item.connect ("focus_in_event", on_focus_in)
    item.connect ("focus_out_event", on_focus_out)
    item.connect ("button_press_event", on_button_press)
    item.connect ("button_release_event", on_button_release)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    image = gtk.Image()

        # use the current directory for the file
    try:
        pixbuf = gtk.gdk.pixbuf_new_from_file("/home/sompoch/pro/ubuntuclub.gif")
        #image.set_from_pixbuf(pixbuf)

    except gobject.GError, error:
        print 'error wth pixbuf'
        
    image = goocanvas.Image(pixbuf=pixbuf, x=100, y=100)'''

    




def _scroll(canvas,event):
    if event.direction == gtk.gdk.SCROLL_UP:
        zmIn = canvas.get_scale()+0.1
        canvas.set_scale(zmIn)
        model = global_var.comboboxZoom.get_model()
        current_scale = zmIn*100
        model[0][0]= str(int(current_scale))+'%'
        global_var.comboboxZoom.set_active(0)
        print 'scroll down zoom in'
    else:
        zmOut = canvas.get_scale()-0.1
        canvas.set_scale(zmOut)
        model = global_var.comboboxZoom.get_model()
        current_scale = zmOut*100
        model[0][0]= str(int(current_scale))+'%'
        global_var.comboboxZoom.set_active(0)
        print 'scroll up zoom out'
    #    self.zoom.set_value(self.zoom.get_value() - 2)
    #else:
    #    self.zoom.set_value(self.zoom.get_value() + 2)
        
def selection(item):
    pass
    return True




    
def set_item_delete(item):
    undo.undoListStore(global_var.undoList,'Delete Item',None,item,None)
    item.remove()
    global_var.bt['Copy'].set_sensitive(False)
    global_var.bt['Cut'].set_sensitive(False)
    global_var.bt['Delete'].set_sensitive(False)
    



def offset_selection(scale,scrolled_win,x1,y1):
    
    hAdj = scrolled_win.get_hadjustment()
    vAdj = scrolled_win.get_vadjustment()
    bound_x0 = global_var.dispProp['cvWidth']
    bound_y0 = global_var.dispProp['cvHeight']
    cavSizeW = global_var.dispProp['cvSizeWidth']
    cavSizeH = global_var.dispProp['cvSizeHeight']
    hValue = hAdj.get_upper()
    wValue = vAdj.get_upper()
    
    if (vAdj.get_upper() < (cavSizeH+5)) or (wValue < (1000)) :#bound_x0
        offset_x0 = (hValue-(bound_x0*scale))/2
        offset_y0 = (wValue-(bound_y0*scale))/2
        #print 'offset x, y = %s , %s ' % (offset_x0,offset_y0)
        new_x = (x1-offset_x0)/scale
        new_y = (y1-offset_y0)/scale
    else:
        new_x = x1/scale
        new_y = y1/scale# -  (y1/scale)/2
        
    #new_x = x1/scale
    #new_y = y1/scale# -  (y1/scale)/2'''
        
    return new_x,new_y




def color_set_cb(colorbutton):
    global boxcolor
    get_color = colorbutton.get_color()
    get_color = get_color.to_string()
    boxcolor = '#'+get_color[1:3]+get_color[5:7]+get_color[9:11]
    print "box color ",boxcolor
    global_var.graphic_default_setting['box_color'] = boxcolor # save new setting
    return

def colortext(c):
    ''' Convert color to 24 bit hex string '''
    s = '%02x%02x%02x' % (c.red>>8, c.green>>8, c.blue>>8)
    return s

def create_canvas (units, units_name):
    vbox = gtk.VBox (False, 4)
    vbox.set_border_width (4)
    hbox = gtk.HBox (False, 4)
    vbox.pack_start (hbox, False, False, 0)

    #global canvas
    #canvas = goocanvas.Canvas ()
    canvas.connect('button_press_event', on_right_click)
    canvas.connect("scroll-event", _scroll)
    #canvas.connect("button-press-event", self.on_button_press)
    #canvas.connect("button-release-event", self.on_button_release)
    #canvas.connect("motion-notify-event", self.on_motion_notify)
    canvas.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)

    canvas.set_flags(gtk.CAN_FOCUS) #Determines whether a widget is able to handle focus grabs.
    
    w = gtk.Label ("Zoom:")
    hbox.pack_start (w, False, False, 0)

    adj = gtk.Adjustment (1.00, 0.05, 100.00, 0.05, 0.50, 0.50)
    w = gtk.SpinButton (adj, 0.0, 2)
    adj.connect ("value_changed", zoom_changed, canvas)
    w.set_size_request (50, -1)
    hbox.pack_start (w, False, False, 0)

    global scrolled_win
    scrolled_win = gtk.ScrolledWindow ()
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC) #gtk.POLICY_NEVER 
    vbox.pack_start (scrolled_win, True, True, 0)

    # Create the canvas.
    #canvas.set_size_request (800, 600)
    #setup_canvas (canvas, units, units_name)
    x0 = global_var.dispProp['cvTop']# default 0
    y0 = global_var.dispProp['cvLeft']# default 0
    x1 = global_var.dispProp['cvWidth']# default 1024
    y1 = global_var.dispProp['cvHeight']# default 768
    print 'canvas read from global varible bounds %s ,%s ,%s , %s' % (x0,y0,x1,y1)
    canvas.set_bounds (x0, y0, x1, y1)
    canvas.props.units = units
    canvas.props.anchor = gtk.ANCHOR_CENTER
    #Change mouse cursor
    

    scrolled_win.add (canvas)
    #shwScroll = addAppMenu()
    #shwScroll(window)
   

    return vbox

def create_under_group(item,parent_edit):
    #parent1 = parent  on edit mode
    #TODO : create item under group
    if global_var.mode_run == False and global_var.edit_group_mode == True :
        #print 'Global button press =  %s ' % global_var.button_press
        parent_item = item.get_parent()
        child_num = parent_item.find_child(item)
        parent_item.remove_child(child_num)
        parent_edit.add_child(item, -1)
        x0,y0 = offset_parent_position(parent_edit)
        npx0 = global_var.sel_area.props.x-x0#(x0-item.props.x) #(parent_edit.props.x)
        npy0 = global_var.sel_area.props.y-y0#(y0-item.props.y) #(parent_edit.props.y)
        item.props.x = 0
        item.props.y = 0
        item.set_simple_transform(npx0,npy0,1,0)
        refresh_new_group_size() # update new group  size
        return True
    else:
        
        return False

def clear_all_multiSelected():
    lenGroup = len(global_var.multiSelect)
    #global_var.itemSelect8Cursor is dictionary and use item to index ...
    #global_var.itemSelect8Cursor['item of select']
    
    
    #print 'old group item select %s' %  lenGroup
    #---------Clear all multisetion cursor----------------
    if lenGroup>0:
        for t in global_var.multiSelect:
            for j in range(8):
                #try:
                if global_var.itemSelect8Cursor[t][j] is not None:
                    global_var.itemSelect8Cursor[t][j].remove()
                #except:
                 #   print 'Error when remove item Selection 8 cusor item is aready remove [nepohmi]'
                
        del global_var.multiSelect[0:lenGroup]
    lenGroupCursor = len(global_var.itemSelect8Cursor)
    
    if lenGroupCursor>0:
        global_var.itemSelect8Cursor.clear() # clear all data in dictionary
    #------End of Clear all selected cursor -------------
    print  "Start of print item selected"
    for t in global_var.multiSelect:
        print t
    global_var.itemSelectActive2 = None
    print  "End of print item selected"

def delete_all(canvas):
    print "delete all item on canvas"
    for itemSelect in global_var.select_cursor :
        global_var.select_cursor[itemSelect].remove()
        
    start_point = (canvas.props.x1, canvas.props.y1)
    end_point = (canvas.props.x2, canvas.props.y2)
    bounds = goocanvas.Bounds(*(start_point + end_point))
    overlaped_items = canvas.get_items_in_area(bounds, True, True, True)
    for j in overlaped_items:
        j.remove()
        
    #for img in global_var.image_store: # cleaer all imagae to store
    global_var.grid['grid'] =  drawItem.canvasGrid(canvas)
    if global_var.grid['show'] :
        global_var.grid['grid'].props.visibility =goocanvas.ITEM_VISIBLE
    else:
        global_var.grid['grid'].props.visibility =goocanvas.ITEM_INVISIBLE
    global_var.image_store.clear()
 


def dialog_color(color,set_color):
    colorbutton = gtk.ColorButton(gtk.gdk.color_parse(color))
    colorseldlg = gtk.ColorSelectionDialog(
                "Select background color")

        # Get the ColorSelection widget
    colorsel = colorseldlg.colorsel
    colorsel.set_previous_color(set_color)
    colorsel.set_current_color(set_color)
    colorsel.set_has_palette(True)

    # Connect to the "color_changed" signal
    #colorsel.connect("color_changed", color_changed_cb,colorsel)
    # Show the dialog
    response = colorseldlg.run()
    if response -- gtk.RESPONSE_OK:
        color1 = colorsel.get_current_color()
        get_color = color1.to_string()
        get_color = '#'+get_color[1:3]+get_color[5:7]+get_color[9:11]
        colorseldlg.destroy()
    
    return get_color




'''def color_event(widget , event):
    
    if event.type == gtk.gdk.BUTTON_PRESS:
        handled = True
        #print 'current color select'
        color = widget.get_colormap()
        color_visual = color.get_visual()
        print color_visual(gtk.gdk.VISUAL_TRUE_COLOR)
        style = widget.get_style()
        gc = style.bg_gc[gtk.STATE_NORMAL]
        gc.background
        print gc.background.red# , gc.foreground.blue ,gc.foreground.green

        #color = widget.get_foreground()
        #color = widget.get_current_color()
        #print color.query_color(5000)
        color_str = str(color)
        newColor = '#'+color_str[30:38]
        #canvas = item.get_canvas ()
        #name = item.get_data("name")
        #if name == global_var.itemSelectActiveName :
        #    item.props.fill_color = color
        #color2 = gtk.gdk.GC.set_rgb_bg_color(color)
        #fill_color = rgbaToInteger(color)
        #color2 = gtk.gdk.Color(0, , 0)
        #print color2.to_string()
        #readColor = color.query_color()
        #color2 = gtk.gdk.Color()
        #print readColor.to_string()
        #color2 = gtk.gdk.Color(newColor)
        #global_var.itemSelectActive.props.fill_color = color2
        print widget.get_style().fg_gc[gtk.STATE_NORMAL]
        print widget.get_style().black_gc
        #global_var.itemSelectActive.props.fill_color = widget.get_style().black_gc
        '''

        

    

    
    

    
def fill_color_in_group(selectItem,color):
    n = selectItem.get_n_children()
    if n > 0:
        for i in range(n):
            print " Children of item is ",selectItem.get_child(i)
            if selectItem.get_child(i).get_n_children() >0:
                fill_color_in_group(selectItem.get_child(i),color)
            else:
                print "fill %s color in group " % selectItem.get_child(i)
                #selectItem.get_child(i).props.fill_color = color
                fill_color_item(selectItem.get_child(i),color)
    else:
        fill_color_item(selectItem,color)
        
    #TODO : Fill color and rgba color
def fill_color_item(selectItem,color):
    selectItem.props.fill_color = color
    myData = selectItem.get_data ('itemProp')
    
    if myData.has_key('fill_mode'):
        if myData['fill_mode'] == 'None':
           pass
            
        if myData['fill_mode'] == 'Solid':
            myData['color'] = color
            myData['rgbaColor'] = None
            
        if myData['fill_mode'] == 'RGBA':
            
            if myData.has_key('rgbaColor') == False:
                myData['rgbaColor'] = 16777471
            #else:
                #if  myData['rgbaColor'] == None :
                 #   myData['rgbaColor'] = 16777471
            
            org_color = myData['color'] 
            org_color = org_color.replace('#','')
            
            org_rgba = myData['rgbaColor'] 
            
            cval = org_rgba - int(org_color,16)*256
            
            color2 = color.replace('#','')
            #color = hex(hex_alpha+color)
            color_rgba = int(color2,16)*256 + int(cval)
            #print hex(color)
            global_var.itemSelectActive2.props.fill_color_rgba = color_rgba#0x3cb37180#0x7fff9c00
            myData['rgbaColor']= color_rgba
            myData['color'] = color

    selectItem.set_data ('itemProp',myData)

def getItem_inGroup(group_item,list_item):#,ingroup):
    cnt_item = group_item.get_n_children()
    
    for i in range(cnt_item):
        v= []
        v.append(saveItemProp(group_item.get_child(i)))
        list_item.append(v)
        print "+----found item ",group_item.get_child(i)
        #ingroup2 = []
        getItem_inGroup(group_item.get_child(i),v)
        
    return True
        
    #print "pass"
def get_item_property(item):
    #print 'select item property'
    selectId = itemPropertySelect(item)



def image_to_pixbuf(image,format):
    fd = StringIO.StringIO()
    image.save(fd, format)
    contents = fd.getvalue()
    fd.close()
    loader = gtk.gdk.PixbufLoader()
    loader.write(contents, len(contents))
    pixbuf = loader.get_pixbuf()
    loader.close()
    return pixbuf

def on_arrow_down_clicked(button,palette,canvas):
    global value_palette,buttonUp,buttonDown
    global_var.win.window.set_cursor(gtk.gdk.pointer_ungrab()) 
    value_palette = value_palette+ 1
    buttonUp.set_sensitive(True)
    max_plate = 14 # Maximun color box on color palette
    if value_palette == max_plate :
        buttonDown.set_sensitive(False)
    if value_palette >max_plate :
        value_palette = max_plate
        return 0
    print 'button arrow down click! and reset grab' + str(value_palette)
    set_new_color_palette(palette,value_palette)

def on_arrow_up_clicked(button,palette,canvas):
    #canvas.window.set_cursor(gtk.gdk.pointer_ungrab()) 
    #palette = item.get_canvas ()
    global value_palette,buttonUp,buttonDown
    value_palette = value_palette- 1
    buttonDown.set_sensitive(True)
    if value_palette == 0 :
        buttonUp.set_sensitive(False)
    if value_palette <0 :
        value_palette = 0
        buttonUp.set_sensitive(False)
        return 0
    
    print 'button arrow up click!' + str(value_palette)
    set_new_color_palette(palette,value_palette)
    
    #print len(overlaped_items)

def on_button_press_canvas(canvas, event,scrolled_win):
        #self.graph.dehighlight()
    global x1
    global y1
    
    x1 = event.x
    y1 = event.y
    #print 'mouse start = [' + str(pressx) +' ,' +str(pressy)+']'
    width =40
    height = 10
    color = 'red'
    #print 'Button select press 1 and cmd draw mode %s and pan %s ' % (global_var.cmd_draw,global_var.pan_select)
    scale = canvas.get_scale()
    if len(global_var.multiSelect)==0:
        canvas.window.set_cursor(gtk.gdk.pointer_ungrab())
        
    #if global_var.item_adj is not None and global_var.adj_box_press:
    if global_var.mode_run == False:
        if global_var.adj_box_press:
            global_var.button_press = False
            print "press item on canvas"
        else:
            global_var.button_press = True

        print 'Global button press = %s .................' % global_var.button_press
        print 'item press = %s' % global_var.item_press
        global_var.drag_action = False
        
        
   # else:
        # press item when run  (pick)
        #item_pick_on_run()
    
    
    return False

def on_button_release_canvas(canvas, event,scrolled_win):
    global x1
    global y1
    global item_select,statusbar1
    global boxcolor
    
    x2 = event.x
    y2 = event.y
    width = x2-x1
    height = y2-y1
    color = boxcolor
    scale = canvas.get_scale()
    #global_var.mouse_over_item_adj = False
    #canvas = item.get_canvas ()
    if global_var.adj_box_press:
        canvas_0 = global_var.item_adj.get_canvas ()
        canvas_0.pointer_ungrab(global_var.item_adj, event.time)
        #update new groupo size when resize item under group 
        global_var.adj_box_press = False
        if  global_var.edit_group_mode == True: 
            refresh_new_group_size()
    global_var.mouse_over_item_adj = False
    
    if global_var.INDEX_CURSOR !=0:
        global_var.INDEX_CURSOR =0
        
    
    #print 'width   =' + str((x2-x1) )
    #print 'height   =' + str((y2-y1) )
    def pan_enable(self,canvas):
        if global_var.pan_select== True:
            global_var.pan_select= False
        else:
            global_var.pan_select= True
            global_var.cmd_draw == 9
        #global_var.pan_select= global_var.pan_select
        #print 'select pan enable'
    global_var.button_press = False
    
    
    
    
    if event.button == 3 : # right click on canvas 
        #global_var.bt_left['Move'].set_active(True)
        print 'press mouse  button 3'
        print "len of mutiselect ", len(global_var.multiSelect)
        if global_var.itemSelectActive2 is not None:
            popup_on_right_click(global_var.itemSelectActive2,event,canvas)
        else:
            popup_None_item_active(event,canvas)
            print "popup none item"
        #global_var.bt_left['SelectionMode'].set_active(True)
        
    '''if(event.button == 3 and item_select==False):
        mCanvas = gtk.Menu()

        pan = gtk.CheckMenuItem('pan')
        if global_var.pan_select== True:
            global_var.cmd_draw == 9 # Commnad for PAN Only
            pan.set_active(True)
        else:
            pan.set_active(False)
            
        pan.connect("activate",pan_enable,canvas )
        canvasProperty = gtk.MenuItem('Property')
        #canvasProperty.connect("activate", get_item_property,item)
        #Show item
        pan.show()
        canvasProperty.show()
        #add item menu
        mCanvas.append(pan)
        mCanvas.append(canvasProperty)
        #show popup 
        mCanvas.popup(None, None, None, event.button, event.time, None)'''
    #----button canvas release
    if global_var.cmd_draw == 0 and event.button == 1: # Command select group item
        #pass
        # mouse move leave adjust cursor for bug fix on win32
        if global_var.outter == False:
            item_lock = False
            if global_var.itemSelectActive is not None:
                get_prop = global_var.itemSelectActive.get_data('itemProp')
                item_lock = get_prop['lock']
                
            if global_var.item_press == False or item_lock ==True:
                print 'button release on main canvas'
                #canvas.window.set_cursor(gtk.gdk.pointer_ungrab())
                #print "clear grab cursor on button release canvas"
                if global_var.edit_group_mode == False: 
                    if global_var.parent_active is not None:
                        global_var.parent_active = global_var.parent_active.get_parent() # reset parent active to root
                        print "set new parent is ",global_var.parent_active
                
                
                if global_var.move_adj_action == False: # if adjust size item,it isn't clear
                    #IF ITEM is not drag resize event
                    clear_all_multiSelected()
                    lenGroup = len(global_var.multiSelect)
                    
                    
                    
                    #Delete group in select area
                    if global_var.edit_item_area_dash is not None:
                        
                        if global_var.edit_item_parent == None:# or len(global_var.edit_group_array)==0:
                            global_var.edit_item_area_dash.remove()
                            global_var.edit_group_mode = False  
                            global_var.parent_active = None 
                            global_var.edit_offset_xy = None
                            
                            
                        else:
                            #TODO : Exit group on mouse click (edit mode)
                        
                            
                            
                            root_edit,parent_edit = return_parent_root(global_var.parent_active)
                            if root_edit is not None:
                                #global_var.edit_item_parent = root_edit#.get_parent()
                                #refresh_new_group_size() # Update new group size
                                print "exit group and edit mode = [",global_var.edit_item_parent#global_var.edit_group_mode
                                print "]"
                                print  "global_var.edit_group_mode =",global_var.edit_group_mode
                                global_var.edit_item_area_dash.remove()
                                
                                renew_group_size(None,global_var.edit_item_parent)# resize of group call from [group_item.py]

                                item1 = global_var.edit_item_parent # current item edit 
                                parent1 = global_var.edit_item_parent.get_parent() # get parent curretn item
                                upper_group_edit_item(item1 ,parent1,canvas)
                                global_var.edit_offset_xy = offset_parent_position(item1)
                                global_var.itemSelectActive2 = None # Clear active item for set above and below
                                global_var.parent_active = parent_edit # update new parent active there is upper parent will be active
                                
                            else:
                                global_var.edit_item_area_dash.remove()
                                global_var.edit_group_mode = False  
                                global_var.parent_active = None
                                global_var.edit_item_area_dash = None
                            #11-06-2011
                            #edit_group_item_all(global_var.parent_active,canvas)
                            
                            '''
                            
                            print "pre remove group edit ",
                            print global_var.edit_group_array
                            del global_var.edit_group_array[-1:] # remove last group from array (pop methode)
                            if len(global_var.edit_group_array)==0:
                                global_var.edit_item_area_dash.remove()
                                global_var.edit_group_mode = False  
                                global_var.parent_active = None 
                                
                            else:
                                print "after remove group edit ",
                                print global_var.edit_group_array
                                len_group = len(global_var.edit_group_array)
                                global_var.edit_item_parent = global_var.edit_group_array[len_group-1]#.get_parent()
                                print "edit item parent value = ",global_var.edit_item_parent
                                #global_var.edit_item_area_dash.remove()
                                refresh_new_group_size() # Update new group size'''
                               
                             
                            
                
                
            
                    #start new group selection
                    #print 'After clear item in main Canvas status multiselect Len = %s item cursor len %s ' % (len(global_var.multiSelect),len(global_var.itemSelect8Cursor))
                    if global_var.item_adj is not None:
                        global_var.item_adj = None
                    
                    if global_var.sel_area is not None :
                        print 'selection area....',
                        x1 = global_var.sel_area.props.x
                        y1 = global_var.sel_area.props.y
                        x2 = global_var.sel_area.props.x + global_var.sel_area.props.width
                        y2 = global_var.sel_area.props.y + global_var.sel_area.props.height
                        
                        start_point = (x1, y1)
                        end_point = (x2, y2)
                        print start_point,end_point
                        bounds = goocanvas.Bounds(*(start_point + end_point))
                        global_var.multiSelect = canvas.get_items_in_area(bounds, True, True, True)
                        #print global_var.multiSelect 
                        lenGroup = len(global_var.multiSelect)
                        print lenGroup
                        if lenGroup >0 :
                            itemRemove = global_var.multiSelect[lenGroup-1] # remove group root
                            try:
                                global_var.multiSelect.remove(itemRemove)
                            except:
                                print 'error when remove item'
                        #multi selection [1,2,3,4,5,6] ... there will be delete 1 and 6 (first item and last item
                        #real of item in selection is [2,3,4,5]
                        itemRemove = global_var.multiSelect[0] # remove group boand in owner
                        global_var.multiSelect.remove(itemRemove)
                        lenGroup = len(global_var.multiSelect)
                        #print 'item on group is %s' % lenGroup
                        '''
                        Filter the item within selection 
                        '''
                        # ---------Start to filter item in selection area -------
                        b = [x1,y1,x2,y2] # bound item 
                        q =0
                        preDelete = []
                        for v in global_var.multiSelect:
                            q +=1
                            if selectionInArea(v,b) == False:
                                preDelete.append(v)
                            get_prop = v.get_data('itemProp')
                            
                            if get_prop == 'cursor Item':
                                preDelete.append(v)
                                
                            #delete item if not root 
                            '''parent = v.get_parent()
                            parent_root = parent.get_parent()
                            if parent_root is not None or  get_prop == 'cursor Item':
                                preDelete.append(v)'''
                                
                        #------End of check item within selected area---------
                        
                        for k in preDelete:# remove item is not within selection 
                            global_var.multiSelect.remove(k) # remove item is overlap
                            
                        del preDelete # delete temp varible 
                        
                        item_inner_group = []
                        
                        for v in global_var.multiSelect:
                            parent = v.get_parent()
                            parent_root = parent.get_parent()
                            if parent_root is not None :
                                item_inner_group.append(v)
                                
                        for k in item_inner_group:# remove item is not within selection 
                            global_var.multiSelect.remove(k) # remove item is overlap

                        for v in global_var.multiSelect:
                            #get_prop = v.get_data('itemProp')
                            #print 'Item %s is  in area name is %s ' %(v,get_prop['main']) #%
                            #print 'item is lock %s and type is %s ' % (get_prop['lock'],type(get_prop['lock']))
                            parent = v.get_parent()
                            #print "parent item",parent
                            global_var.itemSelect8Cursor[v]=drawItem.roundItem(v,canvas,parent) # create around cursor 8 item
                        print "Item count [%s] " % len(global_var.multiSelect)
                        state = event.state
                        if event.button in (1,2): # left or middle button
                            if state & gtk.gdk.SHIFT_MASK:
                                print 'SHIFT PRESS SELECT'
                
                
                
                
                
                global_var.move_adj_action = False # reset action resize event
            
        else:
            # IF outter = True will be reset
            global_var.outter = False
            
        #TODO : initial to create all Item
    if global_var.cmd_draw == 1: # Command create rectangle box
        '''global_var.itemSelectActive.remove()
        global_var.itemSelectActive = None
        for itemSelect in global_var.select_cursor :
            global_var.select_cursor[itemSelect].remove()'''
        #GDK_TCROSS
        if global_var.drag_action:
            print 'Create BOX'
            prop={}
            prop['color'] = color
            prop['x'] = 0#global_var.sel_area.props.x*scale
            prop['y'] = 0#global_var.sel_area.props.y*scale
            prop['transform_x'] = global_var.sel_area.props.x*scale
            prop['transform_y'] = global_var.sel_area.props.y*scale
            prop['radius_x']  = 0
            prop['radius_y']  = 0
            prop['width'] = global_var.sel_area.props.width#*scale
            prop['height'] =  global_var.sel_area.props.height#*scale
            prop['stroke_pattern'] = None
            prop['stroke_color'] = "black"
            prop['line_width'] = 1
            prop['can_focus'] = False
            prop['name'] = 'New Item'
            prop['lock']=False
            prop['main'] = 'Rect Item'
            prop['layer'] = 'Primary'
            prop['dynamic'] = {}
            prop['fill_mode'] = 'Solid'
            prop['scale'] = 1
            prop['degree'] = 0
            print "create box and parent active is ", global_var.parent_active
            item = drawItem.createRect(canvas,prop,None)
            item.set_simple_transform(prop['transform_x']/scale,prop['transform_y']/scale,prop['scale'] ,prop['degree'])
            #if global_var.parent_active != None:
            if global_var.edit_group_mode == True:
                create_under_group(item,global_var.edit_item_parent) # check item create under group edit
            
                
           

        #global_var.bt_left['Move'].set_active(True)
        if global_var.drag_action == False:# Reset to select mode
            global_var.bt_left['SelectionMode'].set_active(True)
            
        
        
    if global_var.cmd_draw == 2: # Command createEllipse in canvas
        if global_var.drag_action:
            print 'Create BOX Eclipse'
            prop={}
            prop['color'] = color
            prop['x'] = 0#global_var.sel_area.props.x*scale
            prop['y'] = 0#global_var.sel_area.props.y*scale
            prop['transform_x'] = global_var.sel_area.props.x
            prop['transform_y'] = global_var.sel_area.props.y
            prop['radius_x'] = global_var.sel_area.props.radius_x*scale
            prop['radius_y'] = global_var.sel_area.props.radius_y*scale
            #prop['center_x'] = (global_var.sel_area.props.width*scale)/2#global_var.sel_area.props.center_x*scale
            #prop['center_y'] =  (global_var.sel_area.props.height*scale)/2#global_var.sel_area.props.center_y*scale
            prop['width'] = global_var.sel_area.props.width
            prop['height'] =  global_var.sel_area.props.height
            prop['stroke_pattern'] = None
            prop['stroke_color'] = 'black'
            prop['line_width'] = 2
            prop['can_focus'] = False
            prop['name'] = 'New Item Text'
            prop['main'] = 'Ellipse Item'
            prop['lock']=False
            prop['layer'] = 'Primary'
            prop['dynamic'] = {}
            prop['buffer']  = ''
            prop['fill_mode'] = 'Solid'
            prop['scale'] = 1
            prop['degree'] = 0
            font_size = 24
            prop['font'] = "Sans %gpx" % font_size
            item = drawItem.createEllipse(canvas,prop,None)
            cx = prop['transform_x']#-(prop['width']/2)
            cy = prop['transform_y']#-(prop['height']/2)
            item.set_simple_transform(cx,cy,prop['scale'] ,prop['degree'])
            #drawItem.createWidget(canvas,prop)
            if global_var.edit_group_mode == True:
                create_under_group(item,global_var.edit_item_parent) # check item create under group edit
            
            
            
        if global_var.drag_action == False:# Reset to select mode
            global_var.bt_left['SelectionMode'].set_active(True)
        
        #global_var.bt_left['Move'].set_active(True)
    # TODO : Create text
    if global_var.cmd_draw == 6: # Command create Text box in canvas
        if global_var.drag_action:
            print 'Create Text BOX'
            prop={}
            prop['color'] = color
            prop['x'] = 0
            prop['y'] = 0
            prop['transform_x'] = global_var.sel_area.props.x*scale
            prop['transform_y'] = global_var.sel_area.props.y*scale
            prop['width'] = global_var.sel_area.props.width
            prop['height'] =  global_var.sel_area.props.height
            prop['scale'] = 1
            prop['degree'] = 0
            prop['stroke_pattern'] = None
            prop['stroke_color'] = color
            prop['line_width'] = 4
            prop['can_focus'] = False
            prop['name'] = 'New Item Text'
            prop['lock']=False
            prop['buffer']  = 'Untitle*'
            prop['main'] = 'Text Item'
            prop['layer'] = 'Primary'
            prop['fill_mode'] = 'Solid'
            prop['dynamic'] = {}
            font_size = 24
            prop['font'] = "Sans %gpx" % font_size
            cx = prop['transform_x']#-(prop['width']/2)
            cy = prop['transform_y']#-(prop['height']/2)
            item = drawItem.createText(canvas,prop,global_var.parent_active)
            item.set_simple_transform(cx,cy,prop['scale'] ,prop['degree'])
            #print "Get get_natural_extents text is ",item.get_natural_extents()
            #drawItem.createWidget(canvas,prop)

            #global_var.bt_left['Move'].set_active(True)
            #create_focus_box(canvas, x1, y1, width, height, color,"new_create")
        else:# Reset to select mode
            global_var.bt_left['SelectionMode'].set_active(True)
    #print self.get_scale()
    if global_var.cmd_draw == 5: # Command create line
        print 'Create LINE'
        prop={}
        prop['color'] = color
        prop['x'] = x1
        prop['y'] =y1
        prop['width'] = width
        prop['height'] =  height
        prop['stroke_pattern'] = None
        prop['stroke_color'] = "green"
        prop['line_width'] = 2
        prop['lock']=False
        prop['can_focus'] = False
        prop['name'] = 'New Item'
        prop['main'] = 'Line Item'
        prop['fill_mode'] = 'Solid'
        prop['dynamic'] = {}
        drawItem.createLine(canvas,prop,global_var.parent_active)
        #global_var.bt_left['SelectionMode'].set_active(True)
        del prop
        
    if global_var.cmd_draw == 7: # Image Insert
        print 'Image Insert'
    
    '''if (width >5 and height >8):
        create_focus_box(canvas, x1, y1, width, height, color)'''
    item_select=False
    
    if global_var.sel_press == True:
        #print 'Delete selection area'
        global_var.sel_press = False
        global_var.sel_area.remove()
        global_var.sel_area = None
        
    #mouse_pos = 'X='+str(x2)+' , Y= '+str(y2)
    #statusbar1.push(1, mouse_pos)
    return False
    


def on_button_press_window(widget,event):
    print 'window press %s , %s ' % (event.x,event.y)




def on_color_release(item,target,event):
    global value_palette
    canvas_p = item.get_canvas ()
    color = item.get_data ("box_color")
    name = item.get_data ("name")
    set_color = gtk.gdk.Color(color)

    
    if value_palette >11 :
        if(event.button == 3):
            
            new_color = dialog_color(color,set_color)
            item.props.fill_color = new_color
            item.set_data("box_color",new_color)
            cntStr = int(name)
            selectBox = value_palette
            name2Load = name
            if cntStr>9:
                selectBox = selectBox+1
                name2Load = '0'+name[1]
            
            global_var.color_bar[selectBox][int(name2Load)] = new_color
            #Save color configure 
            f = open(r'configure/color_palette.cfg')
            lines=[]
            for i in range(4):
                lines.append(f.readline())
            f.close()
            saveLine = selectBox-12
            newColorValue = ''
            for j in range(7):
                if j != 6:
                    newColorValue = newColorValue+'\''+global_var.color_bar[selectBox][j] +'\','
                else:
                    newColorValue = newColorValue+'\''+global_var.color_bar[selectBox][j]
                    
            newColorValue = newColorValue+'\n'
            lines[saveLine] = newColorValue
            f = open(r'configure/color_palette.cfg', 'w')
            f.writelines(lines)
            f.close()
            #colorbutton.connect('color-set', color_set)

    lenOfSelect = len(global_var.multiSelect)
    if (lenOfSelect > 0) and (event.button == 1) :
        for selectItem in global_var.multiSelect:
            fill_color_in_group(selectItem,color)
            #undo.undoListStore(global_var.undoList,'Change Color',color,global_var.itemSelectActive,None)
        global_var.bt['Undo'].set_sensitive(True)
            
        
    if global_var.itemSelectActive2 is not None:
        itemData = global_var.itemSelectActive2.get_data('itemProp')
        item_color =  itemData["color"]
        set_color = gtk.gdk.Color(item_color)
        global_var.dialogWidget['colorColor_button'].set_color(set_color)
       

    print 'success'
        


def on_key_press(widget, event,canvas,scrolled_win,menubar):
    keyname = gtk.gdk.keyval_name(event.keyval)
    print "Key %s (%d) was pressed" % (keyname, event.keyval)
    if event.state & gtk.gdk.CONTROL_MASK:
        if keyname == 'w':
            hAdj = scrolled_win.get_hadjustment()
            vAdj = scrolled_win.get_vadjustment()
            #print 'scroll value max h = %s ,  v =  %s ' % (hAdj.get_upper(),vAdj.get_upper())
            title ='Display position \nhorzontal = ' + str(hAdj.get_upper()) + '  vertical = ' + str(vAdj.get_upper())
            bound_x0 = global_var.dispProp['cvWidth']
            bound_y0 = global_var.dispProp['cvHeight']            
            title = title + '\nBound canvas x = ' + str(bound_x0) + '  y = ' + str(bound_y0)
            
            cvsw = global_var.dispProp['cvSizeWidth']
            cvsh = global_var.dispProp['cvSizeHeight']
            title = title + '\n canvas size x = ' + str(cvsw) + '  y = ' + str(cvsh)
            
            mouse = '\nmouse over item = ' + str(global_var.mouse_over_item)
            title =  title +mouse
            
            label = gtk.Label(title)
            md = gtk.MessageDialog(None,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
            gtk.BUTTONS_CLOSE, title)
            md.run()
            md.destroy()
            
        print "Control was being held down"
    if event.state & gtk.gdk.MOD1_MASK:
        print "Alt was being held down"
    if event.state & gtk.gdk.SHIFT_MASK:
        print "Shift was being held down"
        
    key_move = False
    if keyname == 'Escape' :#and global_var.box_select is not None: # remove all selection area
        print 'escape press'
        global_var.parent_active = None
        global_var.itemSelectActive2 = None # Clear active item for set above and below
        if global_var.edit_item_area_dash is not None:
            global_var.edit_item_area_dash.remove() # remove edit frame group
        global_var.edit_group_mode = False
        lenMultiBox = len(global_var.multiBoxMoveSelect)
        #widget.unfullscreen()
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
        key_move=False
        
    # BOTH ACTIVE ON RUN OR EDIT MODE
    if keyname == 'Control_L' or  keyname == 'Control_R': # Check status Control+L press for COPY Item (Short Cut)
        global_var.key_control_press = True
    if keyname == 'Shift_L' or  keyname == 'Shift_R': # Check ctrl press state
        global_var.key_shift_press = True
        
    if keyname == 'F11' :  # Toggle full screen
        if global_var.full_screen == False:
            global_var.full_screen = True
            while gtk.events_pending():# for bug fix full sreen delay on win32
                gtk.main_iteration() # waiting to clear all gtk.event before full screen 
            print 'Fullscreen press...'
            widget.set_decorated(False)
            #widget.set_has_frame(False)
            #widget.set_border_width(0)
            widget.fullscreen()
            widget.present ()
        else:
            print 'unFullscreen press...'
            global_var.full_screen = False
            widget.unfullscreen()
            widget.set_decorated(True)#windwo
            #widget.set_has_frame(True)
    
    if keyname == 'm' and global_var.key_control_press == True : #Toggle application menu
        print 'Hide / Show main application menu'
        if global_var.main_menu_toggle == False:
            global_var.main_menu_toggle = True
            menubar.hide()
        else:
            global_var.main_menu_toggle = False
            menubar.show()
    
    if global_var.mode_run == False:
        # DISABLE ON RUN MODE
        if keyname == 'Up': # Press arrow key on keyboard UP
            for listItem in global_var.multiSelect:
                prop = listItem.get_data('itemProp')
                if prop['lock'] == False:
                    sx,sy,scale,degree = listItem.get_simple_transform()
                    listItem.set_simple_transform(sx,(sy-1),scale,degree)
                    for j in range(8):
                        global_var.itemSelect8Cursor[listItem][j].props.y -= 1
                    key_move = True
            
        if keyname == 'Down': # Press arrow key on keyboard DOWN
            for listItem in global_var.multiSelect:
                prop = listItem.get_data('itemProp')
                if prop['lock'] == False:
                    sx,sy,scale,degree = listItem.get_simple_transform()
                    listItem.set_simple_transform(sx,(sy+1),scale,degree)
                    for j in range(8):
                        global_var.itemSelect8Cursor[listItem][j].props.y += 1
                    key_move = True
            
        if keyname == 'Left': # Press arrow key on keyboard LEFT
            for listItem in global_var.multiSelect:
                prop = listItem.get_data('itemProp')
                if prop['lock'] == False:
                    sx,sy,scale,degree = listItem.get_simple_transform()
                    listItem.set_simple_transform((sx-1),sy,scale,degree)
                    for j in range(8):
                        global_var.itemSelect8Cursor[listItem][j].props.x -= 1
                    key_move = True
            
        if keyname == 'Right': # Press arrow key on keyboard RIGHT
            for listItem in global_var.multiSelect:
                prop = listItem.get_data('itemProp')
                if prop['lock'] == False:
                    sx,sy,scale,degree = listItem.get_simple_transform()
                    listItem.set_simple_transform((sx+1),sy,scale,degree)
                    for j in range(8):
                        global_var.itemSelect8Cursor[listItem][j].props.x += 1
                    key_move = True
                    
        if key_move == True:
            if global_var.mode_run == False and global_var.edit_group_mode == True :
                #call find_width_height_group in group_item.py to update new position 
                          # select dash 
                refresh_new_group_size()

        if keyname == 'Delete' : # delete all selection area
            deleteSelected()
        if keyname == 'g' and global_var.key_control_press == True : # Group item
            group_item_all(canvas)# call group_item.py
            
        if keyname == 'u' and global_var.key_control_press == True : # Ungroup item
            ungroup_item_all(canvas) # call group_item.py
            
        if keyname == 'a' and global_var.key_control_press == True : # Select all
            select_all(canvas)
            
        if keyname == 'd' and global_var.key_control_press == True : # deSelect all
            deSelectAll()
            
        if keyname == 'c' and global_var.key_control_press == True : # Copy item
            drawItem.copyItem_byKey()
            
        if keyname == 'v' and global_var.key_control_press == True : # Paste item
            drawItem.pasteItem_byKey(canvas)
            
        if keyname == 'x' and global_var.key_control_press == True : # Cut item
            drawItem.copyItem_byKey()
            deleteSelected()
            global_var.bt['Paste'].set_sensitive(True)
            
        if keyname == 'q' and global_var.key_control_press == True : # Clear all on canvas
            for j in global_var.image_store:
                print j
            delete_all(canvas)
            
        if keyname == 'o' and global_var.key_control_press == True : # Open file from key
            global_var.key_control_press = False # reset controle key
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
            
        if keyname == 's' and global_var.key_control_press == True : # Save Document to file
            saveAsFile = ToolbarTop() # call funtion from build_menu.py
            saveAsFile.pre_saveDocument(canvas) #TO save document
            
    
    return True

def deleteSelected():
    for t in global_var.multiSelect:
        for j in range(8):
            global_var.itemSelect8Cursor[t][j].remove()
                
    for v in  global_var.multiSelect: # delete item from root
        v.remove()
    lenGroup = len(global_var.multiSelect)
    #print 'old group item select %s' %  lenGroup
    if lenGroup>0:
        del global_var.multiSelect[0:(lenGroup-1)]
        
    if global_var.mode_run == False and global_var.edit_group_mode == True :
        refresh_new_group_size()

def on_key_release(widget, event,canvas,scrolled_win):
    #Reset Key Control Press
    if global_var.key_control_press:
        global_var.key_control_press = False 
    # reset key shift
    if global_var.key_shift_press:
        global_var.key_shift_press = False
        
def on_enter_notify(item, target, event):
    item.props.fill_color = "red"
    return True

def on_leave_notify(item, target, event):
    item.props.fill_color = "black"
    return True

def on_right_click(canvas,widget,event):
    print 'right click!'
    #print canvas.get_scale()
    watch = gtk.gdk.Cursor(gtk.gdk.WATCH)
    #print event.x
    #window.set_cursor(watch)
        
def open_test():
    myLoad = open('selectAll.xgd', 'r') 
    object = pickle.load(myLoad)
    for j in object[0]:
        #print j['main']
        type_item = "<type \'list\'>"
        if str(type(j)) != type_item:
            print j
        if str(type(j)) == type_item:
            print  "item in group "
            for k in j :
                if str(type(k)) != type_item:
                    print k
                if str(type(k)) == type_item:
                    for l in k :
                        #print type(l),
                        if str(type(l)) != type_item:
                            print "      +--",
                            print l
                        if str(type(l)) == type_item:
                            for m in l :
                                print "              +--",
                                print m
   
    
def openGraphicFile(fileName):
    myLoad = open(fileName, 'r') 
    object = pickle.load(myLoad)
    Itemobject = object[0]
    #global_var.image_store = object[1]
    global_var.image_use = object[2]
    #del object
    myLoad.close()

    for imgLoadNow in object[1]:
        c = StringIO.StringIO()
        c.write(object[1][imgLoadNow][0])
        c.seek(0)
        #print 'Len of loading image file = ' + str(len(c))
        im = Image.open(c)
        format = object[1][imgLoadNow][1] # returm image format
        pixbuf = None
        
        if os.name == 'nt':
            im.save('img_tmp',format)
            pixbuf = gtk.gdk.pixbuf_new_from_file ('img_tmp')
        else:    
            im.save('/tmp/img_tmp',format)
            pixbuf = gtk.gdk.pixbuf_new_from_file ('/tmp/img_tmp')

        global_var.image_store[imgLoadNow]=[pixbuf,object[1][imgLoadNow][1]] # save pixbuf,type
    return Itemobject

def palette_color (palette, x, y, width, height, color,name):
    root = palette.get_root_item ()
    item = goocanvas.Rect (parent = root,
                           x = x,
                           y = y,
                           width = width,
                           height = height,
                           #stroke_pattern = None,
                           fill_color = color,
                           stroke_color="gray",
                           line_width = 2.0,
                           can_focus = True)
                        
    item.connect ("button_release_event", on_color_release)
    item.set_data ("box_color", color)
    item.set_data ("name", name)

def rgbaToInteger(rgba):
    r, g, b, a = rgba
    return (r << 24) | (g << 16) | (b << 8) | a


def selectionInArea(item,bounds):
    x0 = bounds[0]
    y0 = bounds[1]
    x1 =  bounds[2]
    y1 = bounds[3]
    inArea = False
    '''
    x0,y0-------------------------------------x1,y0
    |              1 ------2                      |
    |              |        |                       |
    |x0,y1      3 -----4                       |
    ---------------------------------------------x1,y1
    '''
    #Step 1
    item_sx,item_sy,s_scale,degree = item.get_simple_transform()
  
    if item_sx>x0 and item_sx<x1:
        inArea = True
    else:
        return False
    
    if item_sy>y0 and item_sy<y1:
        inArea = True
    else:
        return False
    #step 2
    Item_x2 = item_sx + item.props.width
    if Item_x2 > x0 and Item_x2 <x1:
        inArea = True
    else:
        return False
    
    Item_y2 = item_sy + item.props.height
    
    if Item_y2>y0 and Item_y2<y1:
        inArea = True
    else:
        return False
    
    return True

def select_all(canvas):
    print "Select all"
    
    deSelectAll()
    #Find item on canvas
    start_point = (canvas.props.x1, canvas.props.y1)
    end_point = (canvas.props.x2, canvas.props.y2)
    bounds = goocanvas.Bounds(*(start_point + end_point))
    overlaped_items = canvas.get_items_in_area(bounds, True, True, True)
    #print start_point,end_point
    #print overlaped_items
    selectItem = []
    
    typeGrid = '<type \'goocanvas.Grid\'>'
    typeGroup = '<type \'goocanvas.Group\'>'
    overlaped_items.reverse()
    cnt = 0
    pack_item = []
    for selected in overlaped_items:
        if str(type(selected)) != typeGrid:# and str(type(save_item)) != typeGroup:
            if selected.get_parent() is not None:
                p = selected.get_parent()
                if p.get_parent() == None:
                    global_var.multiSelect.append(selected)
                    print selected
                    global_var.itemSelect8Cursor[selected]=drawItem.roundItem(selected,canvas,None)
            #print 'item save...is'
            
    return True

def deSelectAll():
    #remove all selected and reset value
    global_var.parent_active = None
    global_var.itemSelectActive2 = None # Clear active item for set above and below
    if global_var.edit_item_area_dash is not None:
        global_var.edit_item_area_dash.remove() # remove edit frame group
    global_var.edit_group_mode = False
    lenMultiBox = len(global_var.multiBoxMoveSelect)
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
        
    # end remove all selected
        
def saveItemProp(save_item):
    updata = save_item.get_data('itemProp')
    updata['x'] = save_item.props.x
    updata['y'] = save_item.props.y
    updata['width'] = save_item.props.width
    updata['height'] = save_item.props.height
    
    if updata['main'] == 'Ellipse Item':
        updata['radius_x'] = save_item.props.radius_x
        updata['radius_y'] = save_item.props.radius_y
        updata['center_x'] = save_item.props.center_x
        updata['center_y'] = save_item.props.center_y
        
    return updata

def set_new_color_palette(palette,color_index):
    start_point = (0, 0)
    end_point = (140, 40)
    bounds = goocanvas.Bounds(*(start_point + end_point))
    overlaped_items = palette.get_items_in_area(bounds, True, True, True)
    
    #load color palette from stcok
    col = global_var.color_bar
    for i in range(6,-1,-1):
        #print i
        #numIndex = str(i)
        #if len(numIndex) <2:
        #    numIndex = '0'+numIndex
        #print numIndex
        #name = overlaped_items[i].get_data("name")
        #color = overlaped_items[i].get_data("box_color")
        #print name+':'+str(color)
        new_col = col[color_index+1][6-i]
        overlaped_items[i].set_data("box_color",new_col)
        overlaped_items[i].props.fill_color = new_col
        
    for j in range(13,6,-1):
        #print j
       # numIndex = str(j)
       # if len(numIndex) <2:
        #    numIndex = '0'+numIndex
        #print numIndex
        #name = overlaped_items[i].get_data("name")
        #color = overlaped_items[i].get_data("box_color")
        #print name+':'+str(color)
        new_col =col[color_index][13-j]
        overlaped_items[j].set_data("box_color",new_col)
        overlaped_items[j].props.fill_color = new_col
    #print col[color_index]
    #print col[color_index+1]


            
        
        



def set_proc_name(newname):
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(len(newname)+1)
    buff.value = newname
    libc.prctl(15, byref(buff), 0, 0, 0)

def get_proc_name():
    from ctypes import cdll, byref, create_string_buffer
    libc = cdll.LoadLibrary('libc.so.6')
    buff = create_string_buffer(128)
    # 16 == PR_GET_NAME from <linux/prctl.h>
    libc.prctl(16, byref(buff), 0, 0, 0)
    return buff.value

def loadItemFromFile(canvas,itemLoad,parent):
    for y in itemLoad:
        if str(type(y))== '<type \'dict\'>':# found item 
            if y['main'] != 'group Item':
                drawItem.loadingDataItem(canvas,y,parent)
        if str(type(y))== '<type \'list\'>':# found item on group 
            item = drawItem.loadingDataItem(canvas,y[0],parent)
           
            loadItemFromFile(canvas,y,item)
            
def loadInitFile(Setting):
    global boxcolor
    #for init in Setting:
    #    print init
    boxcolor = Setting['box_color']
    return True

def exit_(self,window):
    print "Try to save any setting : graphic_.conf "
    file_init = open('graphic_.conf', 'wb')
    pickle.dump(global_var.graphic_default_setting, file_init)
    file_init.close()
    print '\nGood bye!'
    gtk.main_quit()

def zoom_changed (adj, canvas):
    canvas.set_scale (adj.value)
    
    
#Drag and drop area
#Use drop image url://
def motion_cb(wid, context, x, y, time):
    #l.set_text('\n'.join([str(t) for t in context.targets]))
    context.drag_status(gtk.gdk.ACTION_COPY, time)
    # Returning True which means "I accept this data".
    return True

def drop_cb(wid, context, x, y, time):
    # Some data was dropped, get the data
    wid.drag_get_data(context, context.targets[-1], time)
    return True

def got_data_cb(wid, context, x, y, data, info, time,canvas):# get url from drop mouse
    # Got data.
    print "Drag  and drop targat file  is ",
    print data.get_text()
    drawItem.ImportDropImage(data.get_text(),canvas)
    context.finish(True, False, time)

def _canvas_tooltip_cb(canvas, x, y, keyboard_mode, tooltip):
    print "tooltip query: ", x, y
    item = canvas.get_item_at(x, y, True)
    
def main ():
    
    global item_select#,statusbar1 # value of select item
    global boxcolor
    
    item_select = False
    global_var.cmd_draw = 0

    window = gtk.Window (gtk.WINDOW_TOPLEVEL)
    window.set_default_size (800, 500) # 1024,768
    window.set_icon_from_file("images/icon.png")

    window.connect ("delete_event", exit_)
    
    
    #window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
    #addAppMenu('man')
    
    #addMenu(window)
    vbox = gtk.VBox(False, 0)
    
    

        #print imgLoadNow
    #canvas = CreatGooCanvas()
    #canvas =goocanvas.Canvas.__init__(object)

    canvas = CreatGooCanvas()
    canvas.props.has_tooltip = False
    #canvas.connect("query-tooltip", _canvas_tooltip_cb)
    
    
    
    x0 = global_var.dispProp['cvSizeWidth']
    y0 = global_var.dispProp['cvSizeHeight']
    canvas.set_size_request(x0,y0) # set size canvas
    
    x0 = global_var.dispProp['cvTop']# default 0
    y0 = global_var.dispProp['cvLeft']# default 0
    x1 = global_var.dispProp['cvWidth']# default 1024
    y1 = global_var.dispProp['cvHeight']# default 768
    print 'canvas read from global varible bounds %s ,%s ,%s , %s' % (x0,y0,x1,y1)
    canvas.set_bounds (x0, y0, x1, y1)
    
    global_var.grid['grid'] =  drawItem.canvasGrid(canvas)
    if global_var.grid['show'] :
        global_var.grid['grid'].props.visibility =goocanvas.ITEM_VISIBLE
    else:
        global_var.grid['grid'].props.visibility =goocanvas.ITEM_INVISIBLE

    
    #canvas.set_root_item(object[0])
    #Create UI menu
    #uimanager = UIManager(window)
    # Create a MenuBar
    #menubar = uimanager.createMenuBar()
    #print 'Current loading item count is ' + str(len(Itemobject))
    typeGroup = '<type \'goocanvas.Group\'>'
    #for itemLoad in Itemobject:
    
    #Load Object
    
    global_var.current_doc  = 'test_opc_pyro4.xgd'
    if global_var.current_doc != None:
        Itemobject = openGraphicFile(global_var.current_doc)
        loadItemFromFile(canvas,Itemobject,global_var.parent_active)
        title = "Nepo HMI " + global_var.current_doc
        
    else:
        title = "Nepo HMI Untitle*" 
        global_var.current_doc  = "Untitle*"
        
    window.set_title(title)
    
    global_var.parent_active = None
    
    global_var.parent_active = None # reset parent active 
    
    scrolled_win = gtk.ScrolledWindow()
    # create toolbar on the TOP window
    tbTop = ToolbarTop()
    ct= tbTop.createToolbarTop(canvas,scrolled_win) # Call function from 'build_menu.py'
    # create toolbar on the LEFT SIDE window workspace
    tb = ToolbarLeft()
    Lefttb = tb.builtLeftToolbar(canvas) # Call function from 'build_menu.py'
    # create  toolbar on the BUTTOM  window workspace
    tb1 = ToolbarBottom()#create buttom toolbar
    bottomTb = tb1.createToolbarBottom() # Call function from 'build_menu.py'
    #start create menu bar
    menu = addAppMenu(canvas,scrolled_win)
    menubar = menu.create_menu(canvas,scrolled_win,ct,Lefttb,bottomTb)# send all toolbar to main appliccation menu
    #If you press RUN menu the top,left,buttom toolbar will be disapare(hide all)
    vbox.pack_start(menubar, False)
    window.connect("key_press_event", on_key_press,canvas,scrolled_win,menubar)
    window.connect("key_release_event", on_key_release,canvas,scrolled_win)
    #window.connect("button_press_event",on_button_press_window)
    
    
    vbox.pack_start(ct, False)
    
    #vbox.pack_start (menuInit.create_menu(), False, False, 0)  
    #vbox.pack_start (menuUI, False, False, 0)  
    #

    #notebook = gtk.Notebook ()

    #window.add (notebook)

    #notebook.append_page (create_canvas (gtk.UNIT_PIXEL, "pixels"), gtk.Label ("Pixels"))
    #notebook.append_page (create_canvas (gtk.UNIT_POINTS, "points"), gtk.Label ("Points"))
    #notebook.append_page (create_canvas (gtk.UNIT_INCH, "inch"), gtk.Label ("Inch"))
    #notebook.append_page (create_canvas (gtk.UNIT_MM, "millimiters"), gtk.Label ("Millimiters"))
    #vbox.pack_start (notebook, False, False, 0)  
    
    #Create new canvas
    
    
    print 'global pan select = ' ,str(global_var.pan_select)
    canvas.set_flags (gtk.CAN_FOCUS)
    canvas.connect("button-press-event", on_button_press_canvas,scrolled_win)
    canvas.connect("button-release-event", on_button_release_canvas,scrolled_win)
    #canvas.connect("motion-notify-event", on_motion_notify_canvas)
    
    '''canvas.create_shape_box(300, 250, 80, 30, "green","green")'''
    #root = canvas.get_root_item()
    #setup_canvas (canvas, "inch", "Inch")
    #create_canvas (gtk.UNIT_PIXEL, "pixels"), gtk.Label ("Pixels")
    #SelectableBoxesArea(canvas,"/home/sompoch/pro/ubuntuclub.gif")
    
    
    
    scrolled_win.add(canvas)
    #uimanager = gtk.UIManager()
    hbox0 = gtk.HBox(False, 0)
    # creat Left toolbar
    hbox0.pack_start(Lefttb,False, False, 0)
    hbox0.pack_end(scrolled_win,True, True, 0) # If ture ' will be expande full window
    
    
    vbox.pack_start (hbox0, False, False, 0)  
    window.set_focus(canvas)
    global_var.win = window
    
    if os.path.isfile('graphic_.conf'):
        file_init = open('graphic_.conf', 'r') 
        print 'Found graphic_.conf and try to load setting'
        global_var.graphic_setting = pickle.load(file_init)
        file_init.close()
    else:
        print "graphic_.conf is not exist! /n Try to loading default setting" 
        file_init = open('graphic_.conf', 'wb') 
        pickle.dump(global_var.graphic_default_setting, file_init)
        file_init.close()
        global_var.graphic_setting = global_var.graphic_default_setting # get default setting from original [global_var,py]
    
    loadInitFile(global_var.graphic_setting) # init setting from file
    
    
    #create color box
    hbox = gtk.HBox(False, 7)
    hbox.set_border_width(0)
    colorbutton = gtk.ColorButton(gtk.gdk.color_parse(boxcolor))
    colorbutton.connect('color-set', color_set_cb)
    #colorbutton.set_use_alpha(False)
    
    hbox.pack_start(colorbutton,False, False, 0)

    # Load color template configue file at "configure/color_palette.cfg"
    f = open(r'configure/color_palette.cfg')
    lines=[]
    for i in range(4):
        lines.append(f.readline())
        c = lines[i].replace('\'',"")
        c = c.replace('\n',"")
        loadColor =c.split(',')
        global_var.color_bar.append(loadColor)
    #print c[5]
    f.close() 

    color_bar = global_var.color_bar
    
    #scrbar = gtk.Scrollbar(0,10)
    #scrolled_color = gtk.VSscrollbar(scrbar)
    #v
    
    bar = gtk.ScrolledWindow ()

    vbox2 = gtk.VBox(False, 2)
    #scrolled_color.add(vbox2)
    #vscrollbar.add(vbox2)
    global_var.mypalette = hbox
    hbox.pack_start(vbox2,False, False, 0)
    
    
   
    
    
    #create color palette
    palette  = CreatPalette() #from file colorPallet.py
    palette.set_size_request(140, 40) # set size canvas
    
    for j in range(2):
        y = j*20
        col = color_bar[j]
        for i in range(7):
            name = str(j) + str(i)
            x = i*20+2
            palette_color(palette,x,y,18,18,col[i],name)
        
    vbox2.pack_start(palette, False, True, 0)
    #Creat Label under palette
    '''global colorLabel 
    colorLabel = gtk.Label()
    colorLabel.set_text('Block 1 Color = Red')
    colorLabel.set_justify(gtk.JUSTIFY_LEFT )
    vbox2.pack_start(colorLabel, False, True, 0)'''
    
    vbox.pack_start(hbox, False, True, 0)
    
    #Creat spin button to change color pallette
    global value_palette,buttonUp,buttonDown
    value_palette = 0
    vbox3 = gtk.VBox(False, 2)
    buttonUp = gtk.Button();
    arrow = gtk.Arrow(gtk.ARROW_UP, gtk.SHADOW_NONE)#;gtk.gdk.SB_UP_ARROW
    buttonUp.add(arrow)
    buttonUp.set_relief(gtk.RELIEF_NONE)
    buttonUp.set_size_request(20, 20)
    buttonUp.set_tooltip_text("Color Block UP")
    buttonUp.connect("clicked", on_arrow_up_clicked,palette,canvas)
    #button.set_label('^')
    buttonUp.show()
    buttonUp.set_sensitive(False)
    #arrow.show()
    vbox3.pack_start(buttonUp, False, True, 0)
    
    
    
    buttonDown = gtk.Button();
    arrow = gtk.Arrow(gtk.ARROW_DOWN, gtk.SHADOW_ETCHED_IN);
    buttonDown.add(arrow)
    buttonDown.set_relief(gtk.RELIEF_NONE)
    buttonDown.set_size_request(20, 20)
    buttonDown.set_tooltip_text("Color Block Down")
    buttonDown.connect("clicked", on_arrow_down_clicked,palette,canvas)
    buttonDown.show()
    #arrow.show()
    vbox3.pack_start(buttonDown, False, True, 0)
    
    hbox.pack_start(vbox3,False, True, 0)
 
    #INSERT BUTTOM TOOLBAR
    hbox.pack_start(bottomTb,False, True, 0)

    #Create Status bar
    hbox = gtk.HBox(False, 0)
    hbox.set_border_width(2)

    #global_var.statusbar1 = gtk.Statusbar()
    global_var.statusbar1.push(1, "Ready")
    hbox.pack_start(global_var.statusbar1, True, True, 20)
    global_var.statusbar1.show()
    global_var.toolBarButtom = hbox
    hbox.show()
    vbox.pack_start(hbox, False, False, 0)
    
    #statusbar.push(2, "Position")
    
    #vbox.pack_start(statusbar, False, False, 0)
    #workpath = 'nepohmi   '+os.getcwd() # get current folder path
    #window.set_title(workpath)
    
    window.add (vbox)  
    window.drag_dest_set(0, [], 0)
    window.connect('drag_motion', motion_cb)
    window.connect('drag_drop', drop_cb)
    window.connect('drag_data_received', got_data_cb,canvas)
    window.show_all()
    #Show dialog property 
    DialogPoperty(window)
    
    temp = gtk.Entry()
    #getOpcItem(None,temp)
    #change process name
    if os.name != 'nt':
        set_proc_name('nepohmi')
        print os.getpid()

        # outputs 'display process name'
        print get_proc_name()

    
if __name__ == "__main__":
    main()
    gtk.main ()
