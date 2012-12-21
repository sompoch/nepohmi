#!/usr/bin/env python
# -*- coding: utf-8 -*-
import global_var
import goocanvas
import os
import drawItem 

def group_item_all(canvas):
    print "Group item in progress..."
    for t in global_var.multiSelect:
        for j in range(8):
            global_var.itemSelect8Cursor[t][j].remove()
    
    print "*******add group item area************",
    print "Item  active is ",global_var.itemSelectActive
    if global_var.itemSelectActive is not None:# skip when item not select
    #if len(global_var.multiSelect) < 1:
        parent_of_item = global_var.itemSelectActive.get_parent()
        root_of_item = parent_of_item.get_parent()
        #group_root,parent = return_parent_root(item)
        
        #print "root of item is ",root_of_item
        #if root_of_item == None:
        if global_var.edit_group_mode == False: 
            parent1 = create_group_item(canvas,None) # call create group
        else:
            parent1 = create_group_item(canvas,global_var.parent_active)
        
        sxp1,syp1,scale_p1,degree = parent1.get_simple_transform()
        global_var.multiSelect.reverse()
        for v in  global_var.multiSelect: # add group on item 
            #Clear lock item before add  to group 
            itemProperty = v.get_data ('itemProp')
            if itemProperty['lock'] == True:
                itemProperty['lock'] = False # Clear status lock
                v.set_data('itemProp',itemProperty)
                print "Found Lock item ",v
            parent_item = v.get_parent()
            child_num = parent_item.find_child(v)
            parent_item.remove_child(child_num)
            parent1.add_child(v, -1)
            #v.props.x = v.props.x -parent1.props.x#+5
            #v.props.y = v.props.y - parent1.props.y#+5
            sx,sy,scale_,degree = v.get_simple_transform()
            new_sx = sx -sxp1 # offset transform 
            new_sy = sy - syp1 # offset transform 
            v.set_simple_transform(new_sx,new_sy,scale_p1,degree) # update new position on group
        
        
        
        lenGroup = len(global_var.multiSelect)
        #print 'old group item select %s' %  lenGroup
        if lenGroup>0:
            del global_var.multiSelect[0:(lenGroup-1)]
        else:
            print "use item group root"
    else:
        if global_var.edit_group_mode == False and len(global_var.multiSelect)>0:
            parent1 = create_group_item(canvas,None) 
            sxp1,syp1,scale_p1,degree = parent1.get_simple_transform()
            global_var.multiSelect.reverse()
            for v in  global_var.multiSelect: # add group on item 
                #Clear lock item before add  to group 
                itemProperty = v.get_data ('itemProp')
                if itemProperty['lock'] == True:
                    itemProperty['lock'] = False # Clear status lock
                    v.set_data('itemProp',itemProperty)
                    print "Found Lock item ",v
                
                parent_item = v.get_parent()
                child_num = parent_item.find_child(v)
                parent_item.remove_child(child_num)
                parent1.add_child(v, -1)
                #v.props.x = v.props.x -parent1.props.x#+5
                #v.props.y = v.props.y - parent1.props.y#+5
                sx,sy,scale_,degree = v.get_simple_transform()
                new_sx = sx -sxp1 # offset transform 
                new_sy = sy - syp1 # offset transform 
                v.set_simple_transform(new_sx,new_sy,scale_p1,degree) # update new position on group
                #else:
                #    print "Found Lock item ",v
        
        
    print "*******end of goup item*************"
    
    #global_var.parent_active = None # reset parent item 
    return True

def on_enter_notify(item, target, event,canvas):
    print "Inner item group is " , item 
    
def create_group_item(canvas,parent_root):
    #print "use root item "
    if parent_root == None:
        root = canvas.get_root_item()
    else:
        root = parent_root
    group1 = goocanvas.Group(parent = root) # creat group on canvas
    scale = canvas.get_scale() # item get scale
    
    sx,sy,width,height = find_width_height_group(global_var.multiSelect,None)

    group1.connect("button-press-event", on_button_press_group)
    
    group1.props.x = 0#x#-10
    group1.props.y = 0 #y#-10
    group1.props.width = width# + 20
    group1.props.height = height# + 20
    group1.set_simple_transform(sx,sy,1,0)
    #print "Group parent size is      x = %s , y = %s ," % (group1.props.x,group1.props.y),
    #print "w= %s , h = %s " % (group1.props.width,group1.props.height)

    prop={}
    prop['color'] = "red"
    prop['x'] = 0#group1.props.x*scale
    prop['y'] =0#group1.props.y*scale
    prop['transform_x'] = sx
    prop['transform_y'] = sy
    prop['width'] = group1.props.width*scale
    prop['height'] =  group1.props.height*scale
    prop['stroke_pattern'] = None
    prop['stroke_color'] = "black"
    prop['line_width'] = 1
    prop['can_focus'] = False
    prop['name'] = 'group Item'
    prop['lock']= False
    prop['main'] = 'group Item'
    prop['layer'] = 'Primary'
    prop['dynamic'] = {}
    #property['name'] = 'groupItem'
    group1.set_data ("itemProp", prop)
    
    return group1

