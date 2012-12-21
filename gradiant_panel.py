import pygtk
pygtk.require('2.0')
import gtk
import global_var

class gradiantPanelProperty:
    def createGradiantWidget(self):
        
        frame = gtk.Frame('Gradiant')
        frame.set_border_width(0)
        frame.set_size_request(200, 400)
        frame.show()
        label = gtk.Label("Gradiant Edit")
        label.show()
        
        vbox = gtk.VBox(False, 5)
        
        hbox = gtk.HBox(False,0)
        hbox.pack_start(label,False,True,0)
        hbox.show()
        
        vbox.pack_start(hbox,False,True,0)
        
        #label.show()
        frame.add(vbox)
        vbox.show()
        
        return frame