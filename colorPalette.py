import goocanvas

import gobject
import gtk
import gtk.gdk

import global_var

class CreatPalette(goocanvas.Canvas):
    """PyGTK widget that draws dot graphs."""


    #pan_select = False
    def __init__(self):
        goocanvas.Canvas.__init__(self)
        self.set_flags(gtk.CAN_FOCUS)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK)
        #self.connect("button-press-event", self.on_button_press)
        #self.connect("button-release-event", self.on_button_release)
        #self.connect("motion-notify-event", self.on_motion_notify)
        #self.connect("scroll-event", self.on_scroll)

        #self.connect("set-scroll-adjustments", self.on_set_scroll_adjustments)
        self.hadjustment = None
        self.vadjustment = None
       
        self.props.anchor = gtk.ANCHOR_CENTER
       
        '''self.connect("size-allocate", self.on_size_allocate)
       
        self.zoom_to_fit_on_resize = False
        self.animation = NoAnimation(self)
        self.drag_action = NullAction(self)
        self.presstime = None'''
        #root = self.get_root_item()
        #box_color(self,10,10,20,20,'red','box1')
                        
    #canvas.set_data(name, item)
        