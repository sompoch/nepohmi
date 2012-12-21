#!/usr/bin/env python

import os
import sys
import subprocess
import math
import colorsys
import time
import re
import goocanvas

import gobject
import gtk
import gtk.gdk
import gtk.keysyms
import cairo
import pango
import pangocairo
from drawShape import *

import global_var,drawItem
#from group_item import offset_parent_position

try:
    import psyco
except:
    pass
else:
    psyco.full()


class CreatGooCanvas(goocanvas.Canvas):
    """PyGTK widget that draws dot graphs."""

    filter = 'dot'
    #pan_select = False
    def __init__(self):
        goocanvas.Canvas.__init__(self)
        
        #print pan_select
        #shape = Shape()
        #node = Node(1,20,20,200,200,shape,(20,30))#node = Node(id, x, y, w, h, shapes, url)
       #edge = Edge()
        #self.graph = Graph(20,20,shape,node,edge)
        #root = self.get_root_item()
        #self.graph.draw(self)
        #self.pen = Pen()
        #self.shape = Shape()
        
        self.openfilename = None

        self.set_flags(gtk.CAN_FOCUS)

        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
        self.connect("button-press-event", self.on_button_press)
        self.connect("button-release-event", self.on_button_release)
        self.connect("motion-notify-event", self.on_motion_notify)
        self.connect("scroll-event", self.on_scroll)
        self.connect ("key_press_event", self.on_key_press)

        self.connect("set-scroll-adjustments", self.on_set_scroll_adjustments)
        self.hadjustment = None
        self.vadjustment = None
        
        self.status_button = None
       
        self.props.anchor = gtk.ANCHOR_CENTER
       
        self.connect("size-allocate", self.on_size_allocate)
       
        self.zoom_to_fit_on_resize = False
        self.animation = NoAnimation(self)
        self.drag_action = NullAction(self)
        self.presstime = None
        #print self.graph.get_size()
        
    def on_key_press(self,target,event):
        print 'key press canvas'
        if event.keyval == 65307:
            
            for itemSelect in global_var.select_cursor :
                global_var.select_cursor[itemSelect].remove()
            
            lenGroup = len(global_var.itemSelect8Cursor)
            if lenGroup>0:
                for itemSelect in global_var.itemSelect8Cursor:
                    listItem = global_var.itemSelect8Cursor[itemSelect]
                    for j in listItem:
                        j.remove()

    def on_set_scroll_adjustments(self, canvas, hadjustment, vadjustment):
        self.hadjustment = hadjustment
        self.vadjustment = vadjustment

    def set_filter(self, filter):
        self.filter = filter

    def set_dotcode(self, dotcode, filename='<stdin>'):
        if isinstance(dotcode, unicode):
            dotcode = dotcode.encode('utf8')
        p = subprocess.Popen(
            [self.filter, '-Txdot'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
            universal_newlines=True
        )
        xdotcode, error = p.communicate(dotcode)
        if p.returncode != 0:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                                       message_format=error,
                                       buttons=gtk.BUTTONS_OK)
            dialog.set_title('Dot Viewer')
            dialog.run()
            dialog.destroy()
            return False
        try:
            self.set_xdotcode(xdotcode)
        except ParseError, ex:
            dialog = gtk.MessageDialog(type=gtk.MESSAGE_ERROR,
                                       message_format=str(ex),
                                       buttons=gtk.BUTTONS_OK)
            dialog.set_title('Dot Viewer')
            dialog.run()
            dialog.destroy()
            return False
        else:
            self.openfilename = filename
            return True

    def set_xdotcode(self, xdotcode):
        #print xdotcode
        parser = XDotParser(xdotcode)
        self.graph = parser.parse()

        #draw
        self.draw()
       
   
    def draw(self):
        self.graph.draw(self)
        return False
    
    def get_scroll(self):
        bounds = self.get_bounds()
        lt_u = (
            self.hadjustment.value / self.get_scale() + bounds[0],
            self.vadjustment.value / self.get_scale() + bounds[1]
        )
        return lt_u

    def zoom_image(self, zoom_ratio, center=False, pos=None):
        self.request_update()
        if pos is not None:
            mouse_u = self.convert_from_pixels(*pos)
            lt_u = self.get_scroll()
            zoom_diff = zoom_ratio / self.get_scale()
            new_coords = (
                mouse_u[0] - (mouse_u[0] - lt_u[0]) / zoom_diff,
                mouse_u[1] - (mouse_u[1] - lt_u[1]) / zoom_diff
            )

        #anti flick
        #self.hide()
       
        self.set_scale(zoom_ratio)
        self.zoom_to_fit_on_resize = False
        if pos is not None:
            self.scroll_to(*new_coords)
           
        #anti flick
        #self.show()

    def zoom_to_fit(self):
        rect = self.get_allocation()
        bounds = self.get_bounds()
        zoom_ratio = min(
            float(rect.width)/float(bounds[2] - bounds[0]),
            float(rect.height)/float(bounds[3] - bounds[1])
        )
        self.set_scale(zoom_ratio)
        self.zoom_to_fit_on_resize = True

    ZOOM_INCREMENT = 1.10#1.25
    ZOOM_TO_FIT_MARGIN = 12

    def on_zoom_in(self, action):
        
        self.set_scale(self.get_scale() * self.ZOOM_INCREMENT)

    def on_zoom_out(self, action):
        self.set_scale(self.get_scale() / self.ZOOM_INCREMENT)

    def on_zoom_fit(self, action):
        self.zoom_to_fit()

    def on_zoom_100(self, action):
        self.set_scale(1.0)
       
    def on_scroll(self, area, event):
        if event.direction == gtk.gdk.SCROLL_UP:
            self.zoom_image(self.get_scale() * self.ZOOM_INCREMENT,
                            pos=(event.x, event.y))
            
            zmIn= self.get_scale()
            model = global_var.comboboxZoom.get_model()
            current_scale = zmIn*100
            model[0][0]= str(int(current_scale))+'%'
            global_var.comboboxZoom.set_active(0)
            self.auto_cursor_scale(zmIn)
            return True
        if event.direction == gtk.gdk.SCROLL_DOWN:
            self.zoom_image(self.get_scale() / self.ZOOM_INCREMENT,
                            pos=(event.x, event.y))
            zmOut= self.get_scale()
            model = global_var.comboboxZoom.get_model()
            current_scale = zmOut*100
            model[0][0]= str(int(current_scale))+'%'
            global_var.comboboxZoom.set_active(0)
            self.auto_cursor_scale(zmOut)
            return True
        return False
    
    def auto_cursor_scale(self,current_Scale):
        global_var.canvas_scale = current_Scale
        for select in global_var.itemSelect8Cursor:
            print "select item for adjust zoom cursor scale as  ",current_Scale
            drawItem.update_new_round_item(select,current_Scale)
            #for i in range(8):
                #'''global_var.itemSelect8Cursor[select][i].props.x = new_x[i]
                #global_var.itemSelect8Cursor[select][i].props.y= new_y[i]'''
                #global_var.itemSelect8Cursor[select][i].props.width =7*current_Scale
                #global_var.itemSelect8Cursor[select][i].props.height =7*current_Scale
   
    def get_drag_action(self, event):

        state = event.state
        if event.button in (1, 2): # left or middle button
            '''if state & gtk.gdk.CONTROL_MASK:
                return ZoomAction
            elif state & gtk.gdk.SHIFT_MASK:
                return ZoomAreaAction
            else:'''
            if global_var.pan_select == True:
                return PanAction
            else:
                pass
                #print 'key command action = ',global_var.cmd_draw
                    #if global_var.cmd_draw == 1:
                    #    print 'Draw recy=tangle'
                                  
                    
        return NullAction

    def on_button_press(self, widget, event):
        #self.graph.dehighlight()
        #if global_var.outter != True:
        self.animation.stop()
        self.drag_action.abort()
        action_type = self.get_drag_action(event)
        self.drag_action = action_type(self)
        self.drag_action.on_button_press(event)
        self.presstime = time.time()
        self.pressx = event.x
        self.pressy = event.y
        print "666"
        self.status_button = event.button
        #else:
            #global_var.outter = False
            #print "print outter cursor ",global_var.outter
        #print self.pressx ,self.pressy
        
        #print self.get_scale()
        return False

    def is_click(self, event, click_fuzz=4, click_timeout=1.0):
        assert event.type == gtk.gdk.BUTTON_RELEASE
        if self.presstime is None:
            # got a button release without seeing the press?
            return False
        # XXX instead of doing this complicated logic, shouldn't we listen
        # for gtk's clicked event instead?
        deltax = self.pressx - event.x
        deltay = self.pressy - event.y
        return (time.time() < self.presstime + click_timeout
                and math.hypot(deltax, deltay) < click_fuzz)

    def on_button_release(self, area, event):
        self.drag_action.on_button_release(event)
        self.drag_action = NullAction(self)
        
       
        
        return False
    
    def drawBoxItem(self, area, event):
        x1 = event.x
        y1 = event.y
        #print 'mouse start = [' + str(pressx) +' ,' +str(pressy)+']'
        width =40
        height = 10
        color = 'red'
        #print 'Button select press 1 and cmd draw mode %s and pan %s ' % (global_var.cmd_draw,global_var.pan_select)
        scale = self.get_scale()
        #global_var.button_press = True
        #print 'Global button press = %s ' % global_var.button_press
        #print 'item press = %s' % global_var.item_press
        if self.status_button == 1 and  global_var.mouse_over_item == False:
            if event.type != gtk.gdk._2BUTTON_PRESS and event.type != gtk.gdk._3BUTTON_PRESS:
                if global_var.cmd_draw == 0 :
                    if global_var.sel_press == False :
                        global_var.sel_press = True
                        property = {}
                        property['x'],property['y'] = self.offset_move_box(x1,y1) # call offset position of selection  
                        drawItem.selectArea(self,property)
                    
        if self.status_button == 1 and  global_var.mouse_over_item == True:
            if event.type != gtk.gdk._2BUTTON_PRESS and event.type != gtk.gdk._3BUTTON_PRESS:
                if global_var.itemSelectActive is not None:
                    print global_var.itemSelectActive
                    itemData = global_var.itemSelectActive.get_data ("itemProp")
                    print itemData['lock']
                    if itemData['lock'] : # if lock == True
                        if global_var.cmd_draw == 0 :
                            if global_var.sel_press == False:
                                global_var.sel_press = True
                                property = {}
                                property['x'],property['y'] = self.offset_move_box(x1,y1) # call offset position of selection  
                                drawItem.selectArea(self,property)
                        
                    
        
        if global_var.cmd_draw == 1  or global_var.cmd_draw == 6 : # draw rectangle or create text
            
            if global_var.sel_press == False:
                global_var.sel_press = True
                property = {}
                print '555'
                property['x'],property['y'] = self.offset_move_box(x1,y1) # call offset position of selection  
                drawItem.selectArea(self,property)
        

        if global_var.cmd_draw == 2:
            
            if global_var.sel_press == False:
                global_var.sel_press = True
                property = {}
                property['x'],property['y'] = self.offset_move_box(x1,y1) # call offset position of selection 
                property['radius_x'] = width/2
                property['radius_y'] =height/2
                property['center_x'] = x1-width/2
                property['center_y'] =  y1-height/2 
                property['width'] = width
                property['height'] =height
                #global_var.parent_active
                drawItem.selectEllipseArea(self,property,None)
            
        #print 'Drag diff pos x %s , y %s' % ((event.x-self.pressx),(event.y-self.pressy))
            
        return True

    def on_motion_notify(self, area, event):
        self.drag_action.on_motion_notify(event)
        
        pos =  'motion x,y =  ' + str(event.x) + ',' + str(event.y)
        
        global_var.statusbar1.push(1, pos)
        global_var.mov_x = event.x
        global_var.mov_y = event.y
        global_var.mouse_over_item = False
        #global_var.mouse_over_item_adj = False
        #print 'global button press = %s and mouse over adj = %s' % (global_var.button_press,global_var.mouse_over_item_adj)
        
        if global_var.adj_box_press == False:
        
            if global_var.button_press == True :
                if global_var.item_press == False: # Select out side item 
                    if global_var.cmd_draw == 0:
                        self.drawBoxItem(area, event)
                        pass
                if global_var.item_press == True:
                    if global_var.itemSelectActive is not None:
                        myData = global_var.itemSelectActive.get_data ('itemProp')
                        if myData['lock'] == True:
                            self.drawBoxItem(area, event)
                            pass
                global_var.drag_action = True
     
            if global_var.cmd_draw == 1 and global_var.button_press == True:# Draw item
                self.drawBoxItem(area, event)
                global_var.drag_action = True
                
            if global_var.cmd_draw == 2 and global_var.button_press == True:# Draw item
                self.drawBoxItem(area, event)
                global_var.drag_action = True
            #Create text box area
            if global_var.cmd_draw == 6 and global_var.button_press == True:# Text
                self.drawBoxItem(area, event)
                global_var.drag_action = True
            #continuous 7-12-2010 

        if global_var.adj_box_press == True and global_var.outter == False :
             # and global_var.mouse_over_item_adj == True:
            #print 'drag adj begin...%s , %s ' % (global_var.itemSelectActive.props.x,global_var.itemSelectActive.props.y)
            self.adj_item_size(event)
            global_var.move_adj_action = True
            print "to resize item"
            
            
        
            
        '''if global_var.adj_box_press == False and global_var.INDEX_CURSOR !=0 :
            global_var.INDEX_CURSOR =0
            print 'adj_and mouse over item adj ....%s ' % global_var.mouse_over_item_adj
            #print 'Change to default mouse pointer and index cursor = %s' % global_var.INDEX_CURSOR
            if global_var.select_cursor_move is not None:
                self.pointer_ungrab(global_var.select_cursor_move, event.time)
        '''    
        #print 'sel press %s and sel item %s ' %(global_var.sel_press,global_var.sel_item )
        if global_var.sel_press == True and global_var.sel_item == False:
            read_scale = self.get_scale()

            end_x = event.x
            end_y = event.y
            
            new_x = self.pressx
            new_y = self.pressy
            
            w = end_x - self.pressx
            h = end_y - self.pressy
           
            
            if w>0 and h>0:
                #w =  event.x - self.pressx
                #h =  event.y - self.pressy
                global_var.sel_area.props.width = w/read_scale
                global_var.sel_area.props.height = h/read_scale
                
            if w<0 and h>0:
                #move cursor  right --> left 
                offset_x,offset_y = self.offset_selection(event.x,event.y)
                global_var.sel_area.props.x = offset_x/read_scale
                #global_var.sel_area.props.y = end_y/read_scale#
                w = new_x-end_x
                global_var.sel_area.props.width = w/read_scale
                global_var.sel_area.props.height = h/read_scale
                
            if w>0 and h<0:
               # global_var.sel_area.props.x = end_x/read_scale#
                #end_x,end_y = self.offset_selection(event.x,event.y)
                offset_x,offset_y = self.offset_selection(event.x,event.y)
                global_var.sel_area.props.y = offset_y/read_scale
                h = new_y-end_y
                global_var.sel_area.props.width = w/read_scale
                global_var.sel_area.props.height = h/read_scale
                
            if w<0 and h<0:
                w = new_x-end_x
                h = new_y-end_y
                offset_x,offset_y = self.offset_selection(event.x,event.y)
                global_var.sel_area.props.x = offset_x/read_scale
                global_var.sel_area.props.y = offset_y/read_scale
                
                global_var.sel_area.props.width = w/read_scale
                global_var.sel_area.props.height = h/read_scale

            #print 'Refresh area selection'
        return False
    
    def adj_item_size(self,event):
        
        read_scale = self.get_scale()
        prop_adj = global_var.item_adj.get_data ("itemProp")
        adj_name = global_var.item_adj.get_data ("name") # read name position adj (1-8)..int
        select_item = prop_adj['itemParent']
        select_group = select_item.get_parent()
        if select_group is not None:
            x0 = select_item.props.x + select_group.props.x#global_var.itemSelectActive.props.x
            y0 = select_item.props.y + select_group.props.y#global_var.itemSelectActive.props.y
            w0 = select_item.props.x + select_item.props.width
            h0 = select_item.props.y + select_item.props.height
            
            #print "event offset x = %s, y = %s and off_x = %s, off_y = %s " % (of_x,of_y,new_off_x,new_off_y)
            #new_off_x += select_group.props.x
            #new_off_y += select_group.props.y
            
        else:
            #print "item ingrop resize 777"
            x0 = select_item.props.x 
            y0 = select_item.props.y 
            w0 = select_item.props.x + select_item.props.width
            h0 = select_item.props.y + select_item.props.height
            
            #new_off_x,new_off_y = self.offset_selection(event.x,event.y)
            
        #update new position of adjustment cursor under group or root of canvas
        global_var.item_adj.props.x,global_var.item_adj.props.y  = self.offset_resize_in_group(adj_name,select_group,read_scale,event)
        #print "pos x %s , pos y %s " % (global_var.item_adj.props.x,global_var.item_adj.props.y)
        #When edit mode is True
        
        
        if global_var.edit_group_mode == True:
            x0,y0 = global_var.edit_offset_xy
            #print "offset x0 %s , y0 %s " % (x0,y0)
            x0 += (select_item.props.x) #Offset for real item event position (x)
            y0 += (select_item.props.y) #Offset for real item event position (y)
           
            
        if adj_name == '8':

            width_new = (global_var.item_adj.props.x-x0)-3
            height_new = (global_var.item_adj.props.y-y0)-3
            if width_new<0:
                width_new =1
            if height_new<0:
                height_new=1
            select_item.props.width = width_new#/read_scale
            select_item.props.height = height_new#/read_scale
            
            
        if adj_name == '5':
            
            width_new = (global_var.item_adj.props.x-x0)-3
            if width_new<0:
                width_new =1
            select_item.props.width = width_new#/read_scale
            
        if adj_name == '7':
            height_new = (global_var.item_adj.props.y-y0)-3
            if height_new<0:
                height_new =1
            select_item.props.height = height_new#/read_scale
            
        if adj_name == '2':
            height_new = h0-global_var.item_adj.props.y
            if height_new<0:
                height_new =1
            select_item.props.height = height_new#/read_scale
            select_item.props.y = global_var.item_adj.props.y# - 3
            
        if adj_name == '4':
            #if read_scale == 2:
                #global_var.item_adj.props.x =global_var.item_adj.props.x*read_scale# 100
                #y0 += 100
                #print "by manual offset x0 %s , y0 %s " % (x0,y0)
            width_new = w0-(global_var.item_adj.props.x)#*read_scale)
            if width_new<0:
                width_new =1
            select_item.props.width = width_new#/read_scale
            select_item.props.x = (global_var.item_adj.props.x)#read_scale)# - 3
            
        if adj_name == '1':
            height_new = h0-global_var.item_adj.props.y
            width_new = w0-global_var.item_adj.props.x
            if height_new<0:
                height_new =1
            if width_new<0:
                width_new =1
                
            select_item.props.x = global_var.item_adj.props.x#+3
            select_item.props.y = global_var.item_adj.props.y#+3
            select_item.props.width = width_new#/read_scale
            select_item.props.height = height_new#/read_scale
            
        if adj_name == '3':

            #w0 = select_item.props.x + select_item.props.width
            #h0 = select_item.props.y+ select_item.props.height
            offset_y0 =0
            if select_group is not None:
                offset_y0 = select_group.props.y
                h0 = select_item.props.y+ select_item.props.height
                height_new = h0-(global_var.item_adj.props.y)
                #print "pos adj.y " ,global_var.item_adj.props.y
                width_new = (global_var.item_adj.props.x)-x0 #select_group.props.x
                
            else:
                
                height_new = h0-global_var.item_adj.props.y
                width_new = (global_var.item_adj.props.x-x0)
                
            if height_new<0:
                height_new =1
            select_item.props.height = height_new
            #select_item.props.height += offset_y0
            c = global_var.item_adj.props.y# - offset_y0
            select_item.props.y = c
            
            
            if width_new<0:
                width_new =1
            select_item.props.width = width_new#/read_scale
                
        if adj_name == '6':
            width_new = w0-global_var.item_adj.props.x
            if width_new<0:
                width_new =1
            select_item.props.width = width_new#/read_scale
            select_item.props.x = global_var.item_adj.props.x# - 3
            
            height_new = (global_var.item_adj.props.y-y0)
            if height_new<0:
                height_new =1
            select_item.props.height = height_new#/read_scale
            
            
            
        drawItem.update_new_round_item(select_item,read_scale)
        
        return True
    
    def offset_resize_in_group(self,select_id,select_group,read_scale,event):
        #********************************************************
        #-----------------Function description-------------------
        #********************************************************
        
        #select_id = the position of resize cursor 1-----2------3
        #                                          4            5
        #                                          6-----7------8
        #select_group  = the item is selected by mouse click that it's mean item is active.
        #read_scale = report current scale on canvas that user click on zoom button 
        #event      = to get the mouse position over canvas 
        
        
        of_x = event.x#-select_group.props.x
        of_y = event.y#-select_group.props.y
        
        #except 5,7,8
        if select_group is not None:
            if global_var.edit_group_mode: # on group edit mode has active (True)
                x0,y0 = global_var.edit_offset_xy#self.offset_item_position_resize(select_group)
                #if read_scale == 2:
                #x0 = x0*read_scale
                #y0 = y0*read_scale
                #x0 = x0-select_group.props.x
                #y0 = y0-select_group.props.y
                #x0 = select_group.props.x 
                #y0 = select_group.props.y 
            else:
                x0 = select_group.props.x 
                y0 = select_group.props.y
                
            
            if select_id in ['4','1','6']:
                of_x = (event.x/read_scale)-x0#select_group.props.x
               
                #of_x = of_x*read_scale
            if select_id in ['2','3','1']:
                of_y = (event.y/read_scale)-y0
                
            #print "Event.x = %s x0 = %s  diff = %s " % (event.x,x0,of_x)
        #if read_scale == 1:
        new_off_x,new_off_y = self.offset_selection(of_x,of_y)
        #else:
            #new_off_x = of_x
            #new_off_y = of_y
        if  select_id in ['1','2','4']:
            pos_x = (new_off_x-3)
            pos_y = (new_off_y-3)
        if  select_id in ['5','7','8']:
            pos_x = (new_off_x-3)/read_scale
            pos_y = (new_off_y-3)/read_scale
        if select_id in ['3']:
            pos_x = (new_off_x-3)/read_scale
            pos_y = (new_off_y-3)
        if select_id in ['6']:
            pos_x = (new_off_x-3)
            pos_y = (new_off_y-3)/read_scale
       
        return pos_x,pos_y
    
    def offset_item_position_resize(self,item_edit):
        x0 = 0
        y0 = 0
        while item_edit.get_parent() is not None:
            x0 += item_edit.props.x
            y0 += item_edit.props.y
            item_edit = item_edit.get_parent()
        return x0,y0
        
    def offset_move_box(self,x1,y1):
        scale = self.get_scale()
        #self.hadjustment.get_hadjustment()
        #hAdj = self.hadjustment.get_hadjustment()
        #vAdj = self.vadjustment.get_vadjustment()
        hValue = self.hadjustment.get_upper()
        wValue = self.vadjustment.get_upper()
        
        bound_x0 = global_var.dispProp['cvWidth']
        bound_y0 = global_var.dispProp['cvHeight']
        cavSizeW = global_var.dispProp['cvSizeWidth']
        cavSizeH = global_var.dispProp['cvSizeHeight']

        
        if (hValue < (cavSizeH+5)) or (wValue < (1000)) :#bound_x0
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
    
    def offset_selection(self,x1,y1):
        scale = self.get_scale()
        #self.hadjustment.get_hadjustment()
        #hAdj = self.hadjustment.get_hadjustment()
        #vAdj = self.vadjustment.get_vadjustment()
        hValue = self.hadjustment.get_upper()
        wValue = self.vadjustment.get_upper()

        bound_x0 = global_var.dispProp['cvWidth']
        bound_y0 = global_var.dispProp['cvHeight']
        cavSizeW = global_var.dispProp['cvSizeWidth']
        cavSizeH = global_var.dispProp['cvSizeHeight']
        
        if (hValue< (cavSizeH+5)) or (wValue < (1000)) :#bound_x0
            bound_x0 = global_var.dispProp['cvWidth']
            bound_y0 = global_var.dispProp['cvHeight']
            cavSizeW = global_var.dispProp['cvSizeWidth']
            cavSizeH = global_var.dispProp['cvSizeHeight']
            offset_x0 = (hValue-(bound_x0*scale))/2
            offset_y0 = (wValue-(bound_y0*scale))/2
            #print 'offset x, y = %s , %s ' % (offset_x0,offset_y0)
            new_x = (x1-offset_x0)
            new_y = (y1-offset_y0)
        else:
            new_x = x1#/scale
            new_y = y1#/scale# -  (y1/scale)/2
 
        return new_x,new_y

    def on_size_allocate(self, area, allocation):
        if self.zoom_to_fit_on_resize:
            self.zoom_to_fit()
           
    def animate_to(self, x, y):
        self.animation = ZoomToAnimation(self, x, y)
        self.animation.start()  
        
    #create shape area
    '''def create_shape_box (self, x, y, width, height, color,name):
        root = self.get_root_item ()
        item = goocanvas.Rect (parent = root,
                               x = x,
                               y = y,
                               width = width,
                               height = height,
                               stroke_pattern = None,
                               fill_color = color,
                               line_width = 4.0,
                               can_focus = True)
                            
        self.set_data(name, item)
        item.set_data ("id", color)
        item.set_data ("width", width)
        item.set_data ("height", height)
        
        #item.connect("motion_notify_event", self.on_motion_shape)
        item.connect ("button_press_event", self.on_button_press)
        
    def on_motion_shape (self,item, target, event):
        print 'motion'
        id = item.get_data ("id")
        
        if id:
            print "%s item received 'motion-notify' signal" % id
        else:
            print "Unknown item received 'motion-notify' signal"

        return True
    
    def on_button_press (item, target, event):
        id = item.get_data ("id")
        #print 'button press'
        return True'''
        