def find_width_height_group (list_item,item_parent):
    # find min max item on list support 
    itemUnderGroup =[]
    
    if item_parent is not None: #option(None,Parent) 
        n = item_parent.get_n_children()
        for i in range(n):
            itemUnderGroup.append(item_parent.get_child(i))
            
        
        sx,sy,scale_,degree = item_parent.get_simple_transform()
        offset_x = sx#item_parent.props.x
        offset_y = sy#item_parent.props.y
        #print "group item offset position %s %s " % (offset_x,offset_y)
        
    else: #(List_item,None)
        offset_x = 0
        offset_y = 0
        itemUnderGroup = list_item
        
    find_min_x =[]
    find_min_y =[]
    find_max_w =[]
    find_max_h =[]
    
    for v in  itemUnderGroup: # add group on item 
        #print "item position x ", v.props.x
        # find width , height of group 
        get_prop = v.get_data('itemProp')
        if get_prop.has_key('main') and get_prop['main'] != 'cursor Item': # check valid item
            #print get_prop['main'],
            sx,sy,scale_,degree = v.get_simple_transform()
            w = sx + (v.props.width)+(v.props.line_width/2) 
            h = sy + (v.props.height)+(v.props.line_width/2) 
            find_min_x.append(sx+offset_x-(v.props.line_width/2))
            find_min_y.append(sy+offset_y-(v.props.line_width/2))
            find_max_w.append(w)
            find_max_h.append(h)
            #print ' item           x = %s , y = %s , w= %s , h = %s '  % (sx+offset_x,sy+offset_y,w,h)
            
    x= min(find_min_x)#-(v.props.line_width/2)
    y = min(find_min_y)#-(v.props.line_width/2)
    width = max(find_max_w)-x
    height = max(find_max_h)-y

    #print '----------------------------------------------------------------------------------'
    #print 'Min max item              x = %s , y = %s , w= %s , h = %s '  % (x,y,width+x,height+y)
    
    return x,y,width,height


def find_new_group_size(item_parent):
    #Found new group size this not same of def "find_width_height_group".
    #It's not support list item but it can found item under  parent only. 
    #This function  to calcultate minimum position item x,y and maximum position x,y of group.
    #Return new group position [x,y,width,height] type is tuple.
    #Update 10-04-2011
    
    if item_parent is not None:
        itemUnderGroup =[]
        n = item_parent.get_n_children()
        for i in range(n):
            itemUnderGroup.append(item_parent.get_child(i))
            
        sx,sy,scale_,degree = item_parent.get_simple_transform()
        offset_x = sx#item_parent.props.x
        offset_y = sy#item_parent.props.y
        #print "group item offset position %s %s " % (offset_x,offset_y)
        
        find_min_x =[]
        find_min_y =[]
        find_max_w =[]
        find_max_h =[]
      
        #print '----debug def : find_new_group_size------'
        #print 'print value under group is ..',len(itemUnderGroup)
        for v in  itemUnderGroup: # add group on item 
            get_prop = v.get_data('itemProp')
            if get_prop is not None:
                if get_prop.has_key('main'):
                    if (get_prop['main'] != 'cursor Item') or (get_prop['main'] != 'Grid Item'):
                        #print get_prop['main'],
                        if (get_prop['main'] == 'cursor Item'):
                            sx = v.props.x
                            sy = v.props.y
                        else:
                            sx,sy,scale_,degree = v.get_simple_transform()

                        w = sx + (v.props.width  +(v.props.line_width/2)) 
                        h = sy + (v.props.height +(v.props.line_width/2)) 
                        find_min_x.append(sx+offset_x-(v.props.line_width/2))
                        find_min_y.append(sy+offset_y-(v.props.line_width/2))
                        find_max_w.append(w+offset_x)
                        find_max_h.append(h+offset_y)
                        #print " end of debug def : find_new_group_size "
                        #print 'item           x = %s , y = %s , w= %s , h = %s '  % (sx+offset_x,sy+offset_y,w+offset_x,h+offset_y)
                    
        x = min(find_min_x)-10#(10-(v.props.line_width/2))
        y = min(find_min_y)-10#(10-(v.props.line_width/2))
        width = max(find_max_w)
        height = max(find_max_h)
        #print '-------------------Report New Group Size-------------------------------'
        #print 'Min max item              x = %s , y = %s , w= %s , h = %s '  % (x,y,width,height)
        return x,y,width,height

