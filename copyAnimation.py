import os
from animation import *

class copyItemProp():
    def __init__(self):
        print 'start copy item animation property'
        #typeAnimate = type(parentItemAnimate)
        #if typeAnimate == '<class \'animation.animationFlash\'>':
        #    self.animateFlash(newItemAnimate,parentItemAnimate)
            
    def listAnimate(self,parentItemAnimate):
        typeAnimate = str(type(parentItemAnimate))#check animation type
        if typeAnimate == '<class \'animation.animationFlash\'>':
            return self.copyAnimateFlash(parentItemAnimate)
        if typeAnimate == '<class \'animation.animationColor\'>':
            return self.copyAnimateColor(parentItemAnimate)
        if typeAnimate == '<class \'animation.animationPicker\'>':
            return self.copyAnimatePicker(parentItemAnimate)
        
    def copyAnimateFlash(self,parentItemAnimate):
        newItemAnimate = animationFlash(name = parentItemAnimate.name,
                                        tag = parentItemAnimate.tag,
                                        fill_color = parentItemAnimate.fill_color,
                                        refresh_rate = parentItemAnimate.refresh_rate)
                                        
                                        # millisecond to refresh Bilnk
        newItemAnimate.opc_server_name = parentItemAnimate.opc_server_name
        newItemAnimate.color_default = parentItemAnimate.color_default # Load item color 1        
        newItemAnimate.color2 = parentItemAnimate.color2 # display item fill color2
        #newItemAnimate.fill_color = parentItemAnimate.fill_color #change fill color
        newItemAnimate.refresh_rate = parentItemAnimate.refresh_rate # Blink rate (millisecond)
        #Change Color 
        newItemAnimate.chg_fill_color = parentItemAnimate.color2# [tag_codition_list,Default_Value]
        #Change Fill Color State
        newItemAnimate.chg_fill_color_state = parentItemAnimate.chg_fill_color_state
        newItemAnimate.chg_fill_color_value = parentItemAnimate.chg_fill_color_value
        #Change Line Color State
        #Flag 
        newItemAnimate.flash_value = parentItemAnimate.flash_value
        newItemAnimate.flash_active = parentItemAnimate.flash_active

            #print 'type of animation :',parentItemAnimate
        #print 'Copy animation is ',newItemAnimate
        return newItemAnimate
    
    def copyAnimateColor(self,parentItemAnimate):
        newItemAnimate = animationColor(name = parentItemAnimate.name,
                                        tag = parentItemAnimate.tag)
                                        

        newItemAnimate.opc_server_name = parentItemAnimate.opc_server_name
        newItemAnimate.color_default = parentItemAnimate.color_default # Load item color 1        
        newItemAnimate.color2 = parentItemAnimate.color2 # display item fill color2
        newItemAnimate.color3 = parentItemAnimate.color3 # display item line color
        newItemAnimate.fill_color = parentItemAnimate.fill_color #change fill color
        newItemAnimate.line_color = parentItemAnimate.line_color
        #Change Color 
        newItemAnimate.chg_fill_color = parentItemAnimate.chg_fill_color# [tag_codition_list,Default_Value]
        newItemAnimate.chg_line_color = parentItemAnimate.chg_line_color# [tag_codition_list,Default_Value]
        #Change Fill Color State
        newItemAnimate.chg_fill_color_state = parentItemAnimate.chg_fill_color_state
        newItemAnimate.chg_fill_color_value = parentItemAnimate.chg_fill_color_value
        #Change Line Color State
        newItemAnimate.chg_line_color_state = parentItemAnimate.chg_line_color_state
        newItemAnimate.chg_line_color_value = parentItemAnimate.chg_line_color_value
        
        return newItemAnimate
    
    def copyAnimatePicker(self,parentItemAnimate):
        newItemAnimate = animationPicker(name = parentItemAnimate.name,
                                        tag = parentItemAnimate.tag)
        newItemAnimate.opc_server_name = parentItemAnimate.opc_server_name
        newItemAnimate.cmd_type = parentItemAnimate.cmd_type
        newItemAnimate.value = parentItemAnimate.value
        
        return newItemAnimate
        
        