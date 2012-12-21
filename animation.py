#!/usr/bin/env python
# -*- coding: utf-8 -*-

tag_codition = {'True':None,'False':None,'None':None,'Value Error':None,'More than':0,'Less than':0,'Equal':0}

class animationColor(object):
    
    def __init__(self, name='Defualt', tag = None, color_default = 'red', color2 = 'blue',fill_color = 'red',line_color='black'):
        self.name = name # Set name of tag
        self.tag = tag # tag vulue from OPC data
        self.opc_server_name = None
        self.color_default = color_default # Load item color 1        
        self.color2 = color2 # display item fill color2
        self.color3 = 'black' # display item line color
        self.fill_color = fill_color #change fill color
        self.line_color = line_color
        #Change Color 
        self.chg_fill_color = color2# [tag_codition_list,Default_Value]
        self.chg_line_color = color2 # [tag_codition_list,Default_Value]
        #Change Fill Color State
        self.chg_fill_color_state = True
        self.chg_fill_color_value = None
        #Change Line Color State
        self.chg_line_color_state = True
        self.chg_line_color_value = None
        
class animationPicker(object):
        def __init__(self, name='Defualt', tag = None, type = 'Toggle'):
            self.name = name # Set name of tag
            self.tag = tag # tag vulue from OPC data
            self.opc_server_name = None
            self.cmd_type = type
            self.value = ''
            
class animationFlash(object):
    
    def __init__(self, name='Defualt', tag = None, color_default = 'red', color2 = 'blue',fill_color = 'yellow',refresh_rate = 100):
        self.name = name # Set name of tag
        self.tag = tag # tag vulue from OPC data
        self.opc_server_name = None
        self.color_default = color_default # Load item color 1        
        self.color2 = color2 # display item fill color2
        self.fill_color = fill_color #change fill color
        self.refresh_rate = refresh_rate # Blink rate (millisecond)
        #Change Color 
        self.chg_fill_color = color2# [tag_codition_list,Default_Value]
        #Change Fill Color State
        self.chg_fill_color_state = True
        self.chg_fill_color_value = None
        #Change Line Color State
        #Flag 
        self.flash_value = False
        self.flash_active = False

        
