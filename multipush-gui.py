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
        self.treeselection = self.treeview.get_selection()
        self.treeselection.set_select_function(self.set_selectable)
        self.combobox = go('combobox') 
        self.checkbutton_all = go('checkbutton_all')
        self.label_user = go("label_user")
        
        # 'Computer List' dialog widgets
        self.dialog_cl = go("dialog_cl")
        self.headerbar_cl = go("headerbar_cl")
        self.entry_listname_cl = go("entry_listname_cl")
        self.entry_username_cl = go("entry_username_cl")
        self.textview_cl = go("textview_cl")
        
        # Authorisation dialog widgets
        self.dialog_auth = go('dialog_auth')
        self.headerbar_auth = go('headerbar_auth')
        self.entry_auth = go('entry_auth')
        
        # Prepare GUI lists
        self.computerlists = multipush.get_computerlists()       
        self.create_columns()
        self.load_lists()
        self.window.show()
        
        #self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

    # ----- Window signal handlers -----

    def on_window_destroy(self, widget):
        Gtk.main_quit()

    def set_selectable(self, treeselection, model, path, current):
        connected = model[path][4]
        # if not connected:
        #     model[path][0] = False
        return connected
    
    def on_radio_file_group_changed(self, widget):
        print("selected copy file")
        
    def on_radio_cmd_group_changed(self, widget):
        print("selected run command")        
        
    # def on_checkbutton_all_toggled(self, widget):
    #    print("toggle selection to all or none")

    def on_combobox_changed(self, widget):
        '''
        When the computer list is selected, list the computers
        '''
        listname = widget.get_active_text()
        self.checkbutton_all.set_active(False)
        self.liststore_computers.clear()
        if listname:
            username = self.computerlists[listname]['username']
            usertext = "Connecting as: " + username
            self.label_user.set_text(usertext)
            self.list_computers(listname)
        
    def on_button_file_clicked(self, widget):
        print("file selection")
        
    def on_button_to_clicked(self, widget):
        print("Select Destination Directory")


    def on_button_edit_clicked(self, widget):
        '''
        Opens the dialog window for managing computer lists
        '''
        self.headerbar_cl.set_subtitle("Edit")
        listname = self.combobox.get_active_text()
        username = self.computerlists[listname]['username']
        computers = self.computerlists[listname]['computers']
        self.entry_listname_cl.set_text(listname)
        self.entry_username_cl.set_text(username)
        textbuffer = self.textview_cl.get_buffer()
        textbuffer.set_text("")
        for computer in computers:
            newline = computer +  '\n'
            end_iter = textbuffer.get_end_iter()
            textbuffer.insert(end_iter, newline)
        
        response = self.dialog_cl.run()
        if response == Gtk.ResponseType.OK:
            self.update_lists()
        
        self.dialog_cl.hide()
                
    def on_button_del_clicked(self, widget):
        print("Delete")
        listname = self.combobox.get_active_text()
        self.computerlists.pop(listname)
        multipush.write_computerlists(self.computerlists)
        self.load_lists()
        

    def on_button_new_clicked(self, widget):
        self.headerbar_cl.set_subtitle("New")
        self.entry_listname_cl.set_text("")
        self.entry_username_cl.set_text("")
        textbuffer = self.textview_cl.get_buffer()
        textbuffer.set_text("")
        response = self.dialog_cl.run()
        if response == Gtk.ResponseType.OK:
            self.update_lists()
        
        self.dialog_cl.hide()         


    def on_button_auth_clicked(self, widget):
        multipush.local_keys()
        listname = self.combobox.get_active_text()
        username = self.computerlists[listname]['username']
        self.headerbar_auth.set_subtitle(username)        
        response = self.dialog_auth.run()
        self.dialog_auth.hide()
        self.entry_auth.set_text("")
        if response == Gtk.ResponseType.OK:
            password = self.entry_auth.get_text()
            computers = self.get_selected_computers()
            multipush.add_public_key(username, password, computers)
        
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
         
    def on_button_ref_clicked(self, widget):
        self.check_computer_status()    
        
    def on_button_quit_clicked(self, widget):
        print("Bye bye")
        Gtk.main_quit()
        
    # --- Functions to populate the GUI lists --- 

    def load_lists(self):
        '''Populate the main window drop down list
        with the names of computer lists'''
        self.combobox.remove_all()
        listnames = tuple(self.computerlists.keys())
        for listname in listnames:
            self.combobox.append_text(listname)
            
        self.combobox.set_active(0)    

    def list_computers(self, listname):
        computers = self.computerlists[listname]['computers']
        pixel = self.get_colour('grey')
        for computer in computers:
            list_row = [False, pixel, computer, 0, False]
            self.liststore_computers.append(list_row)
        self.check_computer_status()

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

        renderer_toggle1 = Gtk.CellRendererToggle()
        renderer_toggle1.connect("toggled", self.on_cell_toggled)
        column_toggle1 = Gtk.TreeViewColumn("Connected", renderer_toggle1,
            active=4)
        column_toggle1.set_visible(False)
        column_toggle1.set_cell_data_func(renderer_toggle1, self.set_toggle)
        self.treeview.append_column(column_toggle1)

    def set_toggle(self, column, cell, model, iter, user_data):
        connected = model.get_value(iter, 4)
        #print(connected)
        if not connected:
            cell.set_activatable(False)
            model[iter][0] = False
            

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

    def update_lists(self):
            # get the details of the new list
            subtitle = self.headerbar_cl.get_subtitle()
            username = self.entry_username_cl.get_text()
            listname = self.entry_listname_cl.get_text()
            if subtitle == 'New' and listname in self.computerlists: 
                print("Confirm Overwrite")

            textbuffer = self.textview_cl.get_buffer()
            start_iter = textbuffer.get_start_iter()
            end_iter = textbuffer.get_end_iter()
            computerlist = textbuffer.get_text(start_iter, end_iter, False)
            computers = [y for y in (x.strip() for x in computerlist.splitlines()) if y]
            # ensure that none of the above is empty
            if not all([username, listname, computers]):
                print ("Need to fill in all fields")

            else:
                # update the dictionary of lists
 
                computerlist = {
                    listname: {
                        'username': username, 
                        'computers': computers
                        }
                    }
                    
                self.computerlists.update(computerlist)  
                # update the conputers.yml file
                multipush.write_computerlists(self.computerlists)
                # update the GUI main window
                listnames = tuple(self.computerlists.keys())
                position = listnames.index(listname)
                self.load_lists()
                self.combobox.set_active(position)

    def get_selected_computers(self):
        computers = []
        for row in self.liststore_computers:
            if row[0]:
                computers.append(row[2])
        return computers
        
    def check_computer_status(self):
        #rownumber = 0
        for row in self.liststore_computers:
            computer = row[2]
            status = multipush.check_computer_status(computer)
            print((computer, status))
            if status == 'open':
                #set the toggle as available
                # can't work out how to do this
                row[0] = True
                
                #set the colour to green
                pixel = self.get_colour('green')
                row[1] = pixel
                row[4] = True

                #selection  = self.treeview.get_selection()
                #selection.select_path(rownumber)
                #selection.set_select_function(True)
                
            else:
                #set the toggle as unavailable and off
                row[0] = False
                #set the colour to grey
                pixel = self.get_colour('grey')
                row[1] = pixel
                row[4] = False

                #row.set_select_function(False)
                #selection  = self.treeview.get_selection()
                #selection.select_path(rownumber)
                #selection.set_select_function(lambda )
            #rownumber += 1
    
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
    
