import pygtk
pygtk.require('2.0')
import gtk
import goocanvas
import global_var
import cairo
import os

class colorPanelProperty:
    def createColorWidget(self):
        self.size_group = gtk.SizeGroup(gtk.SIZE_GROUP_HORIZONTAL)
        frame = gtk.Frame('Color')
        frame.set_border_width(0)
        frame.set_size_request(200, 400)
        frame.show()
        
        
        vbox = gtk.VBox(False, 0)
        #----Line 1  Opacity --------------- 
        
        hbox = gtk.HBox(False,0)
        hbox.show()
        
        label = gtk.Label("Opacity:")
        label.show()
        hbox.pack_start(label, False, True, 0)
        adj_hscale = gtk.Adjustment(0, 0, 100, 1.0, 5.0, 0.0)
        hscale= gtk.HScale(adj_hscale)
        hscale.set_size_request(30, -1)
        hscale.set_value_pos(gtk.POS_RIGHT)
        hscale.set_draw_value(False) 
        hscale.set_digits(1)
        hbox.pack_start(hscale, True, True, 0)
        hscale.show()
        #keep hscale to global value
        global_var.dialogWidget['colorOpacity_hscale'] = hscale
        
        adj_spin = gtk.Adjustment(0, 0, 100, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj_spin, 0, 0)
        spinner.set_wrap(True)
        spinner.set_size_request(15, -1)
        spinner.show()
        global_var.dialogWidget['colorOpacity_spinner'] = spinner #keep spinner to global value
        
        
                
        
        hbox.pack_start(spinner, True, True, 0)
        
        global cval # temp value of spinner and hscale
        item = None
        color = None
        adj_spin.connect("value_changed", self.change_alpha_level, spinner,hscale, item,"spinner",color)
        adj_hscale.connect("value_changed", self.change_alpha_level, spinner,hscale, item,"hscale",color)
        vbox.pack_start(hbox,False,True,0)
        
        #-----Line 2 Item Color Button -----------
        label_color = gtk.Label("Color   : ")
        label_color.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_color,False,True,0)
        hbox.show()
        #...Create color button
        colorbutton = gtk.ColorButton(gtk.gdk.color_parse('#CC3300')) # Display current fill color
        colorbutton.connect('color-set', self.color_set_cb)
        colorbutton.show()
        global_var.dialogWidget['colorColor_button'] = colorbutton # keep color button to global value
        colorbutton.set_size_request(45, 45)
        hbox.pack_start(colorbutton,False,True,0)
        vbox.pack_start(hbox,False,True,0)
       
        
        #-----Line 3 Item Color Fill Option-----------
        label_Fill = gtk.Label("Fill      : ")
        label_Fill.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label_Fill,False,True,0)
        hbox.show()
        
        options = ["None","Solid", "RGBA","Gradiant","Pattern"]
        option_color = gtk.combo_box_new_text()
        for opt in options:
            option_color.append_text(opt)

        option_color.set_active(0)
        option_color.set_size_request(85, -1)
        option_color.show()
        option_color.connect('changed',self.combo_fill_mode)
        global_var.dialogWidget['colorFill_option'] = option_color # keep fill color option to global value
        
        hbox.pack_start(option_color,False,True,0)
        vbox.pack_start(hbox,False,True,0)
        #vbox.pack_start(colorbutton,False,True,0)
        #label.show()
        frame.add(vbox)
        vbox.show()
        #------Line 4 gradiant option  area-----------
        '''
        expander = gtk.Expander("Gradiant  :")


        # The Label for the expander
        label = gtk.Label("Details can be shown or hidden.")
        expander.add(label)
        
        #label_Gradiant = gtk.Label("Gradiant  : ")
        expander.show()
        hbox = gtk.HBox(False,0)
        hbox.pack_start(expander,False,True,0)
        hbox.show()
        #expander.add(hbox)
        vbox.pack_start(hbox,False,True,0)'''
        hbox = gtk.HBox(False,0)
        vbox_s = gtk.VBox(False,0)
        #scrolled_win = gtk.ScrolledWindow ()
        #scrolled_win.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC) #gtk.POLICY_NEVER 
        #vbox_s.pack_start (scrolled_win, False, True, 0)
        vbox_s.show()
        #vbox.pack_start(vbox, False, True, 0)
        label_Gradiant = gtk.Label("Gradiant Show")
        label_Gradiant.show()
        label_Pattern = gtk.Label("Pattern  Show ")
        label_Pattern.show()
        
        expander_g = gtk.Expander("Gradiant")
        expander_g.show()
        c_pre = self.preview_canvas()
        expander_g.add(c_pre)
        
        expander_p = gtk.Expander("Pattern")
        expander_p.show()
        expander_p.add(label_Pattern)
        
        #scrolled_win.add(expander_g)
        #scrolled_win.add(expander_p)
        #scrolled_win.show()
        #scrolled_win.add(expander_p)
        vbox_s.pack_start(expander_g, False, True, 0)
        vbox_s.pack_start(expander_p, False, True, 0)
        
        #vbox_s.set_border_width(0)
        hbox.pack_start(vbox_s,False,True,0)
        hbox.show()
        
        vbox.pack_start(hbox,False,True,0)
        
        
        
        self.size_group.add_widget(label)
        self.size_group.add_widget(label_color)
        self.size_group.add_widget(label_Fill)
        #self.size_group.add_widget(label_Gradiant)
        
        return frame
    
    def preview_canvas(self):
        vbox = gtk.VBox(False,0)
        canvas = goocanvas.Canvas()
        canvas.set_size_request(185, 125)
        canvas.set_bounds(0, 0, 185, 125)
        canvas.show()
        root = canvas.get_root_item()

        # Create a Linear Patter with cairo 
        linear = cairo.LinearGradient(60, 0, 60, 120)
        linear.add_color_stop_rgba(0.0,  1, 1, 1, 1)
        #linear.add_color_stop_rgba(0.25,  0, 1, 0, 0.5)
        #linear.add_color_stop_rgba(0.50,  1, 1, 1, 0)
        linear.add_color_stop_rgba(0.5,  0, 0, 1, 1)
        #linear.add_color_stop_rgba(1.0,  1, 1, 1, 0)
        self.press_xy = [0,0,20,20] 
        
       # Create a rect to be filled with the linear gradient
        item = goocanvas.Rect(x=0, y=0, width=120, height=120,
                              line_width=0,
                              #radius_x=20.0,
                              #radius_y=10.0,
                              fill_pattern=linear)
                            
        item.connect("button-press-event", self.on_preview_press)
        item.connect("button-release-event", self.on_preview_release)
        canvas.connect("motion-notify-event", self.on_motion_notify)
        
        item.set_simple_transform(0,50,0.5,0)
        
        root.add_child(item, 0)
        
        
        vbox.pack_start(canvas,False,True,1)
        self.label_preview = gtk.Label("Preview")
        self.label_preview.show()
        vbox.pack_start(self.label_preview,False,True,1)
        canvas.connect("motion-notify-event", self.on_motion_notify)#label_preview
        self.sample_gradiant(canvas)
        vbox.show()
        return vbox
        
    def on_button_press_arrow_up (self,item, target, event,item_bg):
        
        print "press arrow up ",item_bg.props.x
        item_bg.props.fill_color_rgba = 0xA1C2D27F
        item_bg.props.fill_pattern = self.radial

        return True
    
    def on_button_release_arrow_up (self,item, target, event,item_bg):
        
        print "release arrow up ",item_bg.props.x
        item_bg.props.fill_color_rgba =  0xA1C2D27F#0xD4B9B05F

        return True
        
    def on_button_press (self,item, target, event):
        
        canvas = item.get_canvas ()
        canvas.grab_focus (item)

        return True
    
    def on_button_press_cursor (self,item, target, event):
        self.posy = item.props.y
        item.props.fill_color = "#E99F86"
        print "Cursor press"

        return True
    
    def on_button_release_cursor (self,item, target, event):
        diff = event.y - self.posy
        item.props.fill_color = "#C8BDBA"
        item.props.y = diff
        print "Cursor release"

        return True
    

    def on_key_press (item, target, event):
        id = item.get_data ("id")
        
        if id:
            print "%s received key-press event" % id
        else:
            print "unknown"

        return False
    
    def on_enter_notify(self,item, target, event):
        #for item in self.list_item:
        #if item.props.stroke_color != "yellow":
        item.props.stroke_color = "yellow"
        item.props.line_width =4
        return True

    def on_leave_notify(self,item, target, event):
        #if item.props.stroke_color != "white":
        item.props.stroke_color = "white"
        item.props.line_width =2
        return True
    
    def sample_gradiant(self,canvas):
        root = canvas.get_root_item()
        self.list_item=[]
        color_set =['red','blue','green','#A0FF05',"#567893",'#567400','#AF3456','#F345B2']
        group1 = goocanvas.Group(parent = root,x=125, y=0, width=46, height=360,
                              line_width=0)
        
        #TODO : create arrow setecd gradiant template
        gadiant_list = []
        
        self.radial = cairo.RadialGradient(20, 7, 15, 20, 7, 40)
        self.radial.add_color_stop_rgba(0,  0.63, 0.76, 0.82,0.8)
        self.radial.add_color_stop_rgba(0.9,  0.1, 0.1, 1,0.8)
        gadiant_list.append(self.radial)
        for j in range(7):
            linear = cairo.LinearGradient(0, 0, 20,7 )
            linear.add_color_stop_rgba(0.0,  1, 1, 1, 0)
            linear.add_color_stop_rgba(0.25,  0, 1, 0, 0.5)
            gadiant_list.append(linear)
        
        for i in range(8):
            item = goocanvas.Rect(parent = group1,x=0, y=(i*30+5), width=45, height=28,
                              line_width=2,
                              fill_color = color_set[i],
                              stroke_color = 'white',
                              fill_pattern = gadiant_list[i],
                              radius_x=4,
                              radius_y=4)
            #focus_in_event
            #item.connect("enter_notify_event", self.on_enter_notify)#enter-notify
            #item.connect("leave_notify_event", self.on_leave_notify)
            item.connect("focus_in_event", self.on_enter_notify)#enter-notify
            item.connect("focus_out_event", self.on_leave_notify)
            item.connect("button_press_event", self.on_button_press)
            self.list_item.append(item)
        #Cursor 
        
                            
        '''item = goocanvas.Rect(parent = root,x=173, y=0, width=11, height=120,
                              line_width=0,
                              fill_color_rgba = 0xEDD4CC7F, #EDD4CC
                              radius_x=3.0,
                              radius_y=3.0,
                              stroke_color = 'white')
                            
        item = goocanvas.Rect(parent = root,x=175, y=0, width=7, height=20,
                              line_width=1,
                              fill_color = "#C8BDBA", #EDD4CC
                              radius_x=3.0,
                              radius_y=3.0,
                              stroke_color = '#9D847C')
        item.connect("button_press_event", self.on_button_press_cursor)
        item.connect("button_release_event", self.on_button_release_cursor)'''
        
        adj_hscale = gtk.Adjustment(0, 0, 100, 1.0, 5.0, 0.0)
        #vscale= gtk.VScale(adj_hscale)
        #vscale.set_size_request(5, 110)
        #vscale.set_value_pos(gtk.POS_RIGHT)
        #vscale.set_draw_value(False) 
        
        #scrbar = gtk.Scrollbar(0,10)
        scrolled = gtk.ScrolledWindow ()
        scrolled.set_policy(gtk.POLICY_NEVER,gtk.POLICY_ALWAYS)
        scrolled.set_vadjustment(adj_hscale)
        adj_hscale.connect("value_changed", self.gradiant_template_sel,group1)
        
        ent = goocanvas.Widget(parent = root,
                           widget = scrolled,
                           x = 176,
                           y = 60,
                           width = -1,
                           height = 120,
                           anchor = gtk.ANCHOR_CENTER)
        
        #Create Arrow button for selected gradaint from template
        
        '''
        group1 = goocanvas.Group(parent = root,x=124, y=0, width=45, height=16,
                              line_width=0)
        #Blackground image arrow up 
        self.radial = cairo.RadialGradient(20, 7, 15, 20, 7, 40)
        self.radial.add_color_stop_rgba(0,  0.63, 0.76, 0.82,0.8)
        self.radial.add_color_stop_rgba(0.9,  0.1, 0.1, 1,0.8)
        
        item = goocanvas.Rect(parent = group1,x=0, y=0, width=45, height=15,
                              line_width=0,
                              fill_color_rgba = 0xA1C2D27F, #EDD4CC
                              #fill_color = 'red',
                              radius_x=2,
                              radius_y=2,
                              #fill_pattern=None,
                              stroke_color = 'green')
                            
        
        
        #p_points = goocanvas.Points([(4, 11), (22, 3), (40, 11)])
        #polyline = goocanvas.Polyline(parent = group1,points=p_points, close_path=False, stroke_color="gray", line_width = 3)
        current_dir = os.getcwd()
        if os.name == 'nt':# check window os
            path = current_dir+'\\images\\'
        else: 
            path = current_dir+'/images/'
            
        path_ico_up = path + "/arrow_up.png"
        path_ico_down = path + "/arrow_down.png"
        
        pixbuf = gtk.gdk.pixbuf_new_from_file(path_ico_up)
        image = goocanvas.Image(parent = group1,pixbuf=pixbuf, x=0, y=-9)
        image.scale(0.7,0.4)
        image.connect("button_press_event", self.on_button_press_arrow_up,item)
        image.connect("button_release_event", self.on_button_release_arrow_up,item)
        
        
        #Create arrow pick down
        group2 = goocanvas.Group(parent = root,x=124, y=105, width=45, height=17,
                              line_width=0)
        item = goocanvas.Rect(parent = group2,x=0, y=0, width=45, height=16, #137
                              line_width=0,
                              fill_color_rgba = 0xA1C2D27F, #EDD4CC
                              #fill_color = 'red',
                              radius_x=2,
                              radius_y=2,
                              #fill_pattern=None,
                              stroke_color = 'green')
        pixbuf = gtk.gdk.pixbuf_new_from_file(path_ico_down)
        image = goocanvas.Image(parent = group2,pixbuf=pixbuf, x=0, y=-7)
        image.scale(0.7,0.4)
        image.connect("button_press_event", self.on_button_press_arrow_up,item)
        image.connect("button_release_event", self.on_button_release_arrow_up,item)'''
       
        
    def gradiant_template_sel(self,widget,group1):
        val = 0-widget.get_value()
        group1.set_simple_transform(0,val , 1, 0)
    
    def pattern_new(self):
        pos = self.press_xy
        linear = cairo.LinearGradient(pos[0], pos[1], pos[2], pos[3])
        linear.add_color_stop_rgba(0.0,  0, 0, 1, 1)
        #linear.add_color_stop_rgba(0.25,  0, 1, 0, 0.5)
        #linear.add_color_stop_rgba(0.50,  1, 1, 1, 0)
        linear.add_color_stop_rgba(0.5,  1, 1, 1, 1)
        return linear
    
    def on_preview_press(self,view, item, event):
        #print "press item %s % s" % (event.x,event.y)
        self.press_xy[0] = event.x
        self.press_xy[1] = event.y
        
    def on_preview_release(self,view, item, event):
        #print "press item %s % s" % (event.x,event.y)
        self.press_xy[2] = event.x
        self.press_xy[3] = event.y
        #print "Sumary position ",
        #print self.press_xy
        pattern_ = self.pattern_new()
        item.props.fill_pattern = pattern_
        if global_var.itemSelectActive2 is not None: # update new pattren 
            global_var.itemSelectActive2.props.fill_pattern = pattern_
            print "set new pattern "
        
    def on_motion_notify(self, area, event):
        pos =  'x,y =  ' + str(event.x) + ',' + str(event.y)
        
        
        #self.label_preview.set_text(pos)
        return True
    
    def color_set_cb(self,widget):
        if global_var.itemSelectActive2 is not None:
            boxcolor = widget.get_color()
            get_color = boxcolor.to_string()
            get_color = '#'+get_color[1:3]+get_color[5:7]+get_color[9:11]
            itemProperty = global_var.itemSelectActive2.get_data('itemProp')
            itemProperty['color'] = get_color
            
            if itemProperty['fill_mode'] == 'Solid':
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
            #----------END OF GET ITEM VALUE ------------------------------

    
    def change_alpha_level(self,widget,spinner,hscale,item,widget_active,color):
        global cval
        if global_var.itemSelectActive2 is not None:
            if widget_active =="spinner":
                cval = int(spinner.get_value())
                if cval != hscale.get_value():
                    hscale.set_value(cval)
                    '''hex_alpha = hex(int(cval*2.55))
                    if len(hex_alpha)<4:
                        hex_alpha = '0'+hex_alpha[2:3]
                    else:
                        hex_alpha = hex_alpha[2:4]'''
                        
                    #print "GET COLOR %s alpha Hex = %s : %s  full " % (color,hex_alpha,widget_active),
                    itemProperty = global_var.itemSelectActive2.get_data('itemProp')
                    color = itemProperty['color']
                    color = color.replace('#','')
                    #color = hex(hex_alpha+color)
                    color = int(color,16)*256 + int(cval*2.55)
                    #print hex(color)
                    global_var.itemSelectActive2.props.fill_color_rgba = color#0x3cb37180#0x7fff9c00
                    itemProperty['rgbaColor']= color
                    #save item property
                    
                    global_var.itemSelectActive2.set_data('itemProp',itemProperty)
                    
            else: # The hscale click active 
                cval = int(hscale.get_value())
                if cval != spinner.get_value():
                    spinner.set_value(cval)
                #print "GET COLOR %s alpha Hex = %s : %s " % (color,hex(cval),widget_active)
                
    def combo_fill_mode(self,widget): #
        index  = widget.get_active()
        if index != -1:
            if global_var.itemSelectActive2 is not None:
                itemProperty = global_var.itemSelectActive2.get_data('itemProp')
                itemProperty['fill_mode'] = widget.get_active_text()
                global_var.itemSelectActive2.set_data('itemProp',itemProperty) # save item property
                print "SET FILL MODE ",widget.get_active_text()
                #SET ITEM TO NEW FILL MODE 
                
                if index == 0: #None mode 
                    itemProperty['fill_mode'] = 'None'
                    
                if index == 1: #solid mode 
                    global_var.itemSelectActive2.props.fill_color = itemProperty['color']
                    itemProperty['fill_mode'] = 'Solid'
                if index == 2: #rgba Mode 
                    itemProperty['fill_mode'] = 'RGBA'
                    
                global_var.itemSelectActive2.set_data('itemProp',itemProperty)
                
            if index in [0,1]:
                global_var.dialogWidget['colorOpacity_hscale'].set_sensitive(False)
                global_var.dialogWidget['colorOpacity_spinner'].set_sensitive(False)
                if index == 0:
                    global_var.dialogWidget['colorColor_button'].set_sensitive(False)
                else:
                    global_var.dialogWidget['colorColor_button'].set_sensitive(True)
                
            if index == 2:
                global_var.dialogWidget['colorOpacity_hscale'].set_sensitive(True)
                global_var.dialogWidget['colorOpacity_spinner'].set_sensitive(True)
                global_var.dialogWidget['colorColor_button'].set_sensitive(True)
            
                
        return True 