class DragAction(object):

    def __init__(self, dot_widget):
        self.dot_widget = dot_widget

    def on_button_press(self, event):
        self.startmousex = self.prevmousex = event.x_root
        self.startmousey = self.prevmousey = event.y_root
        self.start()

    def on_motion_notify(self, event):
        deltax = self.prevmousex - event.x_root
        deltay = self.prevmousey - event.y_root
        self.drag(deltax, deltay)
        self.prevmousex = event.x_root
        self.prevmousey = event.y_root

    def on_button_release(self, event):
        self.stopmousex = event.x_root
        self.stopmousey = event.y_root
        self.stop()

    def draw(self, cr):
        pass

    def start(self):
        pass

    def drag(self, deltax, deltay):
        pass

    def stop(self):
        pass

    def abort(self):
        pass

class NullAction(DragAction):
    
    def on_motion_notify(self, event):
        pass
        

class Animation(object):

    step = 0.03 # seconds

    def __init__(self, dot_widget):
        self.dot_widget = dot_widget
        self.timeout_id = None

    def start(self):
        self.timeout_id = gobject.timeout_add(int(self.step * 1000), self.tick)

    def stop(self):
        self.dot_widget.animation = NoAnimation(self.dot_widget)
        if self.timeout_id is not None:
            gobject.source_remove(self.timeout_id)
            self.timeout_id = None

    def tick(self):
        self.stop()

class NoAnimation(Animation):

    def start(self):
        pass

    def stop(self):
        pass
        return False

class PanAction(DragAction):

    def start(self):
        self.dot_widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.HAND2))
        self.x, self.y = self.dot_widget.get_scroll()

    def drag(self, deltax, deltay):
        self.x += deltax / self.dot_widget.get_scale()
        self.y += deltay / self.dot_widget.get_scale()
        self.dot_widget.scroll_to(self.x, self.y)

    def stop(self):
        #self.dot_widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.ARROW))
        #self.dot_widget.window.set_cursor(gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_ARROW))
        #gtk.gdk.pointer_ungrab
        self.dot_widget.window.set_cursor(gtk.gdk.pointer_ungrab())
        pass
    
    abort = stop

    