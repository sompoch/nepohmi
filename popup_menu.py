import goocanvas
import gtk
import global_var
import drawItem
import nepohmi
from group_item  import return_parent_root
from itemProperty import *
from dynamic import displayActionDynamic
from group_item import * #group_item_all,ungroup_item_all,return_parent_root
                        #from edit_group_item_all
import undo

def popup_on_right_click(item,event,canvas):
    print "popup menu"
    prop = item.get_data ("itemProp")
    m = gtk.Menu()
    i = gtk.MenuItem("Edit")
    root_item,parent = return_parent_root(item)
        
    if root_item == None:
        i.set_sensitive(False)
    else:
        if parent.get_n_children() > 0:
            i.set_sensitive(True)
        else:
            i.set_sensitive(False)
    #if global_var.edit_group_mode:
    #    i.set_sensitive(False)   bbf
    sep1 = gtk.SeparatorMenuItem()
    sep1.show()
    #-------Copy area-------
    copy = gtk.MenuItem("Copy")
    copy.connect("activate",copy_paste_Item,'copy',canvas)
    copy.show()
    
    cut = gtk.MenuItem("Cut")
    cut.connect("activate",copy_paste_Item,'cut',canvas)
    cut.show()
    
    past = gtk.MenuItem("Paste")
    past.connect("activate",copy_paste_Item,'paste',canvas)
    past.show()
        
    sep2 = gtk.SeparatorMenuItem()
    sep2.show()
    
    bringTo = gtk.MenuItem('Bring to ')
    i.connect("activate",edit_group_item,item,canvas)
    
    b_above = gtk.MenuItem("Front")
    b_above.connect("activate", check_item_raise_below,global_var.itemSelectActive2,'raise')
    b_below = gtk.MenuItem("Back")
    b_below.connect("activate", check_item_raise_below,global_var.itemSelectActive2,'below')
    b_none = gtk.MenuItem("None")
    b_above.show()
    b_below.show()
    b_none.show()
    #below = gtk.MenuItem('below')
    bring = gtk.Menu()
    #Rotate Section---------------------
    rotate = gtk.Menu()
    rotate_sub = gtk.MenuItem('Rotate')
    rotate_sub.show()
    r_clock_w = gtk.MenuItem("Clockwise")
    r_clock_w.connect("activate",rotate_item,item,"Clockwise")
    r_clock_cc = gtk.MenuItem("CounterClockwise")
    r_clock_cc.connect("activate",rotate_item,item,"CounterClockwise")
    r_free = gtk.MenuItem("Free")
    r_free.connect("activate",rotate_item,item,"Free")
    r_clock_w.show()
    r_clock_cc.show()
    r_free.show()
    rotate_sub.set_submenu(rotate)
    rotate.append(r_clock_w)
    rotate.append(r_clock_cc)
    rotate.append(r_free)
    rotate.show()
    #Flip Section------------------------
    flip = gtk.Menu()
    flip_sub = gtk.MenuItem('Flip')
    flip_sub.show()
    f_horz = gtk.MenuItem("Horizontal")
    f_vert = gtk.MenuItem("Vertical")
    f_horz.show()
    f_vert.show()
    flip_sub.set_submenu(flip)
    flip.append(f_horz)
    flip.append(f_vert)
    flip.show()
    
    #b_below.connect("activate", set_item_below,item)
    #group and ungroup
    group = gtk.Menu()
    group_sub = gtk.MenuItem('Item')
    group_sub.show()
    g_group = gtk.MenuItem("Group")
    g_ungroup = gtk.MenuItem("Ungroup")
    g_reset_size = gtk.MenuItem("Reset Group Size")
    g_group.show()
    g_ungroup.show()
    g_reset_size.show()
    group_sub.set_submenu(group)
    group.append(g_group)
    group.append(g_ungroup)
    group.append(g_reset_size)
    group.show()
    if len(global_var.multiSelect)>1:
        g_group.set_sensitive(True)
    else:
        g_group.set_sensitive(False)
    
    if len(global_var.multiSelect)==1:
        if global_var.multiSelect[0].get_n_children() > 0:
            g_ungroup.set_sensitive(True)
        else:
            g_ungroup.set_sensitive(False)
    else:
        g_ungroup.set_sensitive(False)
            
    g_group.connect("activate",set_group,canvas)
    g_ungroup.connect("activate",set_ungroup,canvas)
    g_reset_size.connect("activate",renew_group_size,item) # call def "renew_group_size" on group_item.py
        
    #End of group sun item
    
    bringTo.set_submenu(bring)
    bring.append(b_above)
    bring.append(b_below)
    bring.append(b_none)
    bring.show()
    #above.connect("activate", set_item_above,item)
    delete = gtk.MenuItem('Delete')
    delete.connect("activate", set_item_delete,item)
    
    dynamic = gtk.MenuItem('Dynamic')
    dynamic.connect("activate", show_item_dynamic,item)
    
    property = gtk.MenuItem('Property')
    property.connect("activate", get_item_property,item)
    i.show()
    bringTo.show()
    dynamic.show()
    
    if prop.has_key('dynamic'):
        if len(prop['dynamic'] ) >0 :
            dynamic.set_sensitive(True)
        else:
            dynamic.set_sensitive(False)
        
    #show item Lock 
    lock = gtk.CheckMenuItem('Lock')
    def toggleLock(self,item_all):
        for itemSelect in item_all:
            itemLock = itemSelect.get_data ("itemProp")
            if itemLock['lock'] == False:
                itemLock['lock'] = True
            else:
                itemLock['lock'] = False
            itemSelect.set_data ("itemProp",itemLock)
        clear_selection()

        
    #prop = item.get_data ("itemProp")
    if prop.has_key('lock') == False:
        prop['lock']=False
        item.set_data ("itemProp",prop)
        
    lock.set_active(prop['lock'])
    lock.connect("activate", toggleLock,global_var.multiSelect)
    if global_var.edit_group_mode == True: # IF edit mode is active , lock item is disable
        lock.set_sensitive(False)
    #below.show()
    property.show()
    lock.show()
    delete.show()
    m.append(i)
    m.append(sep1)
    m.append(cut)
    m.append(copy)
    m.append(past)
    m.append(sep2)
    m.append(bringTo)
    m.append(rotate_sub)
    m.append(flip_sub)
    m.append(group_sub)
    m.append(delete)
    m.append(lock)
    m.append(dynamic)
    m.append(property)
    m.popup(None, None, None, event.button, event.time, None)
        
    return True

