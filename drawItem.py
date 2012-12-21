#!/usr/bin/env python
import gtk
import goocanvas
import glob,os

import gobject
import gtk.gdk
import gtk.keysyms
import cairo
import array

from layer import *
import global_var
import undo
from itemProperty import *
from group_item  import return_parent_root,refresh_new_group_size
from dynamic import displayActionDynamic
from opc_service import read_from_socket
from copyAnimation import copyItemProp
import nepohmi

from popup_menu import * #call popup_menu .py on right click

def createRect(canvas,property,set_parent):
    #def create_focus_box (canvas, x, y, width, height, color,name):
    
    get_scale = canvas.get_scale()
    #pattern = create_stipple ("cadetblue")
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    
    #if property.has_key('radius_x'):
    #    pass
    #else:
        #property['radius_x'] = 0
        #property['radius_y'] = 0
    
    
    property['can_focus'] = True
    item = goocanvas.Rect (parent = root,
                           x = property['x']/get_scale,#int
                           y = property['y']/get_scale,#int
                           width = property['width'],#int
                           height = property['height'],#int
                          #fill_pattern = pattern,
                           #stroke_pattern =  property['stroke_pattern'],# boolean
                           fill_color = property['color'],# string
                           stroke_color = property['stroke_color'],# string
                           line_width = property['line_width']/get_scale,#, # int
                           radius_x = property['radius_x']/get_scale,
                           radius_y = property['radius_y']/get_scale,
                           tooltip = "Application",
                           can_focus = property['can_focus']) # Boolean
    '''if property.has_key('rgbaColor'):
        if property.has_key('rgbaColor') is not None:
            if property['rgbaColor'] is not None:
                item.props.fill_color_rgba =  property['rgbaColor']
            else:
                print 'item has rgba color == None'''
    #if property.has_key('fill_mode') == False:
    #    property['fill_mode'] = 'Solid'
    #else:
    # Setting item fill mode 
    item_fill_mode(item,property)
    
        
    #print 'Fill mode = ',property['fill_mode']
        
    canvas.set_data(property['main'], item)
    item.set_data ("itemProp", property)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    
    #item.props.has_tooltip = True
    #item.connect ("query-tooltip",set_tooltip)
    
    return item

def set_tooltip( item,x, y, keyboard_mode, tooltip):
    itemData = item.get_data ("itemProp")
    if itemData.has_key('dynamic'):
        pointDynamic = itemData['dynamic']
        if pointDynamic.has_key('Pick'):
            itemSelect = pointDynamic['Pick']
            typeItem =  str(type(itemSelect))
            #print "item select"
            #print typeItem
            if typeItem == '<class \'animation.animationPicker\'>':
                #global_var.list_item_obj.append(item_dyn) # add item on run 
                # Use tempory for test bacnet
                #print itemSelect.tag
                tooltip.set_text(itemSelect.tag)
    else:
        tooltip.set_text(None)
    #print 'item has tooltip'
    return True

def canvasGrid(canvas):
    root = canvas.get_root_item ()
    bound = canvas.get_bounds()
    pattern = create_stipple ("cadetblue")
    grid = goocanvas.Grid(parent=root,
                            x=bound[0],
                            y=bound[1],
                            width=bound[2],
                            height=bound[3],
                            fill_color = 'gray',#,
                            #x_step=20,
                            #Y_step=20,
                            #x_offset=10,
                            #y_offset=10)
                            fill_pattern = pattern,
                            horz_grid_line_width=1.0,
                            horz_grid_line_color="white",
                            vert_grid_line_width=1.0,
                            vert_grid_line_color="white")#,
                            #border_width=3.0,
                            #border_color="white")
                            #fill_color="blue")'''
                            
    print 'Create Grid on Canvas'
    prop={}
    prop['color'] = 'gray'
    prop['x'] = 0
    prop['y'] =0
    prop['width'] = 768#global_var.sel_area.props.width*scale
    prop['height'] =  1024#global_var.sel_area.props.height*scale
    prop['stroke_pattern'] = None
    prop['stroke_color'] = "black"
    prop['line_width'] = 1
    prop['can_focus'] = False
    prop['name'] = 'Grid Item'
    prop['lock'] = False
    prop['main'] = 'Grid Item'
    prop['layer'] = 'Primary'
    prop['dynamic'] = {}
    grid.set_data ("itemProp", prop)
                            
    return grid

def create_stipple (color_name):
        color = gtk.gdk.color_parse (color_name)

        stipple_data = array.array('B', [0, 0, 0, 255,   0, 0, 0, 0,
                                         0, 0, 0, 0,   0, 0, 0, 255])

        stipple_data[2] = stipple_data[14] = color.red >> 8
        stipple_data[1] = stipple_data[13] = color.green >> 8
        stipple_data[0] = stipple_data[12] = color.blue >> 8

        surface = cairo.ImageSurface.create_for_data (stipple_data,
                                                      cairo.FORMAT_ARGB32,
                                                      2, 2, 8)
        pattern = cairo.SurfacePattern(surface)
        pattern.set_extend (cairo.EXTEND_REPEAT)

        ## FIXME workaround a bug into pycairo
        ## https://bugs.freedesktop.org/show_bug.cgi?id=18947
        #global foo
        #foo.append(stipple_data)

        return pattern

def selectArea(canvas,property):
    #def create_focus_box (canvas, x, y, width, height, color,name):
    root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    print "select area create "
    parent_item = root
    #if global_var.edit_group_mode == True and global_var.parent_active != None:  
    #    parent_item = global_var.parent_active
      
    item = goocanvas.Rect (parent = parent_item,
                           x = property['x'],#int
                           y = property['y'],#int
                           width = 20/get_scale,#int
                           height = 20/get_scale,#int
                           line_dash=goocanvas.LineDash([3.0/get_scale, 3.0/get_scale]),
                           line_width = 0.8/get_scale)#, # int
    global_var.sel_area = item
    #print 'current pos %s , %s ' % (item.props.x,item.props.y)
    
def selectEllipseArea(canvas,property,set_parent): # before create Ellipse 
    
    get_scale = canvas.get_scale()
    
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    item = goocanvas.Ellipse(parent=root,
                            x = property['x'],#int
                            y = property['y'],#int
                            center_x=property['center_x']/get_scale,
                            center_y=property['center_y']/get_scale,
                            radius_x=property['radius_x']/get_scale,
                            radius_y=property['radius_y']/get_scale,
                            width = property['width'],#int
                            height = property['height'],#int
                            line_dash=goocanvas.LineDash([3.0/get_scale, 3.0/get_scale]),
                            line_width = 0.8/get_scale)#, # int
    global_var.sel_area = item
    

def createText(canvas,property,set_parent):
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    #root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    item = goocanvas.Text (parent = root,
                           text = property['buffer'],
                           x = property['x'],#int
                           y = property['y'],#int
                           width = property['width'],#int
                           height = property['height'],
                           fill_color = property['color'],
                           anchor = gtk.ANCHOR_NORTH_WEST,#gtk.ANCHOR_CENTER
                           font = property['font'])
                        
    canvas.set_data(property['name'], item)
    item.set_data ("itemProp", property)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    item.connect ("query-tooltip",set_tooltip)
    
    return item

def createWidget(canvas,property,set_parent):
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    #root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    entry = gtk.Button() #gtk.Entry()
    entry.set_size_request(40,20)
    item = goocanvas.Widget(parent = root,
                           widget = entry,
                           x = property['x']/get_scale,#int
                           y = property['y']/get_scale,#int
                           width = property['width']/get_scale,#int
                           height = property['height']/get_scale,#int
                           anchor = gtk.ANCHOR_CENTER)
                        
    canvas.set_data(property['name'], item)
    item.set_data ("itemProp", property)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    return item