def on_leave_notify(item, target, event,canvas):
    print "Outer item group is ", item
    
def ungroup_item_all(canvas):
    print "Ungroup item now"
    
    if len(global_var.multiSelect)==1:
        if global_var.multiSelect[0].get_n_children() > 0:
            group_root,parent = return_parent_root(global_var.multiSelect[0])#call group_item.py -->retrun_parent_root to check root, parent item
            item = global_var.multiSelect[0]
            print "item select item group is ",item
            print "Ungroup to major root"
            chn = item.get_n_children()
            list_item =[]
            for i in range(chn):
                print "     +----",item.get_child(i)
                list_item.append(item.get_child(i))
            #read current position group item
            #offset_x = item.props.x
            #offset_y = item.props.y
            
            sxp1,syp1,scale_p1,degree_p1 = item.get_simple_transform()
            offset_x = sxp1
            offset_y = syp1
            
            for j in list_item:
                child_num = item.find_child(j)
                item.remove_child(child_num)
                parent.add_child(j, -1) # remove from parent 
                sx,sy,scale_,degree = j.get_simple_transform()
                new_sx = sx + offset_x #restore defualt position item
                new_sy  = sy + offset_y #restore defualt position item
                j.set_simple_transform(new_sx,new_sy,scale_,degree)
                
               
            #clear all selection area

            for t in global_var.multiSelect:
                for j in range(8):
                    global_var.itemSelect8Cursor[t][j].remove()
            item.remove() # remove group item
            del global_var.multiSelect[0] # delete temp data 
            
            
            return True
                

    
def return_parent_root(item):
    if item is not None:
        parent = item.get_parent()
        if parent is not None:
            parent_root = parent.get_parent()
        else:
            parent_root = None
        return parent_root,parent # this is define to return perent and root 
    else:
        return None,None

    
def on_button_press_group(item,target, event):
    print "Group press !!!!"
    
def refresh_new_group_size():
    
    x0,y0,w,h = find_width_height_group(None,global_var.edit_item_parent)
    # Check new posiotn update over group size 
    if w != global_var.edit_width_change or h != global_var.edit_height_change:
        global_var.edit_width_change = w
        global_var.edit_height_change = h
        print "update change new group size now! ",global_var.edit_item_parent
    
        #global_var.edit_init_min_x = x0-20 # offset value to cover item under group on x axis
        #global_var.edit_init_min_y = y0-20 # offset value to cover item under group on y axis
        n = global_var.edit_item_parent.get_n_children()
        if n > 0:
            # TODO : ปรับขนาดของ group ใน ช่วงที่เข้าสู่ edit
           
            print "refresh group size "
            # TODO : Big problem whem resize group
            #renew_group_size(None,global_var.edit_item_parent)
            renew_group_size_on_move(None,global_var.edit_item_parent)
            # Set new dash line selection area 
            '''sx,sy,scale_,degree = global_var.edit_item_parent.get_simple_transform()
            global_var.edit_item_area_dash.props.x = sx-10#global_var.edit_item_parent.props.x-10
            global_var.edit_item_area_dash.props.y = sy-10#global_var.edit_item_parent.props.y-10
            global_var.edit_item_area_dash.props.width = global_var.edit_item_parent.props.width +20#(width-x)+10# add number 10 because want to see selection cursor
            global_var.edit_item_area_dash.props.height = global_var.edit_item_parent.props.height+20#(height-y)+10# add number 10 because want to see selection cursor
            '''
 
        #Update new offset size  for reference when adjust item under group [group_edit_mode == True]
        global_var.edit_offset_xy = offset_parent_position(global_var.edit_item_parent)
        
        global_var.edit_item_area_dash.props.x = global_var.edit_offset_xy[0]-10
        global_var.edit_item_area_dash.props.y = global_var.edit_offset_xy[1]-10
        global_var.edit_item_area_dash.props.width = global_var.edit_item_parent.props.width+20
        global_var.edit_item_area_dash.props.height = global_var.edit_item_parent.props.height+20
  
    return True

