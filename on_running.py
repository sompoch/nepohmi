
import getopt, string, re, sys
import time
from datetime import datetime
import random
import gobject ,time
import global_var

class update_item():
    def __init__(self):
        pass
        #print '****initial load update item data****'
        
    def update_on_running(self,opc_get_all,canvas):
        
        if global_var.mode_run: # change item property when run mode only
            #print 'ON RUN ADD SERVICE ITEM..'
            for server_name in opc_get_all:
                #print u
                for tag in opc_get_all[server_name]:
                    #print '       --->',tag
                    if global_var.opc_tag_value.has_key(tag):
                        if global_var.opc_tmp_value.has_key(tag) == False:
                            global_var.opc_tmp_value[tag] = global_var.opc_tag_value[tag][0] # create new tag value
                            self.update_item_value(opc_get_all,server_name,tag)
                        #update when tag value change
                        if global_var.opc_tmp_value[tag] != global_var.opc_tag_value[tag][0]:
                            global_var.opc_tmp_value[tag] = global_var.opc_tag_value[tag][0]
                            print 'update value %s is %s' % (tag,global_var.opc_tag_value[tag][0])
                            self.update_item_value(opc_get_all,server_name,tag)
                            
                                        #item.props.fill_color = itemSelect.fill_color
                                        
                    #for w in opc_get_all[u][v]:
                        #print '             |__',w
                        #for x in opc_get_all[u][v][w]:
                        #    print '                     |__',x
            '''for y in list_item:
                for t in list_item[y]:
                    itemData = t.get_data ("itemProp")
                    if itemData.has_key('dynamic'):
                        pointDynamic = itemData['dynamic']
                        if pointDynamic.has_key('Color'):
                            itemSelect = pointDynamic['Color']
                            typeItem =  str(type(itemSelect))
                            if typeItem == '<class \'animation.animationColor\'>':
                                if global_var.opc_tag_value.has_key(itemSelect.tag):
                                    if global_var.opc_tmp_value.has_key(itemSelect.tag):
                                        if global_var.opc_tmp_value[itemSelect.tag] != global_var.opc_tag_value[itemSelect.tag][0]:
                                            global_var.opc_tmp_value[itemSelect.tag] = global_var.opc_tag_value[itemSelect.tag][0]
                                            #Item action
                                            if itemSelect.chg_fill_color_state == global_var.opc_tag_value[itemSelect.tag][0]:
                                                t.props.fill_color = itemSelect.fill_color
                                            else:
                                                t.props.fill_color = itemSelect.color1
                                    else:
                                        global_var.opc_tmp_value[itemSelect.tag] = global_var.opc_tag_value[itemSelect.tag][0]
            '''

        return global_var.mode_run
        #opcService(opc_server_name,tag,opt).start()
    
    def item_pick_on_run(self,item):
        print 'Item press on run'
        
    def update_item_value(self,opc_get_all,server_name,tag):
        for item in opc_get_all[server_name][tag]:
            #print 'type of item is ',type(item)
            for animateObj in opc_get_all[server_name][tag][item]:
                itemData = item.get_data ("itemProp")
                pointDynamic = itemData['dynamic']
                if animateObj == '<class \'animation.animationColor\'>':
                    itemSelect = pointDynamic['Color']
                    if itemSelect.chg_fill_color_state == global_var.opc_tag_value[itemSelect.tag][0]:
                        item.props.fill_color = itemSelect.fill_color
                    else:
                        item.props.fill_color = itemSelect.color1
                        
                if animateObj == '<class \'animation.animationFlash\'>':
                    itemSelect = pointDynamic['Flash']
                    repeate = itemSelect.refresh_rate
                    #startFlash = False
                    #global startFlash
                    #global flash_value
                    #flash_value = True
                    
                    if repeate<50 :
                            print 'Flash animation repeate time is less than 50 ms and reset to defualt [50] ms'
                            repeat = 50
                        #else:
                        #    repeate = 100 # default va;ue if incorrect data
                    timer = gobject.timeout_add (repeate, self.flash_item,item,itemSelect)
                    
                    if itemSelect.chg_fill_color_state == global_var.opc_tag_value[itemSelect.tag][0]:
                        itemSelect.flash_active = True
                        print 'Flash active'
                    else:
                        itemSelect.flash_active = False
                        print 'Flash deactive'
                        item.props.fill_color = itemSelect.color_default
                    
                        #if refresh_rate.isdigit() :
                            #repeate = int(itemSelect.refresh_rate)
                        
                        
        return True
    
    def flash_item(self,item,itemSelect):
        #global startFlash
        #global flash_value

        if itemSelect.flash_value == True:# toggle value
            itemSelect.flash_value = False
            item.props.fill_color = itemSelect.fill_color
        else:
        #if itemSelect.flash_value == False:
            itemSelect.flash_value = True
            item.props.fill_color = itemSelect.color_default
            
        if global_var.mode_run == False or itemSelect.flash_active == False :
            item.props.fill_color = itemSelect.color_default
            
        #print 'Flash active'
        return global_var.mode_run and itemSelect.flash_active
      
        
        
        