def createEllipse(canvas,property,set_parent):
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent

    #root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    item = goocanvas.Ellipse(parent=root,
                            #center_x=property['center_x']/get_scale,
                            #center_y=property['center_y']/get_scale,
                            x=property['x']/get_scale,
                            y=property['y']/get_scale,
                            width = property['width'],#int
                            height = property['height'],#int
                            radius_x=property['radius_x'],
                            radius_y=property['radius_y'],
                            stroke_color=property['stroke_color'],# string
                            fill_color = property['color'],# string
                            line_width = property['line_width']/get_scale) # int)
    # Setting item fill mode 
    item_fill_mode(item,property)  

    canvas.set_data(property['name'], item)
    item.set_data ("itemProp", property)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    return item

def createGroup(canvas,property,set_parent):
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    get_scale = canvas.get_scale()
    
    group1 = goocanvas.Group(parent = root, # creat group on canvas
                            x = property['x']/get_scale,#int
                            y = property['y']/get_scale,#int
                            width = property['width']/get_scale,#int
                            height = property['height']/get_scale)
    group1.set_data ("itemProp", property)
    return group1

def createLine(canvas,property,set_parent):
    if set_parent == None:
        root = canvas.get_root_item ()
    else:
        root = set_parent
    #root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    item = goocanvas.polyline_new_line(root,(property['x']/get_scale),#int
                           (property['y']/get_scale),#int
                           ((property['width']/get_scale)+(property['x']/get_scale)),#int
                           ((property['height']/get_scale) + (property['y']/get_scale)),#int
                           line_width = property['line_width'],
                           stroke_color=property['stroke_color'])#, # int
                           #can_focus = property['can_focus']) # Boolean
                        
    
    canvas.set_data(property['main'], item)
    item.set_data ("itemProp", property)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    
    return item

def createAdjustCursor(canvas,property,name,sel_item,set_parent):
    #def create_focus_box (canvas, x, y, width, height, color,name):
    root = canvas.get_root_item()
    get_scale = canvas.get_scale()
    #parent_item = root
    #if global_var.edit_group_mode == True and global_var.parent_active != None:  
    #    parent_item = global_var.parent_active
    if set_parent == None:
        set_parent = root

    item = goocanvas.Rect (parent = set_parent,
                           x = property['x'],#/get_scale,#int
                           y = property['y'],#/get_scale,#int
                           width = 7/get_scale,#/get_scale,#int
                           height = 7/get_scale,#/get_scale,#int
                           stroke_color = 'white',
                           fill_color_rgba = property['rgbaColor'],#0x3cb37180,
                           line_width = 0 )#, # int
                        
    
    item.set_data ("itemProp", property)
    item.set_data("name",name)
    global_var.select_cursor[name] = item
    item.connect ("button_press_event", adjBox_press,canvas,sel_item)
    #item.connect ("motion_notify_event", change_cursor,canvas,name)
    item.connect ("button_release_event", adjBox_release,canvas)
    item.connect("enter_notify_event", on_enter_notify,canvas,name)
    item.connect("leave_notify_event", on_leave_notify,canvas,property['rgbaColor'])
    #print 'create adjust'
    return item
    
def startWithBG(canvas):
    # Create Initial Background 
    prop={}
    prop['color'] = 'gray'
    prop['x'] = 0
    prop['y'] = 0
    prop['width'] = global_var.dispProp['cvWidth']
    prop['height'] =  global_var.dispProp['cvHeight']
    prop['stroke_pattern'] = None
    prop['stroke_color'] = "green"
    prop['line_width'] = 0
    prop['name'] = 'Background'
    prop['main'] = 'Background Rect Item'
    prop['fill_mode'] = 'Solid'
    bg = createBackground(canvas, prop)
    
def createBackground(canvas, property):
    root = canvas.get_root_item()
    get_scale = canvas.get_scale()
    item = goocanvas.Rect (parent = root,
                           x = property['x']/get_scale,#int
                           y = property['y']/get_scale,#int
                           width = property['width'],#global_var.dispProp['cvWidth']
                           height = property['height'],#global_var.dispProp['cvHeight']
                           fill_color = property['color'])
                           
    canvas.set_data(property['name'], item)
    item.set_data ("itemProp", property)
    return item
    
    
    
#-------This funtion of copy item we can use ---
#- CTRL+C 
#- Right click on item 
#- Select from main menu
#-----------------------------------------------
def copyItem_byKey():
    print "print press copy item"
    global_var.key_control_press = False# Reset key control
    if len(global_var.multiSelect)>0:   # If item selected has in memory
        del global_var.copyBuffer[0:] # remove all data out of memory
        for item in global_var.multiSelect:
            global_var.copyBuffer.append(item)
            print item
            

def pasteItem_byKey(canvas):
    print "print past item"
    global_var.key_control_press = False # Reset key control
    tempCopy = []
    for thisItem in global_var.copyBuffer:

        if thisItem.get_n_children()>0: # Checked item under group 
            GroupCopy(thisItem,thisItem,canvas,tempCopy,'Normal')
        else:
            #COPY SINGLE PROPERTY ITEM 
            NoneGroupCopy(thisItem,thisItem,canvas,tempCopy,'Normal')
            
    if global_var.edit_group_mode == False:
        refershCursor2NewItem(canvas,tempCopy)
    else:
        refresh_new_group_size()
#TODO : Fill mode area 
def item_fill_mode(item,property):
    if property.has_key('fill_mode'):
        mode = property['fill_mode']
        if mode == 'None':
            pass
        if mode == 'Solid':
            item.props.fill_color =  property['color']
        if mode == 'RGBA':
            if property['rgbaColor'] is not None:
                item.props.fill_color_rgba =  property['rgbaColor']
            else:
                print 'item has rgba color == None'
        
    return True 

def adjBox_press(item,target, event,canvas,sel_item):
    global_var.adj_box_press = True
    print 'press adjust cursor........%s ' % global_var.adj_box_press
    global_var.item_adj = item # temp item to adjust---> createCanvas.on_motion_notify
    
    return True
    
def adjBox_release(item,target, event,canvas):
    global_var.adj_box_press = False
    print  'adj release = %s ....................' %global_var.adj_box_press
    
def on_enter_notify(item, target, event,canvas,cursor_name):
    item.props.fill_color = "red"
    print 'item change color = red'
    global_var.mouse_over_item_adj = True
    
    if cursor_name == '1':
        fleur = gtk.gdk.Cursor(gtk.gdk.TOP_LEFT_CORNER)
        global_var.INDEX_CURSOR = 1
    
    if cursor_name == '2':
        fleur = gtk.gdk.Cursor(gtk.gdk.TOP_SIDE)
        global_var.INDEX_CURSOR = 2
    
    if cursor_name == '3':
        fleur = gtk.gdk.Cursor(gtk.gdk.TOP_RIGHT_CORNER)
        global_var.INDEX_CURSOR = 3
        
    if cursor_name == '4':
        fleur = gtk.gdk.Cursor(gtk.gdk.LEFT_SIDE)
        global_var.INDEX_CURSOR = 4
        
    if cursor_name == '5':
        fleur = gtk.gdk.Cursor(gtk.gdk.RIGHT_SIDE)
        global_var.INDEX_CURSOR = 5
        
    if cursor_name == '6':
        fleur = gtk.gdk.Cursor(gtk.gdk.BOTTOM_LEFT_CORNER)
        global_var.INDEX_CURSOR = 6
    
    if cursor_name == '7':
        fleur = gtk.gdk.Cursor(gtk.gdk.BOTTOM_SIDE)
        global_var.INDEX_CURSOR = 7
    
    if cursor_name == '8':
        fleur = gtk.gdk.Cursor(gtk.gdk.BOTTOM_RIGHT_CORNER)
        #fleur = gtk.gdk.Cursor(gtk.gdk.TCROSS)
        global_var.INDEX_CURSOR = 8
        #print 'cusor 8 global button press %s ' % global_var.button_press
    
    #canvas = item.get_canvas ()
    return_grap = canvas.pointer_grab(item, 
                gtk.gdk.POINTER_MOTION_MASK| gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                fleur, event.time)
    print "return grap event ",return_grap
                
    return True
    