def update_drag_group_size ():
    getUpperParent = global_var.edit_item_parent.get_parent()
    cnt= 0 
    while getUpperParent != None:
        #print "item in get upper parent ",getUpperParent
        cnt +=1 
        print "cnt item ",cnt
        #find_new_group_size(getUpperParent)

        if getUpperParent is not None and getUpperParent.get_parent() is not None :
            itemUnderGroup =[]
            n = getUpperParent.get_n_children()
            for i in range(n):
                itemUnderGroup.append(getUpperParent.get_child(i))
            offset_x = getUpperParent.props.x
            offset_y = getUpperParent.props.y
            #print "group item offset position %s %s " % (offset_x,offset_y)
            
            find_min_x =[]
            find_min_y =[]
            find_max_w =[]
            find_max_h =[]
            print '|------debug def : find_new_group_size------|'
            #print 'Print value under group is ..'
            for v in  itemUnderGroup: # add group on item 
                get_prop = v.get_data('itemProp')
                if get_prop is not None:
                    if get_prop.has_key('main'):
                        if get_prop['main'] != 'cursor Item' and get_prop['main'] != 'Grid Item' : # check valid item
                            #print get_prop['main'],
                            #print v,get_prop['main']
                            w = v.props.x+offset_x+v.props.width 
                            h = v.props.y+offset_y+v.props.height 
                            find_min_x.append(v.props.x+offset_x)
                            find_min_y.append(v.props.y+offset_y)
                            find_max_w.append(w)
                            find_max_h.append(h)
            #print "End of debug def : find_new_group_size "
                        #print ' item           x = %s , y = %s , w= %s , h = %s '  % (v.props.x+offset_x,v.props.y+offset_y,w,h)
        getUpperParent = getUpperParent.get_parent()
            #x= min(find_min_x)-10
            #y = min(find_min_y)-10
            #width = max(find_max_w)
            #height = max(find_max_h)
        

def upper_group_edit_item (item1,parent1,canvas):
    #root_parent,item_parent = return_parent_root(item)
    #update new dash line 
    print "upper group item..."
    if parent1 is not None:
        up_parent = item1.get_parent()
        up_root_parent = parent1.get_parent()
        if up_root_parent == None:
            global_var.parent_active = None 
            global_var.edit_group_mode = False 
        else:
            
            #item_dash =  create_dash_line_group(up_parent,up_root_parent,canvas) # old create  dash line area 
            #global_var.edit_item_area_dash = item_dash # update item dash line to global varible
            
            property = {}
            property['x'] = global_var.edit_offset_xy[0]
            property['y'] = global_var.edit_offset_xy[1]
            item_dash =  create_dash_line_group(property,None,global_var.edit_item_parent,canvas)
            global_var.edit_item_area_dash = item_dash
            
            global_var.edit_item_parent = up_parent # update item parent to global varible 
            # keep initial mix x,y  and  search size of group item 

            global_var.edit_init_min_x,global_var.edit_init_min_y,w,h = find_width_height_group(None,up_parent)
            global_var.edit_init_min_x -= 20 # offset value to cover item under group on x axis
            global_var.edit_init_min_y -= 20 # offset value to cover item under group on y axis
            #global_var.parent_active = up_parent
    else:
        global_var.parent_active = None 
        global_var.edit_group_mode = False 
        

    #TODO : renew_group_size
