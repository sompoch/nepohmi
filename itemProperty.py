#!/usr/bin/env python

# example notebook.py

import pygtk
pygtk.require('2.0')
import gtk

class itemPropertySelect:
    # This method rotates the position of the tabs
    
    def delete(self, window):
        gtk.main_quit()
        return False
    
    

    def __init__(self,item):
        tab_title = ['Color','Line','Gradiant','Position','Advance']
        item_prop = ['Color','Line','Gradiant','Position','Advance']
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        #window.connect("delete_event", self.delete)
        self.window.set_border_width(10)
        self.window.set_title('Item property')
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS) # set window to center posiotion whwn startup
        self.window.set_default_size (400, 300)
        self.window.set_destroy_with_parent(True)
        
        vbox = gtk.VBox(False, 2)
        
        self.window.add(vbox)
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

        # Let's append a bunch of pages to the notebook
        self.ItemProperty = item.get_data ("itemProp")
        #if id:
        #    print "%s by selection" % id
        #else:
        #    print 'unknow id by selection'
        item_prop[0] = self.ItemProperty['color']
        item_prop[1] = 'Line width = '+ str(self.ItemProperty['line_width'])
        item_prop[3] = 'Item position %s , %s ' %(item.props.x,item.props.y)
        # Now finally let's prepend pages to the notebook
        for i in range(5):
            bufferf =  tab_title[4-i] 
            bufferl = tab_title[4-i] #% (i+1)
            
            frame = gtk.Frame(bufferf)
            frame.set_border_width(10)
            frame.set_size_request(100, 75)
            frame.show()
            
            if i == 4: # color item 
                self.panel_color(item,frame)
                
            if i == 3: # color item 
                self.panel_line_weight(item,frame)


            #label = gtk.Label(item_prop[4-i])
            #frame.add(label)
            #label.show()

            label = gtk.Label(bufferl)
            notebook.prepend_page(frame, label)
    
        # Set what page to start at (page 4)
        notebook.set_current_page(0)

        bbox = gtk.HButtonBox()
        vbox.pack_start(bbox, False, False, 0)
        layout=gtk.BUTTONBOX_END
        bbox.set_layout(layout)
        bbox.set_spacing(0)
        buttonok = gtk.Button(stock='gtk-ok')
        buttonok.connect("clicked", self.ok_click,buttonok,item)
        bbox.add(buttonok)
        buttonok.show()

        buttonClear = gtk.Button(stock='gtk-apply')
        bbox.add(buttonClear)
        #buttonClear.connect("clicked", self.clear_text,view1)
        buttonClear.show()
        bbox.show()
        
        def close_dialog(self,window,item):
            #itemPropertySelect.window = None
            
            
            window.destroy()
            #window.destroy()
            
        buttonClose = gtk.Button(stock='gtk-close')
        buttonClose.connect("clicked",close_dialog,self.window,item)
        bbox.add(buttonClose)
        buttonClose.show()
        
       
        
        
        table.show()
        self.window.show()
        self.window.set_modal(True)
        
    def ok_click(self,widget,button,item):
        item.set_data ('itemProp',self.ItemProperty)
        print "click ok and color rgba is  ",self.ItemProperty['rgbaColor']
        self.window.destroy()
        
    def panel_color(self,item,frame):
        
        #myData = item.get_data ('itemProp')
        color = self.ItemProperty['color'] 
        #color = myData['color'] 
        
        vbox = gtk.VBox(True, 0)
        vbox.set_border_width(2)
        frame.add(vbox)
        vbox.show()

        # SET Alpha color level 
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 1)
        hbox.show()
        
        label = gtk.Label("Alpha level :")
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, True, True, 0)
        label.show()
        
        adj_hscale = gtk.Adjustment(1.0, 1.0, 255, 1.0, 5.0, 0.0)
        hscale= gtk.HScale(adj_hscale)
        hscale.set_size_request(140, -1)
        hscale.set_value_pos(gtk.POS_RIGHT)
        hscale.set_draw_value(False) 
        hscale.set_digits(1)
        hbox.pack_start(hscale, True, True, 0)
        hscale.show()
        
        adj_spin = gtk.Adjustment(1.0, 1.0, 255, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj_spin, 0, 0)
        spinner.set_wrap(True)
        hbox.pack_start(spinner, False, True, 0)
        spinner.show()
        
        if self.ItemProperty.has_key('rgbaColor'):
            if self.ItemProperty['rgbaColor'] is not None:
                color_rgba = self.ItemProperty['color']
                color_rgba = color_rgba.replace('#','')
                    #color = hex(hex_alpha+color)
                color_rgba = int(color_rgba,16)
                val = self.ItemProperty['rgbaColor'] - (color_rgba*256)
                print 'alpha value ',self.ItemProperty['rgbaColor']
                print 'diff ' ,val
                hscale.set_value(val)
                spinner.set_value(val)
            
        
        
        global cval # temp value of spinner and hscale
        adj_spin.connect("value_changed", self.change_alpha_level, spinner,hscale, item,"spinner",color)
        adj_hscale.connect("value_changed", self.change_alpha_level, spinner,hscale, item,"hscale",color)
        
        
        
        
        
        # SET Conner curve level 2
        
        #selectItem.set_data ('itemProp',myData)
        #color = item.prop.fill_color
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 1)
        hbox.show()
        
        txt = "Set color: " + str(color)
        label = gtk.Label(txt)
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, True, True, 0)
        label.show()
        
        adj = gtk.Adjustment(0, 0, 255, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        hbox.pack_start(spinner, False, True, 0)
        spinner.show()
        
    def change_alpha_level(self,widget,spinner,hscale,item,widget_active,color):
        global cval
        if widget_active =="spinner":
            cval = int(spinner.get_value())
            if cval != hscale.get_value():
                hscale.set_value(cval)
                hex_alpha = hex(cval)
                if len(hex_alpha)<4:
                    hex_alpha = '0'+hex_alpha[2:3]
                else:
                    hex_alpha = hex_alpha[2:4]
                    
                #print "GET COLOR %s alpha Hex = %s : %s  full " % (color,hex_alpha,widget_active),
                color = color.replace('#','')
                #color = hex(hex_alpha+color)
                color = int(color,16)*256 + cval
                #print hex(color)
                item.props.fill_color_rgba = color#0x3cb37180#0x7fff9c00
                self.ItemProperty['rgbaColor']= color
        else: # The hscale click active 
            cval = int(hscale.get_value())
            if cval != spinner.get_value():
                spinner.set_value(cval)
                #print "GET COLOR %s alpha Hex = %s : %s " % (color,hex(cval),widget_active)
                
        
    def change_curve_level(self,widget,spinner,hscale,item,widget_active):
        if widget_active =="spinner":
            cval = spinner.get_value()
            hscale.set_value(cval)
        else:
            cval = hscale.get_value()
            spinner.set_value(cval)
            
        item.props.radius_x = cval
        item.props.radius_y = cval
        #print "change curve level ",widget_active
            
        
    def panel_line_weight(self,item,frame):
        vbox = gtk.VBox(True, 0)
        vbox.set_border_width(2)
        frame.add(vbox)
        vbox.show()

        # SET Alpha color level 
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 1)
        hbox.show()
        
        label = gtk.Label("Line width :")
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, True, True, 0)
        label.show()
        
        adj = gtk.Adjustment(0, 0, 20, 1.0, 5.0, 0.0)
        spinner = gtk.SpinButton(adj, 0, 0)
        spinner.set_wrap(True)
        hbox.pack_start(spinner, False, True, 0)
        spinner.show()
        spinner.set_value(item.props.line_width)
        adj.connect("value_changed", self.change_line_weight, spinner, item)
        
        # SET Conner curve level 
        rx = item.props.radius_x
        hbox = gtk.HBox(False, 0)
        vbox.pack_start(hbox, True, True, 1)
        hbox.show()
        
        label = gtk.Label("Curve level :")
        label.set_alignment(0, 0.5)
        hbox.pack_start(label, True, True, 0)
        label.show()
        
        adj_hscale = gtk.Adjustment(0, 0, 50, 1.0, 5.0, 0.0)
        hscale= gtk.HScale(adj_hscale)
        hscale.set_size_request(140, -1)
        hscale.set_value_pos(gtk.POS_RIGHT)
        hscale.set_draw_value(False) 
        hscale.set_digits(1)
        hscale.set_value(rx)
        hbox.pack_start(hscale, True, True, 0)
        hscale.show()
        
        adj_spin = gtk.Adjustment(0, 0, 50, 1.0, 5.0, 0.0)
        
        spinner = gtk.SpinButton(adj_spin, 0, 0)
        spinner.set_wrap(True)
        hbox.pack_start(spinner, False, True, 0)
        spinner.set_value(rx)
        spinner.show()
        
        adj_spin.connect("value_changed", self.change_curve_level, spinner,adj_hscale, item,"spinner")
        adj_hscale.connect("value_changed", self.change_curve_level, spinner,adj_hscale, item,"hscale")
        
    def change_line_weight(self,widget,spinner, item):
        cval = spinner.get_value()
        item.props.line_width  = cval
        return True
'''
def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    itemPropertySelect(None)
    main()'''