def on_leave_notify(item, target, event,canvas,reset_color):
    item.props.fill_color_rgba = reset_color
    global_var.mouse_over_item_adj = False # reset mouse over item adj status
    
    if global_var.adj_box_press == False:
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, 0)
        canvas.window.set_cursor(gtk.gdk.pointer_ungrab()) 
        if os.name == 'nt': # fix cursor bug on win32
            # Reset mouse pointer to fix problem on win32
            arrow = gtk.gdk.Cursor(gtk.gdk.ARROW)
            canvas.pointer_grab(item, 
                    gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK,
                    arrow, event.time)
                    
            #canvas.pointer_ungrab(item, event.time)
            canvas.window.set_cursor(gtk.gdk.pointer_ungrab())
            global_var.outter = True
        print "reset cursor adjust item"
        
        
        
       

    return True


def createMoveBoxAlias(canvas,property,set_parent,main_item):
    root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    if set_parent == None:
        set_parent = root
    item = goocanvas.Rect (parent = set_parent,
                           x = property['x'],#/get_scale,#int
                           y = property['y'],#/get_scale,#int
                           width = property['width'],#int
                           height = property['height'],#int
                           line_dash=goocanvas.LineDash([3.0/get_scale, 3.0/get_scale]),
                           line_width = 0.8/get_scale)#, # int
    #global_var.box_select = item
    item.set_data ("itemProp", property)
    item.set_data ("main_item",main_item)
    return item

def createMoveEllipseAlias(canvas,property,set_parent,main_item):
    root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    if set_parent == None:
        set_parent = root
    item = goocanvas.Ellipse (parent = set_parent,
                           x = property['x'],#/get_scale,#int
                           y = property['y'],#/get_scale,#int
                           width = property['width'],#int
                           height = property['height'],#int
                           center_x=property['center_x'],
                           center_y=property['center_y'],
                           radius_x=property['radius_x'],
                           radius_y=property['radius_y'],
                           line_dash=goocanvas.LineDash([3.0, 3.0]),
                           line_width = 0.8)
                                            
    #global_var.box_select = item
    item.set_data ("itemProp", property)
    item.set_data ("main_item",main_item)
    # Re update position again
    item.props.x = property['x']
    item.props.y = property['y']
    return item

def importImage(canvas,property,set_parent,image):

    root = canvas.get_root_item ()
    get_scale = canvas.get_scale()
    if set_parent == None:
        set_parent = root
    item = goocanvas.Image (parent = set_parent,
                             pixbuf = image,
                             x = property['x'] ,
                             y = property['y'] ,
                             width = property['width']/get_scale ,
                             height = property['height']/get_scale)
                            
    canvas.set_data(property['main'], item)#itemProp
    item.set_data ("itemProp", property)
    item.connect ("button_release_event", on_button_release,canvas)
    item.connect ("focus_in_event", on_focus_in,canvas)
    item.connect ("focus_out_event", on_focus_out,canvas)
    item.connect ("button_press_event", on_button_press,canvas)
    item.connect ("key_press_event",  on_key_press)
    item.connect ("motion_notify_event", on_motion_notify)
    
    return item
    #item.scale(0.3,0.3)  
    
def ImportDropImage(pathFile,canvas):
    if pathFile is not None:
        if os.name != 'nt':# for linux and other
            pathFile = pathFile.replace('file://','')
        else: #for window
            pathFile = pathFile.replace('file://','')

        pathFile = pathFile.replace('\n','')
        pathFile = pathFile.replace('\r','')
        
        if os.path.isfile(pathFile):
        
            print pathFile
            im = gtk.gdk.pixbuf_new_from_file (pathFile)
            info = gtk.gdk.pixbuf_get_file_info(pathFile)
            print type(info[0])
            Img_type =  info[0]['name']
            lm_list = [im,pathFile]
            find_name = pathFile.split('/')
            imag_name = find_name[(len(find_name)-1)] +'_'+ str(im.get_width())+'x'+str(im.get_height())
            print imag_name
            
            del find_name # delete find
            global_var.image_store[imag_name] = [im,Img_type]
            #global_var.image_type[imag_name] = Img_type # type of image 
            
            print 'Len of Store Image = %s' % len(global_var.image_store)
            
            if global_var.image_use.has_key(imag_name): # check for dic has exist
                cnt = global_var.image_use[imag_name]
                global_var.image_use[imag_name] = cnt +1
            else:
                global_var.image_use[imag_name] = 1# create new dic and fill item = 1
            

            print 'Current same image count = %s' % global_var.image_use[imag_name]
            '''if global_var.image_use[imag_name] != None:
                global_var.image_use[imag_name] = 1
            else:
                cnt = global_var.image_use[imag_name]
                global_var.image_use[imag_name] = cnt +1
                
            print 'count %s' % global_var.image_use[imag_name] '''
            #TODO : Import image data
            prop={}
            prop['color'] = '#0000FF'
            prop['x'] =0
            prop['y'] = 0
            prop['radius_x'] = 0
            prop['radius_y'] = 0
            prop['width'] = im.get_width ()
            prop['height'] =  im.get_height ()
            prop['stroke_pattern'] = None
            prop['stroke_color'] = "#00FF00"
            prop['line_width'] = 2
            prop['can_focus'] = False
            prop['name'] = 'ImageItem'
            prop['main'] = 'ImageItem'
            prop['transform_x'] = 100.0# - (im.get_width()/2)
            prop['transform_y'] = 225.0# - (im.get_height()/2)
            prop['scale'] = 1
            prop['degree']  = 0
            prop['lock']= False
            prop['image_name'] = imag_name
            prop['dynamic'] = {}
            #prop['file'] = pathFile
            #prop['Image'] = im
            item = drawItem.importImage(canvas,prop,global_var.parent_active,global_var.image_store[imag_name][0]) 
            scale_c = global_var.canvas_scale # call global canvas scale
            item.set_simple_transform(prop['transform_x']/scale_c,prop['transform_y']/scale_c,prop['scale'] ,prop['degree'])
            global_var.bt_left['SelectionMode'].set_active(True)

        else:
            print 'Error to open :',pathFile
            
        return True
    else:
        print "Import none type"
            


def on_button_release (item, target, event,canvas):
    print 'New Shape Press + ' + str(event.x )
    print 'canvas scale = ' + str(canvas.get_scale())
    myProp = item.get_data('itemProp')
    print 'Select color  = ' + myProp['color']
    if global_var.mode_run == False:
        
        if  global_var.pan_select == False:
            print 'button release'
            
            global_var.bt['Delete'].set_sensitive(True)
            global_var.bt['Copy'].set_sensitive(True)
            global_var.bt['Cut'].set_sensitive(True)
            #item.set_property("width",100)
            canvas = item.get_canvas ()
            canvas.pointer_ungrab(item, event.time)
            print 'current pos x item =  ' + str(event.x)
        
    
    global key_press
    key_press = False
    
    return True