def popup_None_item_active(event,canvas):
    #-------Copy area-------
    m = gtk.Menu()
    copy = gtk.MenuItem("Copy")
    copy.show()
    copy.set_sensitive(False)
    
    
    cut = gtk.MenuItem("Cut")
    cut.show()
    cut.set_sensitive(False)
    
    past = gtk.MenuItem("Paste")
    past.connect("activate",copy_paste_Item,'paste',canvas)
    past.show()
    
    m.append(cut)
    m.append(copy)
    m.append(past)
    m.popup(None, None, None, event.button, event.time, None)

def edit_group_item(widget,item,canvas):
    #remove on dash group area 
    #-----------------------------------
    #|                                  |
    #|          Item under group        |
    #|                                  |
    #------------|----------------------|
    #            |----> This is dash group item 
    if global_var.edit_item_area_dash is not None:
        global_var.edit_item_area_dash.remove()# remove dash group item 
    edit_group_item_all(item,canvas)
    #print "edite group item"
    
def copy_paste_Item(self,action,canvas):
    
    if action =='cut':
        drawItem.copyItem_byKey()
        nepohmi.deleteSelected()
        global_var.bt['Paste'].set_sensitive(True)
    if action == 'copy':
        drawItem.copyItem_byKey()
    if action == 'paste':
        drawItem.pasteItem_byKey(canvas)

def rotate_item(self,item,option):
    print "rotate option ",option
    print "original item x %s , y %s " % (item.props.x,item.props.y)
    cx = (item.props.x + item.props.width/2)
    cy = (item.props.y + item.props.height/2)
    if option == "CounterClockwise":
        item.rotate(-90,cx,cy)
    if option == "Clockwise":
        item.rotate(90,cx,cy)
    if option == "Free":
        item.rotate(45,cx,cy)
    print "New item      x %s , y %s " % (item.props.x,item.props.y)

def show_item_dynamic(self,item):
    print 'dynamic press'
    showDynamic = displayActionDynamic(item)
    del showDynamic
    

