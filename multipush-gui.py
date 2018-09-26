#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

#import dialogs
#from dialogs import ComputerList

class Multipush(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('multipush.glade')
        self.builder.connect_signals(self)
        
        go = self.builder.get_object
        self.window = go("window")
        self.dialog_cl = go("dialog_cl")
        self.treeview = go('treeview')
        self.liststore_computers = go('liststore_computers')
        self.liststore_combo = go('liststore_combo')
        self.combobox = go('combobox') 
        
        test_list = [
              ["List1", "User1"]
            , ["List2", "User2"]
            , ["LongerList3", "User3"]
            ]
        for list_item in test_list:
            self.liststore_combo.append(list_item)

        self.combobox.set_active(0)    
            
        #create solid colour image
        red = 0xffbbbbff
        green = 0xa3f079ff
        yellow = 0xffff56ff
        grey = 0x808080ff
        
        red_pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        red_pixel.fill(red)   
        
        green_pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        green_pixel.fill(green)  
        
        yellow_pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        yellow_pixel.fill(yellow)  
                
        grey_pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        grey_pixel.fill(grey)  
                    
        test_rows = [
             [False, red_pixel, 'Computer1', 0]
            ,[False, green_pixel, 'Computer2', 0]
            ,[False, yellow_pixel, 'Computer3', 0]
            ,[False, grey_pixel, 'Computer4', 0]
            ]
            
        for test_row in test_rows:
            self.liststore_computers.append(test_row)        

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("", renderer_toggle,
            active=0)
        self.treeview.append_column(column_toggle)

        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("", renderer_pixbuf, pixbuf=1)
        self.treeview.append_column(column_pixbuf)
        
        renderer_text = Gtk.CellRendererText()
        column_computer = Gtk.TreeViewColumn("Conputer", renderer_text, text=2)
        self.treeview.append_column(column_computer)

        renderer_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress,
            value=3)
        self.treeview.append_column(column_progress)


        self.window.connect('delete-event', lambda x, y: Gtk.main_quit())
        self.window.show()
        
        #self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

# ----- Window signal handlers -----

    def on_window_destroy(self, widget):
        Gtk.main_quit()
    
    def on_radio_file_group_changed(self, widget):
        print("copy file")
        
    def on_radio_cmd_group_changed(self, widget):
        print("run command")        
        
    def on_checkbutton_all_toggled(self, widget):
        print("toggle selection to all or none")

    def combobox_changed_cb(self, widget):
        print("list the computers")

    def on_button_file_clicked(self, widget):
        print("file selection")
        
    def on_button_dest_clicked(self, widget):
        print("Select Destination Directory")
               
    def on_button_del_clicked(self, widget):
        print("Delete")

    def on_button_edit_clicked(self, widget):
        print("Edit computer lists")
        response = self.dialog_cl.run()
        print(response)
        self.dialog_cl.hide()
                    
    def on_cell_toggled(self, widget, path):
        self.liststore_computers[path][0] = not self.liststore_computers[path][0]

    def on_button_apply_clicked(self, widget):
        print("Apply")
        
    def on_button_stop_clicked(self, widget):
        print("Stop")
        
    def on_button_quit_clicked(self, widget):
        print("Bye bye")
        Gtk.main_quit()

# ----- Dialog signal handlers -----

    def on_button_new_clicked(self, widget):
        print("New")
            
    def on_button_del_clicked(self, widget):
        print("Delete")
        
    def on_button_add_clicked(self, widget):
        print("Add")
        
    def on_button_rem_clicked(self, widget):
        print("Remove")
        
    def on_button_ref_clicked(self, widget):
        print("Refresh")    

    def on_button_auth_clicked(self, widget):
        print("Authorise")  



    def reset_model(self):
        for row in self.liststore_computers:
            row[1] = 0
        self.current_iter = self.liststore_computers.get_iter_first()
        

    
    def printTotals(transferred, toBeTransferred):
        '''
        To provide progress information for sftp file transfer use the 
        optional callback parameter of the put function

        '''        
        #print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)

        #sftp.put("myfile","myRemoteFile",callback=printTotals)


if __name__ == "__main__":
    gui = Multipush()
    Gtk.main()