def on_focus_in (item,target, event,canvas):
    itemData = item.get_data ("itemProp")
    width = itemData["width"]
    height =  itemData["height"]
    #print  'Item main is %s' % itemData['main']
    scale = canvas.get_scale()
    #grp = item.get_parent()
    #chnumber = grp.find_child(item)
    #grp.remove_child(chnumber)

    ''' Note that this is only for testing. Setting item properties to indicate
    focus isn't a good idea for real apps, as there may be multiple views. '''
    #print 'focus in'
    
    lenMultiSel = len(global_var.multiSelect)

    if global_var.cmd_draw == 0:# and lenMultiSel < 2: # for selection only
        
        #for itemSelect in global_var.select_cursor :
        #    global_var.select_cursor[itemSelect].remove()
        #item.props.stroke_color = "yellow"
        property ={}
        property['line_wieght'] = 0.5/scale
        property['main'] = 'cursor Item'
        
        #8DD9D9
        #print 'item lock is %s' % itemData['lock']
        if itemData['lock'] == False:
            property['rgbaColor']=0x3cb37180 #blue
        else:
            property['rgbaColor']=0xFF001580 # red
            
        if global_var.itemSelect8Cursor.has_key(item):
            for j in range(8):
                global_var.itemSelect8Cursor[item][j].props.fill_color_rgba = property['rgbaColor']
            #print 'prepare before change color '
            
        global_var.itemSelectActive  = item

        #setBoundItem(item,canvas,property)
        
        
    return False

def setBoundItem(item,canvas,property,set_parent):
    '''
    1-------------2----------------3
    |                                |
    4                                5
    |                                |
    6-------------7----------------8 (selec arrow here)
    
    number is posiotin of arrow
    you can press and drag for resize the item property
    
    '''
    
    scale = canvas.get_scale()
    list = []
    sx,sy,scale_,degree = item.get_simple_transform()
    line_width = item.props.line_width/2
    r1x = (sx-line_width)-(10/scale)
    r1y = (sy-line_width)-(10/scale)
    
    #Create adjust cursor when click item conner 1 (TOP Left)
    property['x'] = r1x
    property['y'] =  r1y
    property['name'] = 1
    list.append(createAdjustCursor(canvas,property,'1',item,set_parent))
    
    #Create adjust cursor when click item conner 2 (TOP Middle)
    mid_x = ((item.props.width+item.props.line_width)/2)+(sx-line_width)
    mid_x = mid_x - (3.5/scale)
    property['x'] = mid_x
    property['y'] =  r1y
    property['name'] = 2
    list.append(createAdjustCursor(canvas,property,'2',item,set_parent))
    
    #Create adjust cursor when click item conner 3 (TOP right)
    r3x = sx + (item.props.width+(3/scale)+line_width)
    property['x'] = r3x
    property['y'] =  r1y
    property['name'] = 3
    list.append(createAdjustCursor(canvas,property,'3',item,set_parent))
    
    #Create adjust cursor when click item conner 4 (Middle Left)
    mid_y = ((item.props.height+item.props.line_width)/2)+(sy-line_width)
    mid_y = mid_y - (3.5/scale)
    property['x'] = r1x
    property['y'] =  mid_y
    property['name'] = 4
    list.append(createAdjustCursor(canvas,property,'4',item,set_parent))
    
    #Create adjust cursor when click item conner 5 (Middle Right)
    property['x'] = r3x
    property['y'] =  mid_y
    property['name'] = 5
    list.append(createAdjustCursor(canvas,property,'5',item,set_parent))
    
    #Create adjust cursor when click item conner 6 (Buttom Left)
    r6y = sy+ item.props.height  + line_width + (5/scale)
    property['x'] = r1x
    property['y'] =  r6y
    property['name'] = 6
    list.append(createAdjustCursor(canvas,property,'6',item,set_parent))
    
    #Create adjust cursor when click item conner 7 (Buttom Middle)
    property['x'] = mid_x
    property['y'] =  r6y
    property['name'] = 7
    list.append(createAdjustCursor(canvas,property,'7',item,set_parent))
    
    #Create adjust cursor when click item conner 8 (Buttom Right)
    property['x'] = r3x
    property['y'] =  r6y
    property['name'] = 8
    list.append(createAdjustCursor(canvas,property,'8',item,set_parent))
        
    return list

def update_new_round_item(item,scale):
    new_x = []
    new_y = []
    new_width_height = []
    
    sx,sy,scale_,degree = item.get_simple_transform()
    line_width = item.props.line_width/2
    r1x = (sx-line_width)-(10/scale)
    r1y = (sy-line_width)-(10/scale)
    
    #update adjust cursor conner number 1 (Top left)
    new_x.append(r1x)#-10)
    new_y.append(r1y)#-10)
    
    #update adjust cursor conner number 2 (Top Middle)
    mid_x = ((item.props.width+item.props.line_width)/2)+(sx-line_width)
    mid_x = mid_x - (3.5/scale)
    new_x.append(mid_x)
    new_y.append(r1y)
    
    #update adjust cursor conner number 3 (Top right)
    r3x = sx + (item.props.width+(3/scale)+line_width)
    new_x.append(r3x)
    new_y.append(r1y)
    
    #update adjust cursor conner number 4 (Middle left)
    mid_y = ((item.props.height+item.props.line_width)/2)+(sy-line_width)
    mid_y = mid_y - (3.5/scale)
    new_x.append(r1x)
    new_y.append(mid_y)
    
    # update adjust cursor conner number 5 (Middle right)
    new_x.append(r3x)
    new_y.append(mid_y)
    
    #update adjust cursor conner number 6 (buttom left)
    r6y = sy+ item.props.height  + line_width + (5/scale)
    new_x.append(r1x)
    new_y.append(r6y)
    
    #update adjust cursor conner number 7 (buttom middle)
    new_x.append(mid_x)
    new_y.append(r6y)
    
    #update adjust cursor conner number 8 (buttom middle)
    new_x.append(r3x)
    new_y.append(r6y)
    
    for i in range(8):
        global_var.itemSelect8Cursor[item][i].props.x = new_x[i]
        global_var.itemSelect8Cursor[item][i].props.y= new_y[i]
        global_var.itemSelect8Cursor[item][i].props.width =7/scale
        global_var.itemSelect8Cursor[item][i].props.height =7/scale
        #global_var.itemSelect8Cursor[item][i].props.line_width =0
        
    return True
    

def roundItem(item,canvas,set_parent): # use when selection many item in area

    itemData = item.get_data ("itemProp")
    scale = canvas.get_scale()
    property ={}
    property['line_wieght'] = 0.5/scale
    property['main'] = 'cursor Item'
    property['itemParent'] = item

    #print 'round item'
   

    if itemData['lock'] == False:
        property['rgbaColor']=0x3cb37180 #blue
    else:
        property['rgbaColor']=0xFF001580 # red
        
    
    listItem = setBoundItem(item,canvas,property,set_parent)
        
    return listItem


def on_focus_out (item, canvas,target, event):
    #itemData = item.get_data ("itemProp")
    #width = itemData["width"]
    #height =  itemData["height"]
    '''if id:
        print "%s received focus-out event" %  itemData["name"]
    else:
        print "unknown"
    '''
    ''' Note that this is only for testing. Setting item properties to indicate
     focus isn't a good idea for real apps, as there may be multiple views. '''
    # reset original line color
    prop = item.get_data('itemProp')
    color = prop['stroke_color']
    item.props.stroke_color = color
    #item.props.stroke_pattern = None
    rgba_color = 0x3cb37180 # color soft blue (defualt color)
    if prop['lock'] == True:
        rgba_color =0xFF001580 # red
        
    if global_var.itemSelect8Cursor.has_key(item):
        for j in range(8):
            global_var.itemSelect8Cursor[item][j].props.fill_color_rgba = rgba_color # change color to soft red
        #print 'prepare before change color '

    return False

