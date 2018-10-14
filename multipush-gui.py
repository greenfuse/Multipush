#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf
import multipush

#import dialogs
#from dialogs import ComputerList

class Multipush(object):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file('multipush.glade')
        self.builder.connect_signals(self)
        go = self.builder.get_object
        
        # Window widgets
        self.window = go("window")
        self.treeview = go('treeview')
        self.liststore_computers = go('liststore_computers')
        self.combobox = go('combobox') 
        self.label_user = go("label_user")
        # 'Computer List' Dialog Widgets
        self.dialog_cl = go("dialog_cl")
        self.treeview_cl = go('treeview_cl')
        self.liststore_computers_cl = go('liststore_computers_cl')        
        self.combobox_cl = go('combobox_cl')
        self.liststore_combo_cl = go('liststore_combo_cl')        

        # 'New List' Dialog Widgets
        self.dialog_nl = go("dialog_nl")
        self.entry_listname_nl = go("entry_listname_nl")
        self.entry_username_nl = go("entry_username_nl")
        self.textview_nl = go("textview_nl")
        
        # 'Add Computer' Dialog Widgets
        self.dialog_add = go("dialog_add")
        self.textview_add = go("textview_add")

        #Populate the GUI with lists
        self.computerlists = multipush.get_computerlists()
        self.load_lists()

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


        #self.window.connect('delete-event', lambda x, y: Gtk.main_quit())
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

    def on_combobox_changed(self, widget):
        listname = widget.get_active_text()
        username = self.computerlists[listname]['username']
        usertext = "Connecting as: " + username
        self.label_user.set_text(usertext)
        print("Now populate the list")
        
    def on_button_file_clicked(self, widget):
        print("file selection")
        
    def on_button_dest_clicked(self, widget):
        print("Select Destination Directory")
               
    def on_button_del_clicked(self, widget):
        print("Delete")

    #   !!!!  Opens the dialog  !!!!!
    def on_button_edit_clicked(self, widget):
        print("Edit computer lists")
        self.load_lists_cl()
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

    # ----- 'Computer Lists' Dialog signal handlers -----

    def on_button_new_clicked(self, widget):
        print("New Computer List")
        response = self.dialog_nl.run()
        print(response)
        self.dialog_nl.hide()
        
    def on_button_del_clicked(self, widget):
        print("Delete")
        
    def on_button_add_clicked(self, widget):
        print("Add Computers")
        response = self.dialog_add.run()
        print(response)
        self.dialog_add.hide()
        
    def on_button_rem_clicked(self, widget):
        print("Remove")
        
    def on_button_ref_clicked(self, widget):
        print("Refresh")    

    def on_button_auth_clicked(self, widget):
        print("Authorise")  

    def on_combobox_cl_changed(self, widget):
        print("populate the computer list")

    # Populate lists in the Main Window GUI 
    def load_lists(self):
        '''Populate the main window drop down list
        with the names of computer lists'''
        listnames = tuple(self.computerlists.keys())
        for listname in listnames:
            self.combobox.append_text(listname)
            
        self.combobox.set_active(0)    
    
    def load_lists_cl(self):
        '''Populate the computerlist dialog drop down list
        with the names of computer lists'''
        listnames = tuple(self.computerlists.keys())
        for listname in listnames:
            self.combobox_cl.append_text(listname)
        self.combobox_cl.set_active(0)    



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
