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
        self.checkbutton_all = go('checkbutton_all')
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
        self.label_user_cl = go("label_user_cl")
        
        # 'Add Computer' Dialog Widgets
        self.dialog_add = go("dialog_add")
        self.textview_add = go("textview_add")
        
        # Prepare GUI lists
        self.computerlists = multipush.get_computerlists()        
        self.create_columns()
        self.create_columns_cl()
        self.load_lists()
        self.window.show()
        
        #self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

    # ----- Window signal handlers -----

    def on_window_destroy(self, widget):
        Gtk.main_quit()
    
    def on_radio_file_group_changed(self, widget):
        print("selected copy file")
        
    def on_radio_cmd_group_changed(self, widget):
        print("selected run command")        
        
    def on_checkbutton_all_toggled(self, widget):
        print("toggle selection to all or none")

    def on_combobox_changed(self, widget):
        '''
        When the computer list is selected, list the computers
        '''
        listname = widget.get_active_text()
        username = self.computerlists[listname]['username']
        usertext = "Connecting as: " + username
        self.label_user.set_text(usertext)
        self.list_computers(listname)
        
    def on_button_file_clicked(self, widget):
        print("file selection")
        
    def on_button_dest_clicked(self, widget):
        print("Select Destination Directory")
               
    def on_button_del_clicked(self, widget):
        print("Delete")

    def on_button_edit_clicked(self, widget):
        '''
        Opens the dialog window for managing computer lists
        '''
        self.combobox_cl.remove_all()
        self.liststore_computers_cl.clear()
        self.load_lists_cl()
        response = self.dialog_cl.run()
        print(response)
        self.dialog_cl.hide()
    
    def on_checkbutton_all_toggled(self, widget):
        active_status = widget.get_active()
        for row in self.liststore_computers:
            row[0] = active_status
        self.current_iter = self.liststore_computers.get_iter_first()
                            
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
        print("delete")
                    
    def on_button_add_clicked(self, widget):
        print("Add Computers")
        response = self.dialog_add.run()
        print(response)
        self.dialog_add.hide()
        
    def on_button_rem_clicked(self, widget):
        selection = self.treeview_cl.get_selection()
        model, paths = selection.get_selected_rows()

        for path in paths:
           iter = model.get_iter(path)
           model.remove(iter)

    def on_button_ref_clicked(self, widget):
        print("Refresh")    

    def on_button_auth_clicked(self, widget):
        print("Authorise")  

    def on_combobox_cl_changed(self, widget):
        '''
        When the computer list is selected, list the computers
        '''
        listname = widget.get_active_text()
        username = self.computerlists[listname]['username']
        usertext = "Connecting as: " + username
        self.label_user_cl.set_text(usertext)
        self.list_computers_cl(listname)
        
    # --- Functions to populate the GUI lists --- 

    def load_lists(self):
        '''Populate the main window drop down list
        with the names of computer lists'''
        listnames = tuple(self.computerlists.keys())
        for listname in listnames:
            self.combobox.append_text(listname)
            
        self.combobox.set_active(0)    

    def list_computers(self, listname):
        self.checkbutton_all.set_active(False)
        self.liststore_computers.clear()
        computers = self.computerlists[listname]['computers']
        pixel = self.get_colour('grey')
        for computer in computers:
            list_row = [False, pixel, computer, 0]
            self.liststore_computers.append(list_row)        

    def create_columns(self) :
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

    # --- Functions to populate the computer list dialog ---
    
    def load_lists_cl(self):
        '''Populate the computerlist dialog drop down list
        with the names of computer lists'''
        listnames = tuple(self.computerlists.keys())
        for listname in listnames:
            self.combobox_cl.append_text(listname)
        self.combobox_cl.set_active(0)


    def list_computers_cl(self, listname):   
        self.liststore_computers_cl.clear()
        computers = self.computerlists[listname]['computers']
        pixel = self.get_colour('grey')
        for computer in computers:
            list_row = [pixel, computer]
            self.liststore_computers_cl.append(list_row)        

    def create_columns_cl(self) :
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("", renderer_pixbuf, pixbuf=0)
        self.treeview_cl.append_column(column_pixbuf)
        
        renderer_text = Gtk.CellRendererText()
        column_computer = Gtk.TreeViewColumn("Conputer", renderer_text, text=1)
        self.treeview_cl.append_column(column_computer)

    def get_colour(self, colour):
        #create solid colour image
        colour_hashes = {
        'red': 0xffbbbbff,
        'green': 0xa3f079ff,
        'yellow': 0xffff56ff,
        'grey': 0x808080ff
        }
        
        if colour not in list(colour_hashes.keys()):
            colour = 'grey'

        pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixel.fill(colour_hashes[colour])   
        
        return pixel     
    
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