def clearItemSelectCursor():
    #print 'Before clear item status multiselect Len = %s item cursor len %s ' % (len(global_var.multiSelect),len(global_var.itemSelect8Cursor))
    
    if len(global_var.multiSelect)>0:
        for t in global_var.multiSelect:
            for j in range(8):
                #try:
                if global_var.itemSelect8Cursor[t][j] is not None:
                    global_var.itemSelect8Cursor[t][j].remove()
                #except:
                #    print 'error when remove item Selection 8 cusor item is aready remove[drawItem]'
                
        # clear all temp data 
        del global_var.multiSelect[0:len(global_var.multiSelect)]
        if  len(global_var.itemSelect8Cursor)>0:
               global_var.itemSelect8Cursor.clear()
            
    #print 'After clear item status multiselect Len = %s item cursor len %s ' % (len(global_var.multiSelect),len(global_var.itemSelect8Cursor))
                
    return True

#def itemRightClick(item,itemData,event,canvas):
#    popup_on_right_click(item,itemData,event,canvas) #call popup_menu.py
#   return True



def on_button_press (item, target, event,canvas):
    itemData = item.get_data ("itemProp")
    width = itemData["width"]
    height =  itemData["height"]
    global key_press
    global pos_x0,pos_y0
    pos_x0 = event.x
    pos_y0 = event.y

    global_var.outter = False # mouse move leave adjust cursor for bug fix on win32
    key_press = True # check key press status
    global_var.sel_item = False # reset item press
    global_var.item_press = True # set item press 
    
    if(event.button == 3):# mouse right click
        #itemRightClick(item,itemData,event,canvas) # show item property to change etc. color , line wieght , action menu
        if len(global_var.multiSelect) > 0 :
            popup_on_right_click(item,event,canvas) #call popup_menu.py
            global_var.button_press = False
                
    global diff_x,diff_y # delta position x ,y 
    
    if(event.button == 1 and global_var.cmd_draw == 0 ):  # for selection mode and mouse left click
        #check item in select group 
        global_var.itemSelectActive  = item # load item click to temporary data (global_var.itemSelectActive)
        ''' Check item in group multiselect
        '''
        Item_result = None
        canvas.window.set_cursor(gtk.gdk.pointer_ungrab())
        print "clear grab cursor on item button press"

        if global_var.mode_run == False: # if edit mode is inactive[false] you can adjust item, delete , modifly etc...
            
            # READ GROUP ITEM
            #parent = None
            group_root,parent = return_parent_root(item)#call group_item.py -->retrun_parent_root to check root, parent item
            #Return when found item under group_root on active item [current item  selected]
            #--[group_root]
            #    |-------[parent]
            #             |------[current item  selected]
            #TODO: Item on button press
            print "read group root %s and parent item %s " % (group_root,parent)
            print "edit group mode =  ",global_var.edit_group_mode
            if group_root is not None:
                #check item under group if group_root return not equal None 
                #It's mean current selected is under group [not single item]
                Item_under_group = True
                #check util group = root
                tmp_root = group_root
                tmp_parent =parent
                cnt = 0
                current_group_check = None
                if global_var.edit_group_mode == True:
                    while parent != global_var.edit_item_parent:
                        cnt +=1
                        tmp_root = group_root
                        tmp_parent =parent
                        print "loop while find group root [%s]" % cnt
                        group_root,parent = return_parent_root(parent)
                        if parent == None:
                            print "item not in group"
                            global_var.edit_item_area_dash.remove()
                            renew_group_size(None,global_var.edit_item_parent)# resize of group
                            item1 = global_var.edit_item_parent # current item edit 
                            parent1 = global_var.edit_item_parent.get_parent() # get parent curretn item
                            global_var.edit_offset_xy = offset_parent_position(item1)
                            upper_group_edit_item(item1 ,parent1,canvas)
                            
                            global_var.itemSelectActive2 = None # Clear active item for set above and below
                            #break
                            return True
                else:
                    while group_root != None:
                        cnt +=1
                        tmp_root = group_root
                        tmp_parent =parent
                        print "loop while find group root [%s]" % cnt
                        group_root,parent = return_parent_root(parent)
                    
                group_root = tmp_root
                parent = tmp_parent
                print "get item ingroup_root %s  , parent %s  deep count %s" % (group_root,parent,cnt)
            else:
                Item_under_group = False
                #It's mean item is single [not in group ] there is free not calculate offset position
                #In these case it is easy to modifier such as , move ,resize, etc   
                
                
            if Item_under_group:
                global_var.parent_active = parent
                print "edit mode is ",global_var.edit_group_mode
                print "global group active is " ,global_var.parent_active
                #print "Group parent property is x = %s y = %s " % (parent.props.x,parent.props.y)
                #print "Group parent property is width= %s height = %s " % (parent.props.width,parent.props.height)
                if global_var.edit_group_mode == False:
                    item = parent
                
                else:
                    print "deep count loop item in group ",cnt
                    if cnt == 0:
                        pass
                        #item = parent
                    else:
                        item = parent#.get_parent()
                
            if global_var.edit_group_mode == False:
                parent = group_root
            #else:
            try:
                Item_result = global_var.multiSelect.index(item)
                check_Item_in_group = True
            except ValueError:
                check_Item_in_group = False
            # clear older selection 
            ''' If item is alaready in multi selec it's return = True
            '''
            
            
            #set parent on create box item 
            if global_var.edit_group_mode == True:
                parent = global_var.edit_item_parent
            
            if global_var.key_shift_press == False  and  check_Item_in_group == False:
                clearItemSelectCursor() # if item is not in group it will be reset the selection
            
            
            
            try:
                Item_result = global_var.multiSelect.index(item)
            except ValueError:
                global_var.multiSelect.append(item)
                global_var.itemSelect8Cursor[item]=roundItem(item,canvas,parent)
            #Select another item by press SHIFT KEY and CLICK Select
                        
           
                #check tem on list 
            
            canvas = item.get_canvas ()
            
            itemData = item.get_data ("itemProp")
            width = itemData["width"]
            height =  itemData["height"]
            #Update item property on dialog box property 
            if global_var.itemSelectActive2 != item :
                item_color =  itemData["color"]
                set_color = gtk.gdk.Color(item_color)
                global_var.dialogWidget['colorColor_button'].set_color(set_color) # on dialog property set color button
                global_var.itemSelectActive2 = item
                
                #print "SET FILL MODE ",itemData['fill_mode']
                if itemData.has_key('fill_mode'):
                    if itemData['fill_mode'] == 'None':
                        global_var.dialogWidget['colorFill_option'].set_active(0)
                        
                    if itemData['fill_mode'] == 'Solid':
                        global_var.dialogWidget['colorFill_option'].set_active(1)
                        
                    if itemData['fill_mode'] == 'RGBA':
                        global_var.dialogWidget['colorFill_option'].set_active(2)
                            
                #Set spinner and hscale for alpha 
                #--------------------------------
                if itemData.has_key('rgbaColor'):
                    if itemData['rgbaColor'] is not None:
                        color_rgba = item_color.replace('#','')
                        color_rgba = int(color_rgba,16)
                        val = itemData['rgbaColor'] - (color_rgba*256)
                        val = int(val/2.54)
                        global_var.dialogWidget['colorOpacity_hscale'].set_value(val)
                        global_var.dialogWidget['colorOpacity_spinner'].set_value(val)
                        
                #get line width to set new item dialog value 
                #['stroke_color']
                print "Line color ",itemData['stroke_color']
                get_line_color = gtk.gdk.Color(itemData['stroke_color'])
                global_var.dialogWidget['lineColor'].set_color(get_line_color)
                #Line width 
                active_line_w = int(global_var.itemSelectActive2.props.line_width) #int(itemData['line_width'])-1
                if active_line_w < 0:
                    active_line_w = 0
                global_var.dialogWidget['lineWidth'].set_active(active_line_w)
                    
                #Line curve 
                if itemData["main"]== 'Rect Item':
                    line_curve = global_var.itemSelectActive2.props.radius_x
                    global_var.dialogWidget['lineCurve_spinner'].set_value(line_curve)
                    
                #Text data
                if itemData["main"]== 'Text Item':
                    getText =  item.props.text
                    global_var.dialogWidget['text_edit'].set_text(getText)
                    
            
            # TODO :  Set item value to dialog property
            if itemData['lock'] == False:
                if global_var.sel_press == True:
                #print 'Delete selection area'
                    global_var.sel_press = False
                    global_var.sel_area.remove()
                
                
                '''fleur = gtk.gdk.Cursor(gtk.gdk.FLEUR)#change mouse cursor to move icon
                canvas.pointer_grab(item, 
                            gtk.gdk.POINTER_MOTION_MASK | gtk.gdk.BUTTON_PRESS_MASK| gtk.gdk.BUTTON_RELEASE_MASK,
                            fleur, event.time)
            
                canvas.grab_focus (item)'''
                name = itemData["name"]
                
                
                    
                # Create box move select 
                #print 'copy method : lenght of multi select %s' % len(global_var.multiSelect)
                global_var.multiSelect.reverse()
                for listBox in global_var.multiSelect:
                #for j in range(len(global_var.multiSelect),0,-1):
                    #listBox = global_var.multiSelect[j-1]
                    boxProperty = {}
                    scale = canvas.get_scale()
                    #Copy item property
                    sx,sy,scale_,degree = listBox.get_simple_transform()
                   
                    prop = listBox.get_data('itemProp')
                    boxProperty['x'] =  sx#listBox.props.x 
                    boxProperty['y'] =  sy#listBox.props.y
                    boxProperty['width'] =  listBox.props.width
                    boxProperty['height'] =  listBox.props.height
                    boxProperty['itemParent'] = listBox
                        
                    
                    if prop['main'] == 'Ellipse Item':
                        #boxProperty['x'] =  listBox.props.x 
                        #boxProperty['y'] =  listBox.props.y
                        boxProperty['radius_x'] =  listBox.props.radius_x
                        boxProperty['radius_y'] =  listBox.props.radius_y
                        boxProperty['center_x'] =  listBox.props.center_x
                        boxProperty['center_y'] =  listBox.props.center_y
                        boxItem = createMoveEllipseAlias(canvas,boxProperty,parent,listBox)
                        global_var.multiBoxMoveSelect.append(boxItem)
                    #TODO : Move rect 
                    if prop['main'] == 'Rect Item' :
                        boxProperty['radius_x'] =  listBox.props.radius_x
                        boxProperty['radius_y'] =  listBox.props.radius_y
                        print "radius copy ",boxProperty['radius_x']
                        print "Get position x %s y %s " % (boxProperty['x'],boxProperty['y'])
                        
                        boxItem = createMoveBoxAlias(canvas,boxProperty,parent,listBox)
                        global_var.multiBoxMoveSelect.append(boxItem)
                        
                    # Move image file to new position 
                    if prop['main'] == 'ImageItem':
                        boxItem = createMoveBoxAlias(canvas,boxProperty,parent,listBox)
                        global_var.multiBoxMoveSelect.append(boxItem)
                        
                    if prop['main'] == 'group Item':
                        #print "copy group and main is ",
                        #print listBox
                        boxItem = createMoveBoxAlias(canvas,boxProperty,parent,listBox)
                        global_var.multiBoxMoveSelect.append(boxItem)
                        
                    if prop['main'] == 'Text Item':
                        print "Get position x %s y %s " % (boxProperty['x'],boxProperty['y'])
                        boxItem = createMoveBoxAlias(canvas,boxProperty,parent,listBox)
                        global_var.multiBoxMoveSelect.append(boxItem)
        else:
            #when run mode == True
            #print 'item press on run'
            itemData = item.get_data ("itemProp")
            if itemData.has_key('dynamic'):
                pointDynamic = itemData['dynamic']
                if pointDynamic.has_key('Pick'):
                        itemSelect = pointDynamic['Pick']
                        typeItem =  str(type(itemSelect))
                        #['ON','OFF','Toggle Value','Forward','Backward','Set Value','Close Window','Run Script']
       
                        if typeItem == '<class \'animation.animationPicker\'>':
                            opc_tag = itemSelect.tag
                            server_name = itemSelect.opc_server_name
                            tag = [opc_tag]
                            result = ''
                            opcSocket = read_from_socket()
                            if itemSelect.cmd_type == 'Toggle Value':
                                if global_var.opc_tag_value[opc_tag][0] == 'False':
                                    global_var.opc_tag_value[opc_tag] = ('True','Bad','12:12:1234')
                                    
                                    #result = opcSocket.writeOPCSocket(server_name,tag,'True')
                                else:
                                    global_var.opc_tag_value[opc_tag] = ('False','Bad','12:12:1234')
                                    #result = opcSocket.writeOPCSocket(server_name,tag,'False')
                                    
                            if  itemSelect.cmd_type == 'ON':
                                global_var.opc_tag_value[opc_tag] = ('True','Bad','12:12:1234')
                                #result = opcSocket.writeOPCSocket(server_name,tag,'True')
                                
                            if  itemSelect.cmd_type == 'OFF':
                                global_var.opc_tag_value[opc_tag] = ('False','Bad','12:12:1234')
                                #result = opcSocket.writeOPCSocket(server_name,tag,'False')
                                
                            print 'Command setting ',itemSelect.cmd_type
                            print 'Result of write tag ',result 
        
       
    return True

