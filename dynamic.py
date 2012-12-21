#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
from animation import animationColor
from opcBrower import getOpcItem
from action_pick import pick_item
import global_var

class displayActionDynamic:
    # This method rotates the position of the tabs
    
    def delete(self, window):
        gtk.main_quit()
        return False
    
    

    def __init__(self,item):
        
        self.list_item_value = ['True','False','None','Value Error','More than','Less than','equal']
        self.list_show_box = ['More than','Less than','equal'] # display active entry box for custom fill value 
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.connect("delete_event", self.delete)
        window.set_border_width(10)
        window.set_title('Action dynamic  property')
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        window.set_default_size (650, 400)
        window.set_destroy_with_parent(True)
        
        vbox = gtk.VBox(False, 2)
        
        window.add(vbox)
        vbox.show()
        
        table = gtk.Table(3,8,False)
        vbox.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0,6,0,1)
        notebook.show()
        self.show_tabs = True
        self.show_border = True
        print 'item dynamic is ',item
        # Let's append a bunch of pages to the notebook
        itemData = item.get_data ("itemProp")
        #property = {}
        widget_in_item = {}
        for readItemDynamic in itemData['dynamic']:
            #print readItemDynamic
            if readItemDynamic == 'Color':
                widget_in_item['Color'] =  {'entry':None,'opc_server_name':None}
                frame,property = self.dynamicColor(readItemDynamic,item,widget_in_item['Color'])
                widget_in_item['Color']['property']=property
                label = gtk.Label(readItemDynamic)
                notebook.prepend_page(frame,label)
                
            if readItemDynamic == 'Flash':
                widget_in_item['Flash'] =  {'entry':None,'opc_server_name':None}
                pcitem = pick_item() # load item pick property from [action_pick.py]
                frame,property = pcitem.dynamicFlash(readItemDynamic,item,widget_in_item['Flash'])#from [action_pick.py]
                widget_in_item['Flash']['property']=property
                label = gtk.Label(readItemDynamic)
                notebook.prepend_page(frame,label)
                
                
            if readItemDynamic == 'Pick':
                #frame,property = self.dynamicColor(readItemDynamic,item,widget_pack)
                widget_in_item['Pick'] =  {'entry':None,'opc_server_name':None}
                pcitem = pick_item() # load item pick property from [action_pick.py]
                frame,property = pcitem.dynamicPick(item,widget_in_item['Pick'])#from [action_pick.py]
                widget_in_item['Pick']['property']=property
                label = gtk.Label(readItemDynamic)
                notebook.prepend_page(frame,label)
    
        # Set what page to start at (page 4)
        notebook.set_current_page(0)

        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_END
        bbox.set_layout(layout)
        bbox.set_spacing(0)
        buttonok = gtk.Button(stock='gtk-ok')
        buttonok.connect("clicked", self.okConfirm,property,item,window,widget_in_item)
        bbox.add(buttonok)
        buttonok.show()

        buttonDelete = gtk.Button(stock='gtk-delete')
        bbox.add(buttonDelete)
        buttonDelete.connect("clicked", self.delete_action,notebook,item)
        buttonDelete.show()
        bbox.show()
    
        
        def close_dialog(self,window):
            #itemPropertySelect.window = None
            window.destroy()
            #window.destroy()
            
        buttonClose = gtk.Button(stock='gtk-close')
        buttonClose.connect("clicked",close_dialog,window)
        bbox.add(buttonClose)
        buttonClose.show()
        
       
        
        
        table.show()
        window.set_resizable(False)
        window.set_modal(True)
        window.show()
        
    def delete_action(self,widget,notebook,item):
        print 'delete action'
        print 'notebook get current page  ',notebook.get_current_page()
        page_num = notebook.get_current_page()
        label = notebook.get_tab_label_text(notebook.get_nth_page(notebook.get_current_page())) 
        print 'remove page and get label is ',label
        itemData = item.get_data ("itemProp")
        del itemData['dynamic'][label]
        '''for readItemDynamic in itemData['dynamic']:
            print type(itemData['dynamic'])
            print readItemDynamic'''
        notebook.remove_page(page_num)
        
    def okConfirm(self,buttonOK,property,item,window,widget_in_item):
        
        for itemDny in widget_in_item:
            self.update_item_property(item,itemDny,widget_in_item[itemDny]) # get update item property
        
        
        window.destroy()
        #for solvent in listProperty:
        #    print "%20s %10s %8s %8s " % (solvent.name,solvent.tag, solvent.color1, solvent.color2)#, solvent.fp)
            #%-20s Left
    def update_item_property(self,item,item_has_dynamic,widget_pack):
        if item_has_dynamic == 'Color':
            itemData = item.get_data ("itemProp")
            new_tag = widget_pack['property']['tag'].get_text()
            item_org_color = self.string_color(widget_pack['property']['colorbutton1'])
            item_fill = self.string_color(widget_pack['property']['colorbutton_fill'])
            item_line = self.string_color(widget_pack['property']['colorbutton_line'])
            #print 'Item color 2 to string is ',itemColor2
            
            #clear item 
            itemDynamic = itemData['dynamic']
            itemDynamicColor = itemDynamic['Color']
            #Update new property from color button
            itemDynamicColor.tag = new_tag
            itemDynamicColor.color_default  = item_org_color
            itemDynamicColor.fill_color  = item_fill#item color
            itemDynamicColor.line_color  = item_line# new color
            
            #Condition to fill color 

            itemDynamicColor.chg_fill_color_state = self.get_combo_text(widget_pack['property']['combo_fill'])
            itemDynamicColor.chg_fill_color_value = widget_pack['property']['entry_fill'].get_text()
            # Line Color Change
            itemDynamicColor.chg_line_color_state = self.get_combo_text(widget_pack['property']['combo_line'])
            itemDynamicColor.chg_line_color_value = widget_pack['property']['entry_line'].get_text()
            #itemData['dynamic']['Color'] = None
           
            item.set_data ('itemProp',itemData) # update new item property
            print 'New tag is ',new_tag
            
            print 'OPC SERVER NAME FROM WIDGET_PACK :',widget_pack['opc_server_name']
            itemDynamicColor.opc_server_name = widget_pack['opc_server_name']
            
        if item_has_dynamic == 'Pick':
            itemData = item.get_data ("itemProp")
            #initial loading new data on widget
            new_tag = widget_pack['property']['tag'].get_text() # read item OPC tag
            combo_widget = widget_pack['property']['combobox2']
            model = combo_widget.get_model()
            index = combo_widget.get_active()
            command_seclect = model[index][0]
            #Load item Group PICK
            itemDynamic = itemData['dynamic'] # load group object
            itemDynamicPick = itemDynamic['Pick'] # load pick object
            itemDynamicPick.tag = new_tag # save new tag value
            itemDynamicPick.opc_server_name = widget_pack['opc_server_name'] # save opc server name 
            itemDynamicPick.cmd_type =  command_seclect # save command select box type
            itemDynamicPick.value = widget_pack['property']['entry2'].get_text() # save value of select
            
            item.set_data ('itemProp',itemData) # update new item property
            
        if item_has_dynamic == 'Flash':
            itemData = item.get_data ("itemProp")
            #initial loading new data on widget
            new_tag = widget_pack['property']['tag'].get_text() # read item OPC tag
            item_fill = self.string_color(widget_pack['property']['colorbutton_fill'])
            combo_widget = widget_pack['property']['combo_fill']
            #model = combo_widget.get_model()
            #index = combo_widget.get_active()
            #command_seclect = model[index][0]
            #Load item Group Flash
            itemDynamic = itemData['dynamic'] # load group object
            itemDynamicFlash = itemDynamic['Flash'] # load pick object
            itemDynamicFlash.tag = new_tag # save new tag value
            itemDynamicFlash.opc_server_name = widget_pack['opc_server_name'] # save opc server name 
            itemDynamicFlash.fill_color  = item_fill#item color
            
            itemDynamicFlash.chg_fill_color_state = self.get_combo_text(widget_pack['property']['combo_fill'])
            itemDynamicFlash.chg_fill_color_value = widget_pack['property']['entry1'].get_text()
            itemDynamicFlash.refresh_rate = int(widget_pack['property']['entry_rate'].get_text())
            #itemDynamicFlash.cmd_type =  command_seclect # save command select box type
            #itemDynamicFlash.value = widget_pack['property']['entry2'].get_text() # save value of select
            item.set_data ('itemProp',itemData) # update new item property
            
        return True
            
    def get_combo_text(self, combobox):
        model = combobox.get_model()
        index = combobox.get_active()
        return model[index][0]
        
    def dynamicColor(self,Color,item,widget_pack):

        dataProperty = {}
        itemData = item.get_data ("itemProp")
        pointDynamic = itemData['dynamic']
        itemSelect = pointDynamic['Color']# itemSelect is data structure see on [animation.py]

        #for solvent in pointDynamic['Color']:
        #    print "Disply tag list %20s %10s %8s %8s " % (solvent.name,solvent.tag, solvent.color1, solvent.color2)#, solvent.fp)
        
        frame = gtk.Frame(Color)
        frame.set_border_width(5)
        frame.set_size_request(530, 280)
        frame.show()

        vbox = gtk.VBox(False, 2)
        vbox.show()
        frame.add(vbox)

        
        table = gtk.Table(6,8,False)# 	if True all cells will be the same size as the largest cell
        table.set_row_spacings(7)
        table.set_col_spacings(8)
        #Table gtk.Table(rows=1, columns=1, homogeneous=False)
        table.show()
        vbox.pack_start(table, False,False, 0)
        
        #---------------------------------------'''LINE 1'''
        hbox = gtk.HBox(False, 2)
        
        label = gtk.Label('OPC Tag   ')
        label.show()
        hbox = self.hbox_pack(label)
        #hbox.pack_start(label, False,False, 0)
        table.attach(hbox, 0,2,0,1)
        
        #hbox.show()
        #label = gtk.Label('Tag.')
        #label.show()
        #table.attach(label, 0,1,0,1)
        entry_tag = self.inputBox(itemSelect.tag)# Display OPC Tag in entry box
        entry_tag.set_size_request(345, 27)
        entry_tag.set_sensitive(True)
        hbox = self.hbox_pack(entry_tag)
        #hbox.pack_start(entry, False,False, 0)
        table.attach(hbox, 2,6,0,1)
        
        buttonTag = gtk.Button("Browe..")
        #buttonTag.set_relief(gtk.RELIEF_NONE)
        buttonTag.set_size_request(65, 27)
        
        
        widget_pack['entry'] = entry_tag
        widget_pack['opc_server_name'] = itemSelect.opc_server_name
        buttonTag.connect("clicked", self.show_opc,item,widget_pack)
        #table.attach(buttonTag,6,7,0,1)
        #hbox.pack_start(buttonTag, False,True, 0)
        buttonTag.show()
        hbox = self.hbox_pack(buttonTag)
        table.attach(hbox,6,8,0,1)
        
        #-------------------------------------------'''LINE2'''

        #hbox = gtk.HBox(False, 2)
        #hbox.show()
        
        label = gtk.Label('Item color')
        label.show()
        #hbox.pack_start(label, False,False, 0)
        hbox = self.hbox_pack(label)
        table.attach(hbox, 0,2,1,2)
        colorbutton1 = gtk.ColorButton(gtk.gdk.color_parse(itemData['color'])) # Display current fill color
        #colorbutton.connect('color-set', color_set_cb)
        colorbutton1.show()
        colorbutton1.set_size_request(30, 30)
        #hbox.pack_start(colorbutton1, False,False, 5)
        hbox = self.hbox_pack(colorbutton1)
        #table.attach(colorbutton1, 3,4,1,2)
        
        Hbox1 = gtk.HBox(False, 0)
        Hbox1.show()
        Hbox1.pack_start(hbox, False,False, 2)
        
        
        
        
        table.attach(Hbox1,2,4,1,2)
        
        #label = gtk.Label('Update')
        #label.show()
        #table.attach(label, 2,4,1,2)
        
        '''#---LINE3---display change fill color '''
        #hbox = gtk.HBox(False, 2)
        #hbox.show()
        label = gtk.Label('Fill color    ')
        label.show()
        hbox = self.hbox_pack(label)
        #hbox.pack_start(label, False,False, 0)
        table.attach(hbox, 0,2,2,3)
        colorbutton_fill = gtk.ColorButton(gtk.gdk.color_parse(itemSelect.fill_color)) # display color 2 has change when tag activate runtime)
        colorbutton_fill.connect('color-set', self.color_set_cb)# print tag color set 
        colorbutton_fill.set_size_request(30, 30) # custom button size is active when homogeneous == False
        colorbutton_fill.show()
        hbox = self.hbox_pack(colorbutton_fill)
        
        #show radio option 
        Hbox2 = gtk.HBox(False, 0)
        Hbox2.show()
        Hbox2.pack_start(hbox, False,False, 2)
        
        #Hbox2.pack_start(hbox, False,False, 2)
        

        label = gtk.Label('Condition when')
        label.show()
        hbox = self.hbox_pack(label)
        Hbox2.pack_start(hbox, False,False, 2)
        
        combobox1 = gtk.combo_box_new_text()
        self.list_value(combobox1)
        vbox = self.vbox_pack(combobox1)
        combobox1.set_size_request(100, 26)
        Hbox2.pack_start(vbox, False,False, 2)
        #Display Input box 
        entry1 = self.inputBox(itemSelect.chg_fill_color_value)# Display OPC Tag in entry box
        entry1.set_size_request(60, 24)
        entry1.set_sensitive(True)
        entry1.set_alignment(0.5)
        hbox = self.hbox_pack(entry1)
        self.change_list_combo(combobox1,entry1)
        #print 'list value 1 ....',self.change_list_combo(combobox,entry)
        combobox1.connect('changed', self.change_list_combo,entry1)# combo changed event
        Hbox2.pack_start(hbox, False,False, 2)
        combobox1.set_active(self.set_combo_text(combobox1,itemSelect.chg_fill_color_state))
        table.attach(Hbox2,2,8,2,3)
        
        
        '''LINE 4 show change Line color'''
        label = gtk.Label('Line color  ')
        label.show()
        hbox = self.hbox_pack(label)
        #hbox.pack_start(label, False,False, 0)
        table.attach(hbox, 0,2,3,4)
        colorbutton_line = gtk.ColorButton(gtk.gdk.color_parse(itemSelect.line_color)) # display color 2 has change when tag activate runtime)
        colorbutton_line.connect('color-set', self.color_set_cb)# print tag color set 
        colorbutton_line.set_size_request(30, 30) # custom button size is active when homogeneous == False
        colorbutton_line.show()
        hbox = self.hbox_pack(colorbutton_line)
        
        #show radio option 
        Hbox2 = gtk.HBox(False, 0)
        Hbox2.show()
        Hbox2.pack_start(hbox, False,False, 2)
        
        #Hbox2.pack_start(hbox, False,False, 2)
        

        
        
        
        
        #Hbox2.pack_start(hbox, False,False, 2)
        label = gtk.Label('Condition when')
        label.show()
        hbox = self.hbox_pack(label)
        Hbox2.pack_start(hbox, False,False, 2)
        
        combobox2 = gtk.combo_box_new_text()
        self.list_value(combobox2)
        vbox = self.vbox_pack(combobox2)
        combobox2.set_size_request(100, 26)
        
        Hbox2.pack_start(vbox, False,False, 2)
        
        #Display Input box 
        entry2 = self.inputBox(itemSelect.chg_line_color_value)# Display OPC Tag in entry box
        entry2.set_size_request(60, 24)
        entry2.set_sensitive(True)
        entry2.set_alignment(0.5)
        
        #print 'list value 2 ....',self.change_list_combo(combobox,entry)
        
        combobox2.connect('changed', self.change_list_combo,entry2)# combo changed event
        
        hbox = self.hbox_pack(entry2)
        Hbox2.pack_start(hbox, False,False, 2)
        
        combobox2.set_active(self.set_combo_text(combobox2,itemSelect.chg_line_color_state))
        
        model = combobox2.get_model()
        print 'Len of  model %s  ',len(model)
        
        self.change_list_combo(combobox2,entry2)
        table.attach(Hbox2,2,8,3,4)
        
        dataProperty['tag'] = entry_tag
        #print eval(repr(colorbutton1.get_color()))
        
        dataProperty['colorbutton1'] = colorbutton1
        dataProperty['colorbutton_fill'] = colorbutton_fill
        dataProperty['colorbutton_line'] = colorbutton_line
        dataProperty['combo_fill'] = combobox1
        dataProperty['entry_fill'] = entry1
        dataProperty['combo_line'] = combobox2
        dataProperty['entry_line'] = entry2
        
        
        return frame,dataProperty
    
    def set_combo_text(self,combobox,set_text):
        model = combobox.get_model()
        if set_text == True:
            set_text = 'True'
            
        if set_text == False:
            set_text = 'False'
            
        for index in range(len(model)):
            if set_text == model[index][0]:
                return index
        return 0 # if none value return default 
        
    
    def list_value(self,widget): # List of change value 
        #TRUE,FALSE,NONE,VALUE ERROR,MORE THAN,LESS THAN,equal
        
        #combobox = gtk.combo_box_new_text()
        for list in self.list_item_value:
            widget.append_text(list)
            
        widget.set_active(0)
        widget.show()
        return widget
    
    def change_list_combo(self,widget,entry):
        model = widget.get_model()
        index = widget.get_active()
        #print 'change list is active index is %s' % index
        print 'List active is ', model[index][0]
        if self.search_list(self.list_show_box,model[index][0]):
            entry.show()
        else:
            entry.hide()
        return True
        
    def search_list (self,list,match):
        for v in list:
            if v == match:
                return True
        return False
    
    def hbox_pack(self,widget):
        hbox = gtk.HBox(False, 0)
        hbox.show()
        hbox.pack_start(widget, False,False, 0)
        widget.show()
        return hbox
    
    def vbox_pack(self,widget):
        vbox = gtk.VBox(False, 0)
        vbox.show()
        vbox.pack_start(widget, False,False, 4)
        widget.show()
        return vbox
    
    def show_opc(self,widget,item,widget_pack):
        #opc_server_name = None
        
        getOpcItem(item,widget_pack) # load window opc tag brower
        
    
    def string_color(self,colorButton):
        color1 = colorButton.get_color()
        get_color = color1.to_string()
        get_color = '#'+get_color[1:3]+get_color[5:7]+get_color[9:11]
        print 'get color from function str ',get_color
        return get_color
    
    def inputBox (self,txt):
        entryDisp = gtk.Entry()
        if txt is not None:
            entryDisp.set_text (txt)
        else:
            entryDisp.set_text ('')
            
        entryDisp.set_editable(True)
        
        return entryDisp
    
    def color_set_cb(self,colorbutton):
        #global color2
        color2 = colorbutton.get_color()
        print 'color set %s '% color2
        return True
    
    