def renew_group_size(widget,group_item):
    
    # Expand size group about 10px for cover adjust cursor
    '''if global_var.edit_group_mode == True:
        ofset_wh = 10/global_var.canvas_scale
        ofset_xy = 0-(10/global_var.canvas_scale)
    else:'''
    ofset_wh = 0
    ofset_xy = 10/global_var.canvas_scale
        
    n = group_item.get_n_children()
    
    if n > 0:
        
        x,y,width,height = find_new_group_size(group_item)# return new size of all item
        #print 'Min max item              x = %s , y = %s , w= %s , h = %s '  % (x,y,width,height)
        x += ofset_xy
        y += ofset_xy
        #print  "x = %s y =%s width = %s height = %s " % (x,y,width,height)
        sx,sy,scale_,degree = group_item.get_simple_transform()
        diff_x = x-sx#group_item.props.x
        diff_y = y-sy#group_item.props.y
        diff_width  = (width-x)-group_item.props.width
        diff_height = (height-y)-group_item.props.height
        #print  "diff x = %s diff y =%s diff_width = %s diff height = %s " % (diff_x,diff_y,diff_width,diff_height)
        if diff_x != 0 or diff_y != 0 or diff_width !=0 or diff_height !=0 :
            
            #Update new group parent first
            sx2,sy2,scale_2,degree2 = group_item.get_simple_transform()
            sx2 +=diff_x 
            sy2 +=diff_y 
            #group_item.props.x +=diff_x
            #group_item.props.y +=diff_y
            group_item.set_simple_transform(sx2,sy2,scale_2,degree2)
            group_item.props.width = (width-x)+ofset_wh
            group_item.props.height = (height-y)+ofset_wh
            
            #Update positon in children second
            for i in range(n):                
                #get_prop = group_item.get_child(i).get_data('itemProp')
                #if get_prop is not None:
                    #if get_prop.has_key('main'):
                        #if get_prop['main'] != 'cursor Item':
                            #print get_prop['main'],
                            #print "]Children item before adj new group position ",global_var.edit_item_parent.get_child(i)
                sx3,sy3,scale_3,degree3 = group_item.get_child(i).get_simple_transform()
                #group_item.get_child(i).props.x -= diff_x
                #group_item.get_child(i).props.y -= diff_y
                sx3 -=diff_x 
                sy3 -=diff_y 
                group_item.get_child(i).set_simple_transform(sx3,sy3,scale_3,degree3)

    return True

def renew_group_size_on_move(widget,group_item):
    print "renew group size on move"
    n = group_item.get_n_children()
    if n > 0:
        x,y,width,height = find_new_group_size(group_item)
        print 'Min max item              x = %s , y = %s , w= %s , h = %s '  % (x,y,width,height)
        x += 10#ofset_xy
        y += 10#ofset_xy
        #print  "x = %s y =%s width = %s height = %s " % (x,y,width,height)
        sx,sy,scale_,degree = group_item.get_simple_transform()
        diff_x = x-sx#group_item.props.x
        diff_y = y-sy#group_item.props.y
        diff_width  = (width-x)-group_item.props.width
        diff_height = (height-y)-group_item.props.height
        #print  "diff x = %s diff y =%s diff_width = %s diff height = %s " % (diff_x,diff_y,diff_width,diff_height)
        
        if diff_x != 0 or diff_y != 0 or diff_width !=0 or diff_height !=0 :
            
            #Update new group parent first
            sx2,sy2,scale_2,degree2 = group_item.get_simple_transform()
            sx2 +=diff_x 
            sy2 +=diff_y 
            #group_item.props.x +=diff_x
            #group_item.props.y +=diff_y
            group_item.set_simple_transform(sx2,sy2,scale_2,degree2)
            group_item.props.width = (width-x)
            group_item.props.height = (height-y)
            if diff_x != 0 or diff_y != 0:
                #Update positon in children second
                for i in range(n):                
                    get_prop = group_item.get_child(i).get_data('itemProp')
                    if get_prop is not None:
                        if get_prop.has_key('main'):
                            if get_prop['main'] != 'cursor Item':
                            #    pass
                                #print get_prop['main'],
                                #print "]Children item before adj new group position ",global_var.edit_item_parent.get_child(i)
                            #else:
                                sx3,sy3,scale_3,degree3 = group_item.get_child(i).get_simple_transform()
                                #group_item.get_child(i).props.x -= diff_x
                                #group_item.get_child(i).props.y -= diff_y
                                sx3 -=diff_x 
                                sy3 -=diff_y 
                                group_item.get_child(i).set_simple_transform(sx3,sy3,scale_3,degree3)
                                if group_item.get_child(i) in global_var.multiSelect:
                                    drawItem.update_new_round_item(group_item.get_child(i),global_var.canvas_scale)
            
    
