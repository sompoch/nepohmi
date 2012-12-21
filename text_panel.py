import pygtk
pygtk.require('2.0')
import gtk,os
import global_var

class textPanelProperty:
    def createLineWidget(self):
        self.size_group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        
        options = ["None","Solid", "Dashed", "Dotted"]
        frame = gtk.Frame('Line')
        frame.set_border_width(0)
        frame.set_size_request(200, 400)
        frame.show()
        label = gtk.Label("Text Editor: ")
        label.show()
        
        vbox = gtk.VBox(False, 5)
        
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label,False,True,0)
        hbox.show()
        vbox.pack_start(hbox,False,True,0)
        # Create Text box Entry 
        #Create Line Color 
        
        entry = gtk.Entry()
        entry.set_max_length(150) 
        entry.set_text("hello")       
        #entry.connect("activate", self.enter_callback, entry)
        #entry.insert_text(" world", len(entry.get_text()))
        #entry.select_region(0, len(entry.get_text()))
        #vbox.pack_start(entry, True, True, 0)
        entry.set_size_request(180,25)
        entry.show()
        global_var.dialogWidget['text_edit'] = entry

    
        hbox = gtk.HBox(False,0)
        hbox.pack_start(entry,False,True,0)
        hbox.show()
        vbox.pack_start(hbox,False,True,0)
        
        image = gtk.Image()
        image.set_from_stock(gtk.STOCK_APPLY,gtk.ICON_SIZE_MENU)
        button = gtk.Button()
        button.add(image)
        button.set_tooltip_text('Save text')
        button.connect("clicked",self.applyText,entry)
        button.set_size_request(30,30)
        button.show()
        
        
        hbox = gtk.HBox(False,0)
        hbox.pack_start(button,False,True,0)
        hbox.show()
        vbox.pack_start(hbox,False,True,0)
        
        '''
        option_line = gtk.combo_box_new_text()
        for opt in options:
            option_line.append_text(opt)

        option_line.set_active(0)
        option_line.set_size_request(85, -1)
        option_line.show()
        global_var.dialogWidget['lineOption'] = option_line # Keep line option on global variable
        
        hbox.pack_start(option_line,False,True,0)
        vbox.pack_start(hbox,False,True,0)
        
        #Create Line Color 
        label_color = gtk.Label("Line color  : ")
        label_color.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_color,False,True,0)
        hbox.show()
        #...Create color button
        colorbutton = gtk.ColorButton(gtk.gdk.color_parse('#CC3300')) # Display current fill color
        colorbutton.connect('color-set', self.color_set_cb)
        colorbutton.show()
        colorbutton.set_size_request(45, 45)
        global_var.dialogWidget['lineColor'] = colorbutton
        hbox.pack_start(colorbutton,False,True,0)
        vbox.pack_start(hbox,False,True,0)
        #----Line 3---------------------------
        
        label_width = gtk.Label("Line width  : ")
        label_width.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_width,False,True,0)
        hbox.show()
        vbox.pack_start(hbox,False,True,0)
        #  add combo with image line width 
        combo_img = self.createLineWidth()
        hbox.pack_start(combo_img,False,True,0)
        global_var.dialogWidget['lineWidth'] = combo_img
        
        #line 4---dash----------------------------
        label_dash = gtk.Label("Dash Type  : ")
        label_dash.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_dash,False,True,0)
        hbox.show()
        vbox.pack_start(hbox,False,True,0)
        #  add combo with image line width 
        combo_dash = self.createDashType()
        hbox.pack_start(combo_dash,False,True,0)
        global_var.dialogWidget['lineDash'] = combo_dash
        #label.show()
        #line 5 ------------------------------

        label_curve = gtk.Label("Radius :    ")
        label_curve.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_curve,False,True,0)
        hbox.show()
        
        adj_hscale = gtk.Adjustment(0, 0, 50, 1.0, 5.0, 0.0)
        hscale= gtk.HScale(adj_hscale)
        hscale.set_size_request(30, -1)
        hscale.set_value_pos(gtk.POS_RIGHT)
        hscale.set_draw_value(False) 
        hscale.set_digits(1)
        hbox.pack_start(hscale, True, True, 0)
        hscale.show()
        global_var.dialogWidget['lineCurve_hscale'] = hscale
        
        adj_spin = gtk.Adjustment(0, 0, 50, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj_spin, 0, 0)
        spinner.set_wrap(False)
        spinner.set_size_request(35, -1)
        hbox.pack_start(spinner, True, True, 0)
        spinner.show()
        global_var.dialogWidget['lineCurve_spinner'] = spinner
        
        item = None
        adj_spin.connect("value_changed", self.change_curve_level, spinner,adj_hscale, item,"spinner")
        adj_hscale.connect("value_changed", self.change_curve_level, spinner,adj_hscale, item,"hscale")
        
        vbox.pack_start(hbox,False,True,0)'''
        
        frame.add(vbox)
        vbox.show()
        self.size_group.add_widget(label)
        #self.size_group.add_widget(label_color)
        #self.size_group.add_widget(label_width)
        #self.size_group.add_widget(label_dash)
        #self.size_group.add_widget(label_curve)
        
        return frame
    
    def applyText(self,button,entry):
        if global_var.itemSelectActive2 is not None:
            global_var.itemSelectActive2.props.text = entry.get_text()
        print "Save edit text ",entry.get_text()
        
    def createLineWidth(self):
        it = gtk.icon_theme_get_default()
        ls = gtk.ListStore(gtk.gdk.Pixbuf, str)
        ComboImage = gtk.ComboBox()
        # build our list store with an icon column and
        #Get current directory
        current_dir = os.getcwd()
        if os.name == 'nt':# check win32 os
            path = current_dir+'\\images\\line_width'
        else: 
            path = current_dir+'/images/line_width'

        for i in range(0,21):
            path_ico = path+str(i)+".png"
            image = gtk.gdk.pixbuf_new_from_file(path_ico)
            ls.append([image,str(i)])
        
        ComboImage.set_model(ls)
        
        # Add text
        crt = gtk.CellRendererText()
        crt.set_property('xalign',0)
        ComboImage.pack_start(crt, True)
        ComboImage.add_attribute(crt, 'text', 1)  
        # Add Image Area on combo
        crp = gtk.CellRendererPixbuf()
        crp.set_property('xalign',0)
        ComboImage.pack_start(crp, True)
        ComboImage.add_attribute(crp, 'pixbuf', 0)
        ComboImage.set_size_request(85, -1)
        ComboImage.set_active(0)
        ComboImage.connect('changed',self.combo_fill_line)
        ComboImage.show()
        
        return ComboImage
    
    def color_set_cb(self,widget):
        if global_var.itemSelectActive2 is not None:
            boxcolor = widget.get_color()
            get_color = boxcolor.to_string()
            get_color = '#'+get_color[1:3]+get_color[5:7]+get_color[9:11]
            itemProperty = global_var.itemSelectActive2.get_data('itemProp')
            itemProperty['stroke_color'] = get_color
            global_var.itemSelectActive2.props.stroke_color = get_color
            global_var.itemSelectActive2.set_data('itemProp',itemProperty)
            
            '''if itemProperty['fill_mode'] == 'Solid':
                global_var.itemSelectActive2.props.fill_color = get_color
                
                
            if itemProperty['fill_mode'] == 'RGBA':
                cval = int(global_var.dialogWidget['colorOpacity_hscale'].get_value())
                color = itemProperty['color']
                get_color = get_color.replace('#','')
                get_color = int(get_color,16)*256 + int(cval*2.55)
                global_var.itemSelectActive2.props.fill_color_rgba = get_color#0x3cb37180#0x7fff9c00
                itemProperty['rgbaColor']= get_color
                
            #----------GET ITEM PROPERTY AND SAVE NEW VALUE----------------
            
            
            global_var.itemSelectActive2.set_data('itemProp',itemProperty)
            #----------END OF GET ITEM VALUE ------------------------------'''
    
    def combo_fill_line(self,widget):
        index  = widget.get_active()
        if index != -1 and global_var.itemSelectActive2 is not None:
            global_var.itemSelectActive2.props.line_width = index # set new line width
    
    def change_curve_level(self,widget,spinner,hscale,item,widget_active):
        if widget_active =="spinner":
            cval = spinner.get_value()
            hscale.set_value(cval)
        else:
            cval = hscale.get_value()
            spinner.set_value(cval)
            
        if global_var.itemSelectActive2 is not None:
            global_var.itemSelectActive2.props.radius_x = cval
            global_var.itemSelectActive2.props.radius_y = cval
    
    def createDashType(self):
        it = gtk.icon_theme_get_default()
        ls = gtk.ListStore(gtk.gdk.Pixbuf, str)
        ComboImage = gtk.ComboBox()
        # build our list store with an icon column and
        #Get current directory
        current_dir = os.getcwd()
        if os.name == 'nt':# check win32 os
            path = current_dir+'\\images\\dash'
        else: 
            path = current_dir+'/images/dash'

        for i in range(1,3):
            path_ico = path+str(i)+".png"
            image = gtk.gdk.pixbuf_new_from_file(path_ico)
            ls.append([image,str(i)])

        
        ComboImage.set_model(ls)
        
        # Add text
        crt = gtk.CellRendererText()
        crt.set_property('xalign',0)
        ComboImage.pack_start(crt, True)
        ComboImage.add_attribute(crt, 'text', 1)  
        # Add Image Area on combo
        crp = gtk.CellRendererPixbuf()
        crp.set_property('xalign',0)
        ComboImage.pack_start(crp, True)
        ComboImage.add_attribute(crp, 'pixbuf', 0)
        ComboImage.set_size_request(85, -1)
        ComboImage.set_active(3)
        ComboImage.show()
        
        return ComboImage