def on_button_release (item, target, event,canvas):
    if  global_var.pan_select == False:
        #print 'button release'
        global_var.bt['Delete'].set_sensitive(True)
        global_var.bt['Copy'].set_sensitive(True)
        global_var.bt['Cut'].set_sensitive(True)
        #item.set_data("width",100)
        canvas = item.get_canvas ()
        canvas.pointer_ungrab(item, event.time)
        scale = canvas.get_scale()
        # Clear other selection 
        lenBox = len(global_var.multiBoxMoveSelect)
            
        #--------------------------------------------------
        #------COPY ITEM USE DRAG MOUSE WITH CTRL LEFT KEY-
        #--------------------------------------------------
        if global_var.key_control_press: # to COPY ITEM
            tempCopy = []
            
            for newPosItem in global_var.multiBoxMoveSelect:
                thisItem = newPosItem.get_data ('main_item') # thisItem is the original item (master item)
                print "copy children item =  ",thisItem.get_n_children()
                # Copy Item under Group [item more than one]
                if thisItem.get_n_children()>0: # Checked item under group 
                    GroupCopy(thisItem,newPosItem,canvas,tempCopy,'CtrlDrag')
                else:
                    #COPY SINGLE PROPERTY ITEM 
                    NoneGroupCopy(thisItem,newPosItem,canvas,tempCopy,'CtrlDrag')
                   
            #MOVE Selected cusor to new item and update new data in global_var.multiSelect
            refershCursor2NewItem(canvas,tempCopy)
            
        #------------MOVE ITEM TO NEW POSITION ---------
        #--------Move item by drag mouse and release to new position 
        else:
            for newPosItem in global_var.multiBoxMoveSelect:
                itemProp = newPosItem.get_data ('itemProp')
                parentItem = itemProp['itemParent']
                myData = parentItem.get_data ('itemProp')
                if myData['lock'] == False:
                    #item_positon = newPosItem.get_simple_transform()
                    #parentItem.props.x = item_positon[0]#newPosItem.props.x
                    #parentItem.props.y = item_positon[1]#newPosItem.props.y
                    sx = newPosItem.props.x
                    sy = newPosItem.props.y
                    parentItem.set_simple_transform(sx,sy,1,0)
                    update_new_round_item(parentItem,scale)
                   
                print "Move item to new position"
                
                if global_var.mode_run == False and global_var.edit_group_mode == True :
                    print 'Global button press =  %s ' % global_var.button_press
                    #call find_width_height_group in group_item.py to update new position 
                    # select dash 
                    refresh_new_group_size()
                        

        # Remove box selected
        lenBox = len(global_var.multiBoxMoveSelect)
        for k in range(lenBox):
            global_var.multiBoxMoveSelect[k].remove()
        
        del global_var.multiBoxMoveSelect[0:len(global_var.multiBoxMoveSelect)]#delete data buffer
         
    global key_press
    key_press = False
    global_var.sel_item = False
    global_var.item_press = False
    
    return True

