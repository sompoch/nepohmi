#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import gtk
import goocanvas
pan_select = False
cmd_draw = 0
# cmd = command to draw when 
# 0 = Selection Mode
# 1= Creat Rectangle 
# 2 = CreateEllipse
# 3 = CreateCurve
# 4 = CreatePoly
# 5 = line
# 6 = text
# 7 = Image insert
# 8 = Pan
statusbar1 = gtk.Statusbar()
itemSelectName = ''

# define Canvas and event global varible 
itemSelectActive = None # Current select item
itemSelectActive2 = None #Current select item use on above / below click item 
multiSelect = [] #List of select 
copyBuffer = []
multiBoxMoveSelect = []
itemSelect8Cursor= {} # group of selected the arrow cursor
item_press = False # item key press status
mouse_over_item = False # item mouse over status
mouse_over_item_adj = False
button_press = False
move_action = False
move_adj_action = False # action resize item if True it's will be not clear adj cursor
item_adj = None
canvas_scale = 1 # get canvas scale 
outter = False

#------Group edit------------
edit_item_area_dash = None # keep edit area
edit_item_area_dash2 = None
edit_item_parent = None # keep edit parent item for dash line
edit_group_mode = False #status edit group item 
edit_init_min_x = 0
edit_init_min_y = 0
edit_group_array = []
edit_width_change = 0
edit_height_change =0
edit_offset_xy = None # Type tuple

parent_active = None  # set/get root parent item active 

#The global data on aplication run.stop.pause
menu_run = None
menu_stop = None
menu_pause = None

item_active_h0 = 0


comboboxZoom = gtk.combo_box_new_text() # Combo Percent Zoom
undoList = [['','','','']]
index_select_undo = 0
clipboard = []
sel_item = False
bt = {} # Button on toolbar TOP
bt_left = {} # Button on toolbar LEFT
image_import_default_path = '/home/sompoch/Pictures'
current_doc = None
win = None

image_store = {}
image_use = {}
sel_area = None
sel_press = False
select_cursor = {}
box_select = None
adj_box_press = False
grid = {'show':False,'grid':None}
x1 = 100
y1 = 100
INDEX_CURSOR = 0
full_screen = False
main_menu_toggle = False
mode_run = False
mypalette = None
toolBarTop = None
toolBarButtom = None
opc_server_name = None # get OPC SERVER Name from opcBrower.py 
opc_tag_value ={} # read opc data & value from opc server
opc_tmp_value ={} 
item_signal ={}
list_item_obj = [] # list of item when item have dynamic property , use on running mode.
item_dynamic = []

key_control_press = False # use to copy item 
key_shift_press = False # use to select by manaul 

dialogProperty = None # this dialog perperty hide/show
dialogItemValue = {}
dialogWidget = {} #Keep all widget in dialog property for share another class :
dialogOPCbrowe = None

dispProp = {'sameDisp':False,'cvTop':0,'cvLeft':0,'cvWidth':1024,'cvHeight':768,'cvSizeWidth':500,'cvSizeHeight':500}
offset_hsize = 125
graphic_default_setting = {'box_color':'#00AD8C','last_doct':[]}
graphic_setting = None
win_state = None

#OPC Connect 
option = None
opc_value = None
select_server_opc=[] # select opc server



color_bar = [['#8C0000','#9D0000','#AE0000','#BF0000','#D00000','#E10000','#FF0000'],#Red
    ['#FF3C00','#FF5800','#FF6900','#FF7A00','#FF8B00','#FF9C00','#FFAD00'],#Soft Red
    ['#FFFF3C','#FFFF58','#FFFF69','#FFFF7A','#FFFF8B','#FFFF9C','#FFFFAD'],#Soft Yellow
    ['#FF7D3C','#FF7D58','#FF7D69','#FF7D7A','#FF7D8B','#FF7D9C','#FF7DAD'],#Soft Pink
    ['#008C00','#009D00','#00AE00','#00BF00','#00D000','#00E100','#00FF00'],#Green
    ['#7DFF3C','#7DFF58','#7DFF69','#7DFF7A','#7DFF8B','#7DFF9C','#7DFFAD'],#Soft green
    ['#00008C','#00009D','#0000AE','#0000BF','#0000D0','#0000E1','#0000FF'],#Blue
    ['#003C8C','#00588C','#00698C','#007A8C','#008B8C','#009C8C','#00AD8C'],#Soft blue
    ['#3EB59F','#63C5B3','#7FD4C4','#9AD9CE','#B8E5DD','#D5ECE8','#E9EBEB'],#Soft green2 
    ['#3C7DFF','#587DFF','#697DFF','#7A7DFF','#8B7DFF','#9C7DFF','#AD7DFF'],#Soft violet
    ['#000000','#3C3C3C','#585858','#696969','#7A7A7A','#8B8B8B','#9C9C9C'],#Black--Gray
    ['#ADADAD','#BFBFBF','#CFCFCF','#E0E0E0','#F1F1F1','#F8F8F8','#FFFFFF']] # Black to white