'''
def temp_create_dash_line_group (item_parent,root_parent,canvas):
    get_scale = canvas.get_scale()
    #pattern = create_stipple ("cadetblue")
    get_scale = 1
    property = {}
    sx,sy,scale_,degree = item_parent.get_simple_transform()
    property['x'] = sx#(item_parent.props.x - 10)/get_scale
    property['y'] = sy#(item_parent.props.y - 10)/get_scale
    property['width'] = (item_parent.props.width )/get_scale#(item_parent.props.width + 20)/get_scale
    property['height'] = (item_parent.props.height )/get_scale#(item_parent.props.height + 20)/get_scale
    property['color'] = None
    property['main'] = 'dash line selection'
    property['stroke_color'] = '#769998'
    property['line_width'] = 2#/get_scale
    
    if root_parent == None:
        root_parent = canvas.get_root_item ()
        
    # Create dash line of group     
    item = goocanvas.Rect (parent = root_parent,
                               x = property['x'],#int
                               y = property['y'],#int
                               width = property['width'],#int
                               height = property['height'],#int
                               radius_x = 5/get_scale,
                               radius_y = 5/get_scale,
                               #fill_pattern = pattern,
                               #stroke_pattern =  property['stroke_pattern'],# boolean
                               #fill_color = property['color'],# string
                               stroke_color=property['stroke_color'],# string
                               line_dash=goocanvas.LineDash([3.0, 3.0]),
                               line_width = property['line_width'])#, # int
    return item 

'''

def create_dash_line_group (property ,root_parent,item_parent,canvas):
    get_scale = canvas.get_scale()
    #pattern = create_stipple ("cadetblue")
    get_scale = 1
    
    
    property['width'] = (item_parent.props.width )/get_scale#(item_parent.props.width + 20)/get_scale
    property['height'] = (item_parent.props.height )/get_scale#(item_parent.props.height + 20)/get_scale
    property['color'] = None
    property['main'] = 'dash line selection2'
    property['stroke_color'] ='#769998'
    property['line_width'] = 2#/get_scale
    
    if root_parent == None:
        root_parent = canvas.get_root_item ()
        
    # Create dash line of group     
    item = goocanvas.Rect (parent = root_parent,
                               x = property['x'],#int
                               y = property['y'],#int
                               width = property['width'],#int
                               height = property['height'],#int
                               radius_x = 5/get_scale,
                               radius_y = 5/get_scale,
                               #fill_pattern = pattern,
                               #stroke_pattern =  property['stroke_pattern'],# boolean
                               #fill_color = property['color'],# string
                               stroke_color=property['stroke_color'],# string
                               line_dash=goocanvas.LineDash([3.0, 3.0]),
                               line_width = property['line_width'])#, # int
    return item 

def edit_group_item_all(item,canvas):
    
    root_,parent = return_parent_root(item)
    tmp_root = root_
    tmp_parent = parent
    
    #Initial parent setup if None and edit mode is False 
    #It's upper canvas root item 
    item_selected = None
    print "edit group item all"
    if global_var.edit_group_mode == True:
        item_selected = global_var.edit_item_parent # update current on root parent in group edit mode 
    #found item util equal current root parent item 
    while root_ != item_selected:
        tmp_root = root_
        tmp_parent = parent
        root_,parent = return_parent_root(parent)
        
    root_ = tmp_root # update new root of item 
    parent = tmp_parent # update new parent of item 
    
    
    #Push current item edit to data array 
    #global_var.edit_group_array.append(parent)
    
    #root_,parent = return_parent_root(item)
    
    #item_dash =  create_dash_line_group(parent,root_,canvas)
    print "edit mode item is [",parent
    print "]"
    #global_var.edit_item_area_dash = item_dash # update item dash line to global varible
    global_var.edit_item_parent = parent # update item parent to global varible 
    global_var.edit_group_mode = True # set edit mode
    # keep initial mix x,y  and  search size of group item 
    global_var.edit_init_min_x,global_var.edit_init_min_y,w,h = find_width_height_group(None,global_var.edit_item_parent)
    global_var.edit_init_min_x -= 20 # offset value to cover item under group on x axis
    global_var.edit_init_min_y -= 20 # offset value to cover item under group on y axis
    global_var.edit_offset_xy = offset_parent_position(parent)
    
    property = {}
    property['x'] = global_var.edit_offset_xy[0]
    property['y'] = global_var.edit_offset_xy[1]
    item_dash =  create_dash_line_group(property,None,global_var.edit_item_parent,canvas)
    global_var.edit_item_area_dash = item_dash
    
    
def offset_parent_position(parent_edit):
    x0 = 0
    y0 = 0
    while parent_edit.get_parent() is not None:#.get_parent()
        sx,sy,scale_,degree = parent_edit.get_simple_transform()
        x0 += sx#parent_edit.props.x
        y0 += sy#parent_edit.props.y
        parent_edit = parent_edit.get_parent()
        renew_group_size(None,parent_edit)# set real size group
        
        print "\nOffset value on parent position x= %s , y = %s" % (x0,y0)
    return x0,y0
   
    