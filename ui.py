#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import global_var
import gobject
import os


def register_iconsets(icon_info):
        
        try:
            iconfactory = gtk.IconFactory()
            stock_ids = gtk.stock_list_ids()
            img_dir = os.path.join(os.path.dirname(__file__), 'images')
            for stock_id, file in icon_info:
              # only load image files when our stock_id is not present
                img_path = os.path.join(img_dir, file)
                if stock_id not in stock_ids:
                    pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)
                    transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
                    icon_set = gtk.IconSet(transparent)
                    iconfactory.add(stock_id, icon_set)
            iconfactory.add_default()
        except gobject.GError, error:
            print 'failed to load GTK logo for toolbar'


class UIManager(gtk.Window):
    ui0 = '''<ui>
    <menubar name="MenuBar">
      <menu action="File">
        <menuitem action="New"/>
        <menuitem action="Close"/>
        <separator name="sep0"/>
        <menuitem action="Exit"/>
      </menu>
      <menu action="Edit">
        <menuitem action="Delete"/>
      </menu>
      <menu action="Draw">
        <menuitem action="SELECT"/>
        <menuitem action="RECTANGLE"/>
        <menuitem action="PAN"/>
      </menu>
    </menubar>
    <toolbar name="Toolbar">
      <toolitem action="New"/>
      <separator/>
      <toolitem action="Delete"/>
      <separator name="sep1"/>
      <placeholder name="DrawItems">
        <toolitem action="SELECT"/>
        <toolitem action="RECTANGLE"/>
        <toolitem action="PAN"/>
      </placeholder>
    </toolbar>
    </ui>'''
    
    

    def __init__(self,window):
        #Register image to gtk-stock

        ''' This function registers our custom toolbar icons, so they
        can be themed.
        '''
        '''items = [('MY_RECT', '_GTK!', 0, 0, '')]
        # Register our stock items
        gtk.stock_add(items)'''

        # Add our custom icon factory to the list of defaults
        '''factory = gtk.IconFactory()
        factory.add_default()

        import os
        img_dir = os.path.join(os.path.dirname(__file__), 'images')
        img_path = os.path.join(img_dir, 'CreateRect.gif')
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file(img_path)

            # Register icon to accompany stock item

            # The gtk-logo-rgb icon has a white background, make it transparent
            # the call is wrapped to (gboolean, guchar, guchar, guchar)
            transparent = pixbuf.add_alpha(True, chr(255), chr(255),chr(255))
            icon_set = gtk.IconSet(transparent)
            factory.add('MY_RECT', icon_set)

        except gobject.GError, error:
            print 'failed to load GTK logo for toolbar'''''
        register_iconsets([('MY_RECT', 'CreateRect.gif'),
                     ('MY_SELECT', 'SelectionMode.gif'),('MY_ELLIPSE','CreateEllipse.gif')])

        
        global uimanager
        uimanager = gtk.UIManager()
        merge_id = 0
        accelgroup = uimanager.get_accel_group()
        window.add_accel_group(accelgroup)
        #menuUI = 


        # Create the base ActionGroup
        actiongroup0 = gtk.ActionGroup('UIMergeBase')

        actiongroup0.add_actions([('File', None, '_File'),
                                  ('Edit', None, '_Edit'),
                                  ('Draw', None, '_Draw')])
        uimanager.insert_action_group(actiongroup0, 0)

        # Create an ActionGroup
        actiongroup = gtk.ActionGroup('UIMergeBase')


        # Create a ToggleAction, etc.
        actiongroup.add_toggle_actions([('Delete', gtk.STOCK_DELETE, '_Delete', '<Control>d',
                                         'Delete the Object', self.Delete_cb)])

        # Create actions
        actiongroup.add_actions([('New', gtk.STOCK_NEW, '_New', None,
                                  'Crete new file', self.new_file), 
                                ('Close', gtk.STOCK_CLOSE, '_Close', None,
                                  'Close File', self.new_file), 
                                ('Exit', gtk.STOCK_QUIT, '_Exit', None,
                                  'Exit my program', self.quit),])
        #actiongroup.get_action('Quit').set_property('short-label', '_Quit')

        # Create some RadioActions
        '''image = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file('CreateRect.gif')
        image.set_from_pixbuf(pixbuf)'''

        #item.set_image(img)

        
        
        actiongroup.add_radio_actions([('SELECT',"MY_SELECT", '_SEL', None,
                                        'Selected', 0),
                                       ('RECTANGLE',"MY_RECT" , '_RECT',None,#gtk.STOCK_SELECT_ALL
                                        'Create Rectangle', 1),
                                       ('PAN', "MY_ELLIPSE", '_PAN', None,
                                        'PAN', 2),
                                       ], 0, self.Draw_cb)

        # Add the actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup, 1)

        # Add a UI description
        merge_id = uimanager.add_ui_from_string(UIManager.ui0)

        '''# Create another actiongroup and add actions
        actiongroup1 = gtk.ActionGroup('UIMergeExtras')
        actiongroup1.add_toggle_actions([('Loudness', None, '_Loudness',
                                          '<Control>l', 'Loudness Control',
                                          self.loudness_cb)])
        actiongroup1.add_actions([('New', gtk.STOCK_NEW, None, None,
                                   'New Settings', self.new_cb),
                                  ('Save', gtk.STOCK_SAVE, None, None,
                                   'Save Settings', self.save_cb)])
        # Adding radioactions to existing radioactions requires setting the
        # group and making sure the values are unique and the actions are
        # not active
        actiongroup1.add_radio_actions([('CB', None, '_CB', '<Control>c',
                                         'CB Radio', 3),
                                       ('Shortwave', None, 'Short_wave',
                                        '<Control>w', 'Shortwave Radio', 4),
                                       ], 3, self.Delete_cb)
        group = actiongroup.get_action('SELECT').get_group()[0]
        action = actiongroup1.get_action('CB')
        action.set_group(group)
        action.set_active(False)
        action = actiongroup1.get_action('Shortwave')
        action.set_group(group)
        action.set_active(False)
        # Add the extra actiongroup to the uimanager
        uimanager.insert_action_group(actiongroup1, 2)'''
        
        window.set_title('miniBAS v0.0.1')
        '''pixbuf = window.render_icon('gtk.MY_RECT', gtk.ICON_SIZE_MENU)
        window.set_icon(pixbuf)'''

        #print 'Pass UI  and get window title = ' + str(window.get_title())
        #return uimanager
        
    
    
    def createMenuBar(self):
        global uimanager
        menubar = uimanager.get_widget('/MenuBar')
        return menubar
    
    def createToolBar(self):
        global uimanager
        toolbar = uimanager.get_widget('/Toolbar')
        return toolbar
    
    def Delete_cb(self, action):
        pass
        # action has not toggled yet
        #text = ('Deleted', 'not Deleted')[action.get_active()==False]
        #self.Deletelabel.set_text('Edit is %s' % text)
        return

    def new_file(self, action):
        # action has not toggled yet
        print 'Press new file create'
        return
    
    def loudness_cb(self, action):
        # action has not toggled yet
        print 'Loudness toggled'
        return

    def Draw_cb(self,action, current):
        text = current.get_name()
        value = current.get_current_value()
        if value == 2:
            global_var.pan_select = True
        else:
            global_var.pan_select = False
            
        if value == 1:
            global_var.cmd_draw = 1 # commnad draw shape rectangle
        else:
            global_var.cmd_draw = 0
            
        print 'Radio band is %s '+text+'and value = '  + str(value)
        return

    def new_cb(self, b):
        print 'New settings'
        return

    def save_cb(self, b):
        print 'Save settings'
        return

    def quit(self,b):
        #print 'Quitting program'
        gtk.main_quit()
        

    def toggle_sensitivity(self, b):
        self.actiongroup.set_sensitive(b.get_active())
        return

    def toggle_visibility(self, b):
        self.actiongroup.set_visible(b.get_active())
        return

    def toggle_merged(self, b):
        if self.merge_id:
            self.uimanager.remove_ui(self.merge_id)
            self.merge_id = 0
        else:
            self.merge_id = self.uimanager.add_ui_from_string(self.ui1)
            print 'merge id:', self.merge_id
        print self.uimanager.get_ui()
        return

'''if __name__ == '__main__':
    ba = UIManager()
    gtk.main()'''