def check_item_raise_below(self,item,event_state):
    ListItemOverlap = getOverlapedAreas(item)
    #print "parent select is ",global_var.parent_active
    typeGrid = '<type \'goocanvas.Grid\'>'
    typeGroup = '<type \'goocanvas.Group\'>'
    if item is not None: # check item is not exist
        if global_var.edit_group_mode == True: 
            item_under_group = []
            n = global_var.edit_item_parent.get_n_children()
            if n > 0:
                for i in range(n):
                    item_under_group.append(global_var.edit_item_parent.get_child(i))
        pre_item = None # temp item for keep on one up / down item
        oneUpDownList = []
        for item_a in ListItemOverlap:
            if event_state in ['raise','below']: # one click to TOP or Buttom
                if str(type(item_a)) != typeGrid and item.get_parent() != item_a and item_a != item :
                    if global_var.edit_group_mode == True: 
                        get_prop = item_a.get_data('itemProp')
                        #if str(type(item_a)) != typeGroup and get_prop is not None :
                        if item_a in item_under_group and get_prop is not None :
                            print "pre above",
                            print item_a
                        #if item.get_parent() == item_a.get_parent:
                            set_item_raise_below(item,item_a,event_state)
                    else:
                        if item_a.get_parent() == item.get_parent(): # check same parent
                            set_item_raise_below(item,item_a,event_state)
            
            if  event_state in ['oneUp','oneDown']:
                if str(type(item_a)) != typeGrid and item.get_parent() != item_a: 
                    if item_a.get_parent() == item.get_parent(): # check same parent
                        oneUpDownList.append(item_a)
                        
        if  event_state == 'oneUp':
            id = oneUpDownList.index(item)
            if id > 0:
                item.raise_(oneUpDownList[id-1])
        if  event_state == 'oneDown':
            id = oneUpDownList.index(item)
            if id < (len(oneUpDownList)-1):
                item.lower(oneUpDownList[id+1])

    return True
                        
def set_item_one_up():
    pass 
    
def set_item_one_down():
    pass
     
def set_item_raise_below(item,item_a,event_state):
    if event_state == 'raise':
        item.raise_(item_a)
    else:
        item.lower(item_a)
    return True
        
def set_group(item,canvas):
    group_item_all(canvas)#call def from group_item.py
    
    
def set_ungroup(item,canvas):
    ungroup_item_all(canvas) # call def from ungroup_item.py
    
#def renew_group_size(data,item):
    #root_parent,item_parent = return_parent_root(item)
    #item.set_simple_transform(0, 0, 0.5, 0)
    #renew_group_size(item,canvas)
    #item.scale(0.5,0.5)
    #pass
    
def set_item_delete(self,item):
    #undo.undoListStore(global_var.undoList,'Delete Item',None,item,None)
    for item_select in global_var.multiSelect:
        item_select.remove()
        
    clear_selection() # clear all  select
    
    global_var.bt['Copy'].set_sensitive(False)
    global_var.bt['Cut'].set_sensitive(False)
    global_var.bt['Delete'].set_sensitive(False)
    
def clear_selection():
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
    
def get_item_property(self,item):
    #print 'select item property'
    selectId = itemPropertySelect(item) #call function from "displayProperty.py"
    
def getOverlapedAreas(area):
        canvas = area.get_canvas ()
        offset = 2
        #print "offset x y ",
        x0,y0 = offset_parent_position(area.get_parent())
        item_position = area.get_simple_transform()
        print "item position overlaps",item_position
        sx = item_position[0]
        sy = item_position[1]
        '''
        start_point = (area.props.x + (x0), area.props.y + (offset+y0))
        end_point = (area.props.x + x0+(area.props.width - offset), area.props.y +y0+ (area.props.height - offset))
        '''
        start_point = (sx + (x0), sy + (offset+y0))
        end_point = (sx + x0+(area.props.width - offset), sy +y0+ (area.props.height - offset))
        bounds = goocanvas.Bounds(*(start_point + end_point))
        print start_point,end_point
        overlaped_items = canvas.get_items_in_area(bounds, True, True, True)
        print len(overlaped_items)
        
        found_bg = None
        for item_over in overlaped_items:
            itemData = item_over.get_data ("itemProp")
            if itemData is not None:
                if itemData['main'] =='Background Rect Item': 
                    found_bg = item_over
                    break
        if found_bg is not None:
            #Remove item background 
            overlaped_items.remove(found_bg)
            
        return overlaped_items
