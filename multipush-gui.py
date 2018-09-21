import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, GdkPixbuf

class Multipush(Gtk.Window):
    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file('gladebuildertest.glade')
        builder.connect_signals(self)

        self.liststore_computers = builder.get_object('liststore_computers')
        self.liststore_combo = builder.get_object('liststore_combo')
        
        #create solid colour image
        red = 0xffbbbbff
        green = 0xa3f079ff
        yellow = 0xffff56ff
        grey = 0x808080ff
        
        pixel = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, 16, 16)
        pixel.fill(grey)    
            
        test_rows = [[False, pixel, 'Computer1', 0]
            ,[False, pixel, 'Computer2', 0]
            ,[False, pixel, 'Computer3', 0]]
        for test_row in test_rows:
            self.liststore_computers.append(test_row)        

        
        self.treeview = builder.get_object('treeview')

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Select", renderer_toggle,
            active=0)
        self.treeview.append_column(column_toggle)

        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Status", renderer_pixbuf, pixbuf=1)
        self.treeview.append_column(column_pixbuf)
        
        renderer_text = Gtk.CellRendererText()
        column_computer = Gtk.TreeViewColumn("Conputer", renderer_text, text=2)
        self.treeview.append_column(column_computer)

        renderer_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress,
            value=3)
        self.treeview.append_column(column_progress)



        test_list = [["List1"], ["List2"], ["List3"]]
        for list_item in test_list:
            self.liststore_combo.append(list_item)
        
        window = builder.get_object('window')
        window.show_all()
        
        #self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

    def on_cell_toggled(self, widget, path):
        self.liststore_computers[path][0] = not self.liststore_computers[path][0]
    
    def on_radio_file_group_changed(self, widget):
        print("")
        
    def on_radio_cmd_group_changed(self, widget):
        print("")        
        
    def on_checkbutton_all_toggled(self, widget):
        print("toggle selection to all or none")

    def combo_computers_changed_cb(self, widget):
        print("")

    def on_button_file_clicked(self, widget):
        print("file selection")
        
    def on_button_computers_clicked(self, widget):
        print("")

    def on_button_auth_clicked(self, widget):
        print("open authorisation management window")
    
    def on_button_add_clicked(self, widget):
        print("")
    
    def on_button_apply_clicked(self, widget):
        print("")
        
    def on_button_stop_clicked(self, widget):
        print("")
        
    def on_button_quit_clicked(self, widget):
        print("")
        Gtk.main_quit()
        
    def on_timeout(self, user_data):
        new_value = self.liststore_computers[self.current_iter][1] + 1
        if new_value > 100:
            self.current_iter = self.liststore_computers.iter_next(self.current_iter)
            if self.current_iter is None:
                self.reset_model()
            new_value = self.liststore_computers[self.current_iter][1] + 1

        self.liststore_computers[self.current_iter][1] = new_value
        return True

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
    Multipush()
    Gtk.main()