def NoneGroupCopy(thisItem,newPosItem,canvas,tempCopy,modeCopy):
    # TODO : Copy single item property 
    scale = canvas.get_scale()
    if modeCopy == 'CtrlDrag': # Copy by Hold CTRL Key and Drag item to new position and finish copy  by release mouse
        itemProp = newPosItem.get_data ('itemProp')
        parentItem = itemProp['itemParent']
        myData = parentItem.get_data ('itemProp')
        pos_x = newPosItem.props.x#/scale
        pos_y = newPosItem.props.y#/scale
    else:
        # Normal copy by CTRL+ c and Past By CTRL + v
        myData = thisItem.get_data ('itemProp')
        parentItem = thisItem
        sx,sy,scale_,degree = thisItem.get_simple_transform()
        pos_x = sx + 4
        pos_y = sy + 4
        
    cpData = {}
    for listCp in myData:
        #print listCp,
        #print myData[listCp]
        if listCp == 'dynamic':
            cpData['dynamic'] = {}
            for listDynamic in myData['dynamic']:# = {}
                listProperty = myData['dynamic'][listDynamic]
                AnimationProp = copyItemProp()
                #newAnimationProp = None
                newAnimationProp = AnimationProp.listAnimate(listProperty)#copy item animation property
                cpData['dynamic'] [listDynamic]=newAnimationProp
                #print 'old dynamic tag name :',listProperty
                #print 'dynamic tag opc server name :',newAnimationProp.opc_server_name
        else:
            cpData[listCp] = myData[listCp]
        
    cpData['x'] = 0
    cpData['y'] = 0
    cpData['transform_x'] = pos_x #newPosItem.props.x#/scale
    cpData['transform_y'] = pos_y #newPosItem.props.y#/scale
   
    cpData['width'] = newPosItem.props.width*scale
    cpData['height'] =  newPosItem.props.height*scale
    cpData['line_width'] = thisItem.props.line_width*scale
    
    if myData['main'] != "ImageItem":
        if myData['main'] != "Text Item":
            cpData['radius_x'] = thisItem.props.radius_x*scale
            cpData['radius_y'] = thisItem.props.radius_y*scale
        else:
            cpData['buffer'] = thisItem.props.text
        
        cpData['width'] = thisItem.props.width
        cpData['height'] =  thisItem.props.height
        
    if myData['main'] != "Ellipse Item":
        #cpData['radius_x'] = thisItem.props.radius_x*scale
        #cpData['radius_y'] = thisItem.props.radius_y*scale
        pass

    if global_var.edit_group_mode == False: 
        global_var.parent_active = None # reset if not edit item mode 

    newItem = loadingDataItem(canvas,cpData,global_var.parent_active) # create copy item
    newItem.set_simple_transform(cpData['transform_x'],cpData['transform_y'],1 ,0)
    tempCopy.append(newItem)
    
    print "*********debug copy item*********"
    print "Print item ",newItem
    for t in cpData:
        #print t
        if t == 'dynamic':
            for u in cpData[t]:
                #print '      > ',u
                pass
    print "*********************************"
    #del cpData,myData # delete temp data 
#TODO : COPY GROUP ITEM
def GroupCopy(thisItem,newPosItem,canvas,tempCopy,modeCopy):
    
    if modeCopy == 'CtrlDrag': 
        pos_x = newPosItem.props.x
        pos_y = newPosItem.props.y
    else:#Copy by Normal
        print "Copy group item by normal"
        sx,sy,scale_,degree = thisItem.get_simple_transform()
        pos_x = sx + 4
        pos_y = sy + 4
        
    
    if global_var.edit_group_mode ==True:
        newItem = copyGroupItem(canvas,thisItem,global_var.edit_item_parent)
    else:
        newItem = copyGroupItem(canvas,thisItem,None)
        
    newItem.props.x = 0#newPosItem.props.x#*scale
    newItem.props.y = 0#newPosItem.props.y#*scale
    newItem.props.width = newPosItem.props.width#*scale
    newItem.props.height = newPosItem.props.height#*scale
    
    
    newItem.set_simple_transform(pos_x,pos_y,1,0)
    tempCopy.append(newItem)
    
def refershCursor2NewItem(canvas,tempCopy): # add new item to multiSelected and update new roundItem
    if len(global_var.multiSelect) > 0:
        nepohmi.clear_all_multiSelected()
        print "create new item selected and copy to new global_var.multiSelect"
        cursorParent = global_var.parent_active
        for nItem in tempCopy:
            global_var.multiSelect.append(nItem)
            if nItem.get_n_children() > 0:
                UpcursorParent = cursorParent.get_parent()
            else:
                UpcursorParent = global_var.parent_active
            global_var.itemSelect8Cursor[nItem]=roundItem(nItem,canvas,UpcursorParent)
            
        if  global_var.edit_group_mode == True: 
            refresh_new_group_size()

