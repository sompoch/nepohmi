import pygtk
pygtk.require('2.0')
import gtk
#import os
#import global_var
from opcBrower import getOpcItem
from animation import animationPicker

class pick_item():
    
    def __init__(self):
        print 'pick_item initial...'
        self.list_item_value = ['ON','OFF','Toggle Value','Forward','Backward','Set Value','Close Window','Run Script','Text Display']
        self.list_show_flash = ['True','False','None','Value Error','More than','Less than','equal']
    
    def dynamicPick(self,item,widget_pack):

        dataProperty = {}
        itemData = item.get_data ("itemProp")
        pointDynamic = itemData['dynamic']
        itemSelect = pointDynamic['Pick']# itemSelect is data structure see on [animation.py]

        #for solvent in pointDynamic['Color']:
        #    print "Disply tag list %20s %10s %8s %8s " % (solvent.name,solvent.tag, solvent.color1, solvent.color2)#, solvent.fp)
        
        frame = gtk.Frame('Action on press') # set fram title
        frame.set_border_width(5)
        frame.set_size_request(530, 280)
        frame.show()

        vbox = gtk.VBox(False, 2)
        vbox.show()
        frame.add(vbox)

        
        table = gtk.Table(6,8,False)# 	if True all cells will be the same size as the largest cell
        table.set_row_spacings(8)
        table.set_col_spacings(0)
        #Table gtk.Table(rows=1, columns=1, homogeneous=False)
        table.show()
        vbox.pack_start(table, False,False, 0)
        
        #---------------------------------------'''LINE 1'''
        
        # Create OPC Entry Box
        # From table
        # ---------Table (6,8)------------------------------------------------------
        #| 0----hbox(1)----2 2 -------hbox(2)------------------6  6-----hbox(3)---8 |
        #| | Label(OPC Tag)|  | |     Opc entry_tag()          |  | Button(Browe..| |
        #| 1---------------2 2 --------------------------------6  6---------------8 |
        # --------------------------------------------------------------------------
        
        hbox = gtk.HBox(False, 0)
        
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
        entry_tag.set_size_request(345, 28)
        entry_tag.set_sensitive(True)
        hbox = self.hbox_pack(entry_tag)
        #hbox.pack_start(entry, False,False, 0)
        table.attach(hbox, 2,6,0,1)
        
        buttonTag = gtk.Button("Browe..")
        #buttonTag.set_relief(gtk.RELIEF_NONE)
        buttonTag.set_size_request(70, 28)
        
        
        widget_pack['entry'] = entry_tag
        #print 'Show entry tag ',widget_pack['entry']
        widget_pack['opc_server_name'] = itemSelect.opc_server_name
        buttonTag.connect("clicked", self.show_opc,item,widget_pack)
        #table.attach(buttonTag,6,7,0,1)
        #hbox.pack_start(buttonTag, False,True, 0)
        buttonTag.show()
        hbox = self.hbox_pack(buttonTag)
        table.attach(hbox,6,8,0,1)
        
        #-------------------------------------------'''LINE2'''
        
        hbox = gtk.HBox(False, 2)
        hbox.show()
        label = gtk.Label('Command ')
        label.show()
        hbox.pack_start(label, False,False, 0)
        #hbox = self.hbox_pack(label)
        table.attach(hbox, 0,2,1,2)
        
        
        # Create Combobox 
        # x,y (table)
        # 0,1---------hbox-----------------------------------------4,1
        # --------vbox--------------    | -------vbox--------      |
        #| |    Combo_box_new_text() |  | |       entry2() |       |
        #| --------------------------   | -------------------      |
        # 0,2------------------------------------------------------4,2
        
        hbox = gtk.HBox(False, 0)
        combobox2 = gtk.combo_box_new_text()
        self.list_value(combobox2,self.list_item_value)
        vbox = self.vbox_pack(combobox2)
        combobox2.set_size_request(140, 28)
        hbox.pack_start(vbox, False,False, 0)
        
        entry2 = self.inputBox(itemSelect.value)# Display OPC Tag in entry box
        entry2.set_size_request(100, 28)
        entry2.set_sensitive(True)
        entry2.set_alignment(0.5)
        entry2.hide()
        #entry2.set_text(itemSelect.value)
        hbox.pack_start(entry2, False,False, 0)
        #combobox2.set_active(self.set_combo_text(combobox2,itemSelect.cmd_type))
        combobox2.connect('changed', self.change_list_combo,entry2)
        combobox2.set_active(self.set_combo_text(combobox2,itemSelect.cmd_type))
        hbox.show()
        table.attach(hbox, 2,4,1,2)
        #return widget for confirm
        dataProperty['tag'] = entry_tag
        dataProperty['combobox2'] = combobox2
        dataProperty['entry2'] = entry2
        return frame,dataProperty
    
    
    
    
    def dynamicFlash(self,readItemDynamic,item,widget_pack):
        dataProperty = {}
        itemData = item.get_data ("itemProp")
        pointDynamic = itemData['dynamic']
        itemSelect = pointDynamic['Flash']# itemSelect is data structure see on [animation.py]
        print itemSelect
        #for solvent in pointDynamic['Color']:
        #    print "Disply tag list %20s %10s %8s %8s " % (solvent.name,solvent.tag, solvent.color1, solvent.color2)#, solvent.fp)
        
        frame = gtk.Frame('Flash')
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
        
        #---------------------------------------'''ROW 1'''
        hbox = gtk.HBox(False, 2)
        
        label = gtk.Label('OPC Tag   ')
        label.show()
        hbox = self.hbox_pack(label)
        #hbox.pack_start(label, False,False, 0)
        table.attach(hbox, 0,2,0,1)
        #------------------------------------------------
        #|               dynamicFlash ROW1               |
        #------------------------------------------------
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
        
        #------------------------------------------------
        #|               dynamicFlash ROW2               |
        #------------------------------------------------
        # Create OPC Entry Box
        # From table
        # ---------Table (6,8)------------------------------------------------------
        #| 1,0---hbox(1)-----2 2 --hbox(2)---4 4------hbox(3)----6 6---------------8 |
        #| |Label(Item col)  | | Colorbutton1 |  Entry1(refresh) | |                 | HBOX1
        #| 2,0---------------2 2 ------------4 4-----------------6 6---------------8 |
        # --------------------------------------------------------------------------
 
        label = gtk.Label('Item color')
        label.show()
        #hbox.pack_start(label, False,False, 0)
        hbox = self.hbox_pack(label)
        table.attach(hbox, 0,2,1,2)
        
        
        colorbutton1 = gtk.ColorButton(gtk.gdk.color_parse(itemData['color'])) # Display current fill color
        #colorbutton.connect('color-set', color_set_cb)
        colorbutton1.show()
        colorbutton1.set_size_request(35, 35)
        #hbox.pack_start(colorbutton1, False,False, 5)
        hbox = self.hbox_pack(colorbutton1)
        #table.attach(colorbutton1, 3,4,1,2)
        Hbox1 = gtk.HBox(False, 0)
        Hbox1.show()
        Hbox1.pack_start(hbox, False,False, 2)
        
        label = gtk.Label('  Refresh rate')
        label.show()
        #hbox.pack_start(label, False,False, 0)
        hbox = self.hbox_pack(label)
        Hbox1.pack_start(hbox, False,False, 2)
        
        
        
        entry_rate = self.inputBox(str(itemSelect.refresh_rate))# Display refresh rate
        entry_rate.set_size_request(60, 27)
        entry_rate.set_sensitive(True)
        entry_rate.set_alignment(0.5)
        hbox = self.hbox_pack(entry_rate)
        #hbox = self.hbox_pack(hbox_entry)
        Hbox1.pack_start(hbox, False,False, 2)
        
        label = gtk.Label(' millisecond')
        label.show()
        #hbox.pack_start(label, False,False, 0)
        hbox = self.hbox_pack(label)
        Hbox1.pack_start(hbox, False,False, 2)
        
        
        table.attach(Hbox1,2,6,1,2)
        
        #label = gtk.Label('Update')
        #label.show()
        #table.attach(label, 2,4,1,2)
        
        #------------------------------------------------
        #|               dynamicFlash ROW 3             |
        #------------------------------------------------
        
        #hbox = gtk.HBox(False, 2)
        #hbox.show()
        label = gtk.Label('Flash color  ')
        label.show()
        hbox = self.hbox_pack(label)
        #hbox.pack_start(label, False,False, 0)
        table.attach(hbox, 0,2,2,3)
        colorbutton_fill = gtk.ColorButton(gtk.gdk.color_parse(itemSelect.fill_color)) # display color 2 has change when tag activate runtime)
        colorbutton_fill.connect('color-set', self.color_set_cb)# print tag color set 
        colorbutton_fill.set_size_request(35, 35) # custom button size is active when homogeneous == False
        colorbutton_fill.show()
        hbox = self.hbox_pack(colorbutton_fill)
        
        #show radio option 
        Hbox2 = gtk.HBox(False, 0)
        Hbox2.show()
        Hbox2.pack_start(hbox, False,False, 2)
        
        #Hbox2.pack_start(hbox, False,False, 2)
        

        label = gtk.Label('  Condition when')
        label.show()
        hbox = self.hbox_pack(label)
        Hbox2.pack_start(hbox, False,False, 2)
        
        combobox1 = gtk.combo_box_new_text()
        self.list_value(combobox1,self.list_show_flash)
        vbox = self.vbox_pack(combobox1)
        combobox1.set_size_request(100, 26)
        Hbox2.pack_start(vbox, False,False, 2)
        #Display Input box 
        entry1 = self.inputBox(itemSelect.chg_fill_color_value)# Display OPC Tag in entry box
        entry1.set_size_request(60, 24)
        entry1.set_sensitive(True)
        entry1.set_alignment(0.5)
        hbox = self.hbox_pack(entry1)
        self.change_list_combo_flash(combobox1,entry1)
        #print 'list value 1 ....',self.change_list_combo(combobox,entry)
        combobox1.connect('changed', self.change_list_combo_flash,entry1)# combo changed event
        Hbox2.pack_start(hbox, False,False, 2)
        combobox1.set_active(self.set_combo_text(combobox1,itemSelect.chg_fill_color_state))
        table.attach(Hbox2,2,8,2,3)
        
        '''
        #LINE 4 show change Line color
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
        '''
        
        dataProperty['tag'] = entry_tag
        dataProperty['colorbutton1'] = colorbutton1
        dataProperty['colorbutton_fill'] = colorbutton_fill
        dataProperty['entry_rate'] = entry_rate
        dataProperty['combo_fill'] = combobox1
        dataProperty['entry1'] = entry1
        
    
        
        
        return frame,dataProperty
    
    def set_combo_text(self,combobox,set_text):
        model = combobox.get_model()
        print 'combo set ',set_text
        if set_text == True:
            set_text = 'True'
            
        if set_text == False:
            set_text = 'False'
            
        for index in range(len(model)):
            if set_text == model[index][0]:
                return index
        return 0 # if none value return default 
        
    
    def list_value(self,widget,list_item_value): # List of change value 
        #TRUE,FALSE,NONE,VALUE ERROR,MORE THAN,LESS THAN,equal
        #combobox = gtk.combo_box_new_text()
        for list in list_item_value:
            widget.append_text(list)
            
        widget.set_active(0)
        widget.show()
        return widget
    
    def change_list_combo(self,widget,entry):#Pick action
        model = widget.get_model()
        index = widget.get_active()

        #print 'change list is active index is %s' % index
        print 'List active is ', model[index][0]
        #entry.set_text(model[index][0])
        list_enable_entry = ['Set Value','Run Script']
        if self.search_list(list_enable_entry,model[index][0]):
            entry.show()
        else:
            entry.hide()
        return True
    
    def change_list_combo_flash(self,widget,entry):
        model = widget.get_model()
        index = widget.get_active()
        #print 'change list is active index is %s' % index
        list_show_box = ['More than','Less than','equal']
        print 'List active is ', model[index][0]
        if self.search_list(list_show_box,model[index][0]):
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
        
        getOpcItem(item,widget_pack) # load window opc tag brower{opcBrower.py}
        #from opcBrower import getOpcItetm
    
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