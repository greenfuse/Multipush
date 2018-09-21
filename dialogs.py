#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf

class ComputerList(Gtk.Dialog):
    def __init__(self, parent):
        builder = Gtk.Builder()
        builder.add_from_file('computerlists.glade')
        builder.connect_signals(self)

        self.treeview = builder.get_object('treeview')

        #create solid colour image
        red    = 0xffbbbbff
        green  = 0xa3f079ff
        yellow = 0xffff56ff
        grey   = 0x808080ff
        
        pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixel.fill(grey)    
        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Status", renderer_pixbuf, pixbuf=0)
        self.treeview.append_column(column_pixbuf)
        
        renderer_text = Gtk.CellRendererText()
        column_computer = Gtk.TreeViewColumn("Conputer", renderer_text, text=1)
        self.treeview.append_column(column_computer)

        #test_list = [["List1"], ["List2"], ["List3"]]
        #for list_item in test_list:
        #    self.liststore_combo.append(list_item)
        
        dialog = builder.get_object('dialog')
        dialog.show_all()

    def on_button_ok_clicked(self, widget):
        print("Ok")
        
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

 