def copyGroupItem(canvas,item,self_parent):
    #[def] is copy group item all group 
    n = item.get_n_children()
    itemProp = item.get_data ('itemProp')
    scale = canvas.get_scale()
    print "copy item main is ",itemProp['main']
    nextParent = None
    if n > 0:
        itemProp = item.get_data ('itemProp')
        newPosItem = item
        cpData = {}
        for listCp in itemProp:
            cpData[listCp] = itemProp[listCp]
            
        sx,sy,scale_,degree = newPosItem.get_simple_transform()
        cpData['x'] = 0#newPosItem.props.x*scale
        cpData['y'] = 0#newPosItem.props.y*scale
        cpData['width'] = newPosItem.props.width#*scale
        cpData['height'] = newPosItem.props.height#*scale
        #item.set_data ('itemProp',cpData)
        nextParent = createGroup(canvas,cpData,self_parent)
        nextParent.set_simple_transform(sx,sy,scale_,degree) # update new position
    else:
        #parentItem = itemProp['itemParent']
        myData = item.get_data ('itemProp')
        newPosItem = item
        cpData = {}
        for listCp in myData:
            if listCp == 'dynamic':
                cpData['dynamic'] = {}
                for listDynamic in myData['dynamic']:# = {}
                    listProperty = myData['dynamic'][listDynamic]
                    AnimationProp = copyItemProp()
                    #newAnimationProp = None
                    newAnimationProp = AnimationProp.listAnimate(listProperty)#copy item animation property
                    cpData['dynamic'] [listDynamic]= newAnimationProp
                    #print 'old dynamic tag name :',listProperty
                    #print 'dynamic tag opc server name :',newAnimationProp.opc_server_name
            else:
                cpData[listCp] = myData[listCp]
            
        #if cpData['main'] == 'Ellipse Item':
        cpData['x'] = 0#newPosItem.props.x*scale
        cpData['y'] = 0#newPosItem.props.y*scale
        if myData['main'] != "ImageItem":
            cpData['radius_x'] = item.props.radius_x*scale
            cpData['radius_y'] = item.props.radius_y*scale
            cpData['width'] = item.props.width
            cpData['height'] =  item.props.height
            #cpData['radius_x'] = item.props.radius_x*scale
            #cpData['radius_y'] = item.props.radius_y*scale
        #cpData['width'] = newPosItem.props.width#*scale
        #cpData['height'] =  newPosItem.props.height#*scale
        #cpData['line_width'] = item.props.line_width*scale
        
        
        cpData['width'] = newPosItem.props.width
        cpData['height'] =  newPosItem.props.height
        cpData['line_width'] = item.props.line_width*scale
            
        #else:
            #cpData['x'] = newPosItem.props.x*scale
            #cpData['y'] = newPosItem.props.y*scale
        #cpData['width'] = newPosItem.props.width*scale
        #cpData['height'] = newPosItem.props.height*scale
            #cpData['radius_x'] = newPosItem.props.radius_x*scale
            #cpData['radius_y'] = newPosItem.props.radius_y*scale
        
        #TODO : Copy image on group
        sx,sy,scale_,degree = newPosItem.get_simple_transform()
        newItem = loadingDataItem(canvas,cpData,self_parent) # create copy item
        newItem.set_simple_transform(sx,sy,scale_,degree)
        
    for i in range(n):
        print " Children of item is ",item.get_child(i)
        copyGroupItem(canvas,item.get_child(i),nextParent)
        #call copy all item under group 
    return nextParent

    
def on_motion_notify (item, target, event):
    #print 'motion'
    #canvas = item.get_canvas ()
    #name = item.get_data ("name")
    #global key_press

    '''if item == canvas.get_data("name_red") and global_var.sel_item== True:
        x = event.x
        y = event.y
        width = (MIDDLE - y) / 5
        if width < 0:
            return False
        canvas.set_data("width", width)
        #canvas.set_data("width", 100)'''
        #print 'press name red before move!'
    global_var.mouse_over_item = True
    
    if global_var.item_press== True :
        for boxItem in global_var.multiBoxMoveSelect:
            prop = boxItem.get_data('itemProp')
        #move_drag_box(canvas.get_data("name_red"), LEFT, MIDDLE - 10 * width / 2.0)
            #if prop['lock'] == False: # check item selection and no lock position select
            global pos_x0,pos_y0
            
            x = event.x-pos_x0
            y = event.y-pos_y0
            #print pos_x0,pos_y0,x,y
            #print 'Move...'
            move_drag_box(boxItem, x, y,prop['x'],prop['y'])
   
    return False# if True when stop signal

def move_drag_box(item, x, y,old_x,old_y):
    #global diff_x,diff_y
    item.props.x = old_x + x
    item.props.y = old_y + y
    return True

def updateBoxSelectPosition(item):
    global_var.select_cursor['1'].props.x = item.props.x-10
    global_var.select_cursor['1'].props.y = item.props.y-10
    
    global_var.select_cursor['2'].props.x = item.props.x + (item.props.width-7)/2
    global_var.select_cursor['2'].props.y = item.props.y-10
    
    global_var.select_cursor['3'].props.x =  item.props.x + (item.props.width+3)
    global_var.select_cursor['3'].props.y = item.props.y -10
    
    global_var.select_cursor['4'].props.x =  item.props.x -10
    global_var.select_cursor['4'].props.y = item.props.y + (item.props.height-7)/2
    
    global_var.select_cursor['5'].props.x = item.props.x + (item.props.width+3)
    global_var.select_cursor['5'].props.y =  item.props.y + (item.props.height-7)/2
    
    global_var.select_cursor['6'].props.x =  item.props.x -10
    global_var.select_cursor['6'].props.y =  item.props.y + (item.props.height+3)
    
    global_var.select_cursor['7'].props.x = item.props.x + (item.props.width-7)/2
    global_var.select_cursor['7'].props.y =   item.props.y + (item.props.height+3)
    
    global_var.select_cursor['8'].props.x =  item.props.x + (item.props.width+3)
    global_var.select_cursor['8'].props.y =   item.props.y + (item.props.height+3)
    

def on_key_press (item, target, event):
    print event.keyval
    if id:
        global_var.bt['Delete'].set_sensitive(True)
        #global_var.bt['Paste'].set_sensitive(False)
        global_var.bt['Copy'].set_sensitive(True)
        print "%s received key-press event" % id
    else:
        print "unknown"
    if event.keyval ==65535 : # key press delete
        undo.undoListStore(global_var.undoList,'Delete Item',None,item,None)
        prop = item.get_data('itemProp')
        if prop['main'] == 'ImageItem':
            imagIndex = prop['image_name']
            list_cnt = global_var.image_use[imagIndex]
            if list_cnt < 2:
                del global_var.image_use[imagIndex]
                del global_var.image_store[imagIndex]
            else:
                global_var.image_use[imagIndex] = list_cnt-1
        
        for itemSelect in global_var.select_cursor :
            global_var.select_cursor[itemSelect].remove()
        
        global_var.bt['Copy'].set_sensitive(False)
        global_var.bt['Cut'].set_sensitive(False)
        global_var.bt['Delete'].set_sensitive(False)
        global_var.bt['Undo'].set_sensitive(True)
        item.remove()
    if event.keyval == 65307: # key ESC
        print 'ESC key unselected item'
        global_var.bt['Delete'].set_sensitive(False)
        global_var.bt['Copy'].set_sensitive(False)
        global_var.bt['Cut'].set_sensitive(False)
        #item.props.stroke_pattern = None # reset stroke
        item.props.stroke_color = "black"
        global_var.itemSelectActive = None # Delete on Item Select
       
        
    return False



    
def loadingDataItem(canvas,itemProperty,set_parent):
    if itemProperty['main'] == 'Rect Item':
        item = createRect(canvas,itemProperty,set_parent)
        
    if itemProperty['main'] == 'Ellipse Item':
        item = createEllipse(canvas,itemProperty,set_parent)

    if itemProperty['main'] == 'Text Item':
        item = createText(canvas,itemProperty,set_parent)

    if itemProperty['main'] == 'Line Item':
        item = createLine(canvas,itemProperty,set_parent)
        
    if itemProperty['main'] == 'group Item':
        item = createGroup(canvas,itemProperty,set_parent)
        
    if  itemProperty['main'] == 'ImageItem':
        imag_name=itemProperty['image_name']
        #print 'loading image file  name is  ' + imag_name
        #print global_var.image_store[imag_name]
                #prop['file'] = pathFile
                #prop['Image'] = im
        #drawItem.importImage(data[2],prop,global_var.image_store[imag_name]) 
        item = importImage(canvas,itemProperty,set_parent,global_var.image_store[imag_name][0])
        
    if itemProperty['main'] =='Background Rect Item':
        print "Background Found"
        item = drawItem.createBackground(canvas, itemProperty)
    prop = item.get_data('itemProp')
    #if prop is not None:
    scale_c = global_var.canvas_scale
    item.set_simple_transform(prop['transform_x']/scale_c,prop['transform_y']/scale_c,prop['scale'] ,prop['degree'])

    return item 
    
    
