#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk
import global_var
import goocanvas

class displayProperty():
    # This method rotates the position of the tabs
    
    def delete(self, window):
        gtk.main_quit()
        return False
    
    def enableScrollZoom(self, widget, data=None):
        print "%s was toggled %s" % (data, ("OFF", "ON")[widget.get_active()])
        
        
    def setSameDisplay(self, widget,listEntry):
        #print " was toggled %s" % (("OFF", "ON")[widget.get_active()])
        if widget.get_active():
            for entry in listEntry:
                entry.set_editable(False)
                entry.set_sensitive(False)
                
            dgd=gtk.gdk.display_get_default()
            gsd=dgd.get_default_screen()
            #print " current screen resolution height=",gsd.get_height(),"width=",gsd.get_width()
            listEntry[2].set_text(str(gsd.get_width()))
            listEntry[3].set_text(str(gsd.get_height()))
            
            global_var.dispProp['sameDisp'] = True
            
        else:
            for entry in listEntry:
                entry.set_editable(True)
                entry.set_sensitive(True)
            global_var.dispProp['sameDisp'] = False
        
    def inputBox (self,txt):
        entryDisp = gtk.Entry()
        entryDisp.set_max_length(5)
        entryDisp.set_size_request(40, 20)
        entryDisp.set_text (str(int(txt)))
        entryDisp.set_editable(True)
        entryDisp.show()
        return entryDisp
    
    def canvas_bound_setting(self,x0,y0,x1,y1):
        vbox3 = gtk.VBox(False, 2)
        vbox3.show()
        
        table1 = gtk.Table(6,4,False)
        vbox3.pack_start(table1, False, False, 0)
        is_sameDisp = True
        
        if global_var.dispProp['sameDisp']:
            is_sameDisp = False
        #is_sameDisp = global_var.dispProp['sameDisp']
        #Line 1 
        label = gtk.Label('Top:')
        label.show()
        table1.attach(label, 0,1,0,1)
        entry1 = self.inputBox(x0)
        entry1.set_sensitive(is_sameDisp)
        table1.attach(entry1, 1,2,0,1)
        
        label = gtk.Label('Left:')
        label.show()
        table1.attach(label, 3,4,0,1)
        entry2 = self.inputBox(y0)
        entry2.set_sensitive(is_sameDisp)
        table1.attach(entry2, 4,5,0,1)
        
        #Line 2
        label = gtk.Label('Width:')
        label.show()
        table1.attach(label, 0,1,1,2)
        entry3 = self.inputBox(x1)
        entry3.set_sensitive(is_sameDisp)
        table1.attach(entry3, 1,2,1,2)
        
        label = gtk.Label('Height:')
        label.show()
        table1.attach(label, 3,4,1,2)
        entry4 = self.inputBox(y1)
        entry4.set_sensitive(is_sameDisp)
        table1.attach(entry4, 4,5,1,2)
    
        table2 = gtk.Table(6,2,False)
        bt = gtk.CheckButton("Use same display resolution")
        bt.set_active(global_var.dispProp['sameDisp']) # Set init value of scroll zoom status
        listEntry = [entry1,entry2,entry3,entry4]
        bt.connect("toggled", self.setSameDisplay,listEntry) # Toggle enable scroll zoom
        bt.show() # Enable display button == ON
        table2.attach(bt, 2,4,0,1)
        vbox3.pack_start(table2, False, False, 0)
        
        table1.show()
        table2.show()
        
        return vbox3,listEntry
    
    def displaySetting(self,w0,h0,is_edit):
        vbox = gtk.VBox(False, 2)
        vbox.show()
        
        table1 = gtk.Table(6,2,False)
        vbox.pack_start(table1, False, False, 0)
        
        #Line 1 
        label = gtk.Label('Width:')
        label.show()
        table1.attach(label, 0,1,1,2)
        entry1 = self.inputBox(str(w0))
        entry1.set_editable(is_edit)
        table1.attach(entry1, 1,2,1,2)
        
        label = gtk.Label('Height:')
        label.show()
        table1.attach(label, 3,4,1,2)
        entry2 = self.inputBox(str(h0))
        entry2.set_editable(is_edit)
        table1.attach(entry2, 4,5,1,2)
        table1.show()
        listEntry = [entry1,entry2]
        return vbox,listEntry
    
    def winOption(self,bt_name):
        button = gtk.CheckButton(bt_name)
        button.set_active(True) # Set init value of scroll zoom status
        button.connect("toggled", self.enableScrollZoom, bt_name) # Toggle enable scroll zoom
        button.show() # Enable display button == ON
        return button
    
    def runDialog(self,title):
        label = gtk.Label(title)
        md = gtk.MessageDialog(None,
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_WARNING, 
            gtk.BUTTONS_CLOSE, title)
        md.run()
        md.destroy()

    
    def confirmChange(self,widget,window,canvas):
        print 'press o.k.'
        listBound = []
        for entry in self.listEntryBound :
            input = entry.get_text()
            try:
                intInput = float(input)
                listBound.append(intInput)
                if intInput <0 :
                    txt = 'Input is negative ' + input
                    self.runDialog(txt)
                    return False
            except ValueError:
                txt = 'Input invalid \'' + input + '\''
                self.runDialog(txt)
                return False
            
        
        '''if input.isdigit():
            
            if intInput <0 :
                txt = 'Input invalid ' + input
                self.runDialog(txt)
                return False
        else:
            txt = 'Input must be a number ' + input
            self.runDialog(txt)
            return False'''
        canvasSize = []
        for entry in self.listEntryCanvasSize:
            input = entry.get_text()
            try:
                intInput = int(input)
                canvasSize.append(intInput)
                if intInput <0 :
                    txt = 'Input is negative ' + input
                    self.runDialog(txt)
                    return False
            except ValueError:
                txt = 'Input invalid \'' + input + '\''
                self.runDialog(txt)
                return False
            
        for entry in self.listEntryDisp:
            print entry.get_text()
            
        canvas.set_bounds (listBound[0], listBound[1], listBound[2], listBound[3])
        canvas.set_size_request(canvasSize[0], canvasSize[1])
        global_var.dispProp['cvSizeWidth'] = canvasSize[0]
        global_var.dispProp['cvSizeHeight'] = canvasSize[1]
        
        global_var.dispProp['cvTop'] =  listBound[0]
        global_var.dispProp['cvLeft'] =  listBound[1]
        global_var.dispProp['cvWidth'] =  listBound[2]
        global_var.dispProp['cvHeight'] = listBound[3]
        
        global_var.grid['grid'].props.width = listBound[2]
        global_var.grid['grid'].props.height = listBound[3]
        
        global_var.grid['show'] = self.bt_grid.get_active()
        if global_var.grid['show'] :
            global_var.grid['grid'].props.visibility =goocanvas.ITEM_VISIBLE
        else:
            global_var.grid['grid'].props.visibility =goocanvas.ITEM_INVISIBLE
        
        #global_var.grid['grid'].set_active()
        '''
         
        try:
            inv_num = int(raw_input("Please type the integer number of flowers you want to order."))
        except ValueError:
            print "I don't understand your answer"
                
        '''
        window.destroy()

    def __init__(self,canvas,scrolled_win): #,canvas,scroll_win
        
        bound = canvas.get_bounds()
        read_size = canvas.get_size_request()
        txt = ""
        self.bt_grid = None
        
        #for imgList in global_var.image_store:
        #    txt = txt + 'Name of Image '+ imgList  + 'image count = ' + str(global_var.image_cnt[imgList]) +  '\n'
        #image_cnt = {}
        
        tab_title = ['Display','General']
        item_disp = ['Display',txt]
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.connect("delete_event", self.delete)
        window.set_border_width(10)
        window.set_title('Display property')
        window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        window.set_default_size (550, 400)
        window.set_destroy_with_parent(True)
        
        vbox = gtk.VBox(False, 0)
        
        window.add(vbox)
        vbox.show()
        
        table = gtk.Table(3,6,False)
        vbox.add(table)

        # Create a new notebook, place the position of the tabs
        notebook = gtk.Notebook()
        notebook.set_tab_pos(gtk.POS_TOP)
        table.attach(notebook, 0,6,0,1)
        notebook.show()
        self.show_tabs = True
        self.show_border = True
        
        dgd=gtk.gdk.display_get_default()
        gsd=dgd.get_default_screen()
        print " current screen resolution height=",gsd.get_height(),"width=",gsd.get_width()
        item_disp[0] = 'Display resolution (width x height) ' 

        # Let's append a bunch of pages to the notebook

        #if id:
        #    print "%s by selection" % id
        #else:
        #    print 'unknow id by selection'

        # Now finally let's prepend pages to the notebook
        for i in range(2):
            if i == 0:
                bufferf =  tab_title[1-i] 
                bufferl = tab_title[1-i] #% (i+1)

                mainHBox = gtk.HBox(False, 2)
                mainHBox.show()
                
                vBox1 = gtk.VBox(False, 0)
                vBox1.show()
                
                vBox2 = gtk.VBox(False, 0)
                vBox2.show()
                
                mainHBox.pack_start(vBox1,False, False, 0)
                mainHBox.pack_start(vBox2,False, False, 0)
                
                #Frame number 1
                frameLabe = 'Canvas bounds (pixel) ' 
                frame = gtk.Frame(frameLabe)
                frame.set_border_width(3)
                frame.set_size_request(250, 100)
                frame.show()
                vBox1.pack_start(frame,False, False, 0)
                vboxInFrame,self.listEntryBound = self.canvas_bound_setting(bound[0],bound[1],bound[2],bound[3])# create fram 1 canvas bounds get dimension setting
               
                frame.add(vboxInFrame)
                # Frame number 2
                frameLabe = 'Canvas size' 
                frame = gtk.Frame(frameLabe)
                frame.set_border_width(3)
                frame.set_size_request(250, 60)
                frame.show()
                vBox1.pack_start(frame,False, False, 0)
                vboxInFrame,self.listEntryCanvasSize = self.displaySetting(read_size[0],read_size[1],True)# create fram 1 canvas bounds get dimension setting
                frame.add(vboxInFrame)
                
                # Frame number 3
                frameLabe = 'Current dispplay resolution ' 
                frame = gtk.Frame(frameLabe)
                frame.set_border_width(3)
                frame.set_size_request(250, 60)
                frame.show()
                vBox1.pack_start(frame,False, False, 0)
                vboxInFrame,self.listEntryDisp = self.displaySetting(gsd.get_width(),gsd.get_height(),False)# create fram 1 canvas bounds get dimension setting
                frame.add(vboxInFrame)
                
                # Frame number 4
                frameLabe = 'Window option ' 
                frame = gtk.Frame(frameLabe)
                frame.set_border_width(3)
                frame.set_size_request(150, 200)
                frame.show()
                vBox2.pack_start(frame,False, False, 0)
                vboxInFrame = gtk.VBox(False, 0)
                bt = self.winOption("Enable scroll zoom")
                vboxInFrame.pack_start(bt,False, False, 0)
                self.bt_grid = self.winOption("Show grid")
                self.bt_grid .set_active(global_var.grid['show'])
                vboxInFrame.pack_start(self.bt_grid ,False, False, 0)
                bt = self.winOption("Alway on top")
                vboxInFrame.pack_start(bt,False, False, 0)
                bt = self.winOption("Start run mode \n when window load")
                vboxInFrame.pack_start(bt,False, False, 0)
                vboxInFrame.show()
                #vboxInFrame = self.displaySetting(gsd.get_width(),gsd.get_height())# create fram 1 canvas bounds get dimension setting
                frame.add(vboxInFrame)
                

                label = gtk.Label(bufferl)
                notebook.prepend_page(mainHBox, label)
                
            if i == 1:
                
                pass
    
        # Set what page to start at (page 4)
        notebook.set_current_page(0)
        

        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_END
        bbox.set_layout(layout)
        bbox.set_spacing(0)
        buttonok = gtk.Button(stock='gtk-ok')
        buttonok.connect("clicked", self.confirmChange,window,canvas)
        bbox.add(buttonok)
        buttonok.show()

        buttonClear = gtk.Button(stock='gtk-apply')
        bbox.add(buttonClear)
        #buttonClear.connect("clicked", self.clear_text,view1)
        buttonClear.show()
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
        window.show()
        window.set_resizable(False)
        window.set_modal(True)