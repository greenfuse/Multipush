import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class CellRendererProgressWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Multipush")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(bool, str, int, str)
        self.current_iter = self.liststore.append([False, "Computer1", 0, "network-offline"])
        self.liststore.append([False, "Computer2", 0, "network-idle"])
        self.liststore.append([False, "Computer3", 0, "network-transmit-receive"])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)
        column_toggle = Gtk.TreeViewColumn("Selected", renderer_toggle,
            active=0)
        treeview.append_column(column_toggle)

        renderer_text = Gtk.CellRendererText()
        column_computer = Gtk.TreeViewColumn("Conputer", renderer_text, text=1)
        treeview.append_column(column_computer)

        renderer_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress,
            pulse=2)
        treeview.append_column(column_progress)

        renderer_pixbuf = Gtk.CellRendererPixbuf()
        column_pixbuf = Gtk.TreeViewColumn("Status", renderer_pixbuf, icon_name=3)
        treeview.append_column(column_pixbuf)

        self.add(treeview)

        #self.timeout_id = GLib.timeout_add(100, self.on_timeout, None)

    def on_cell_toggled(self, widget, path):
        self.liststore[path][0] = not self.liststore[path][0]

    def on_timeout(self, user_data):
        new_value = self.liststore[self.current_iter][1] + 1
        if new_value > 100:
            self.current_iter = self.liststore.iter_next(self.current_iter)
            if self.current_iter is None:
                self.reset_model()
            new_value = self.liststore[self.current_iter][1] + 1

        self.liststore[self.current_iter][1] = new_value
        return True

    def reset_model(self):
        for row in self.liststore:
            row[1] = 0
        self.current_iter = self.liststore.get_iter_first()
        

    
    def printTotals(transferred, toBeTransferred):
        '''
        To provide progress information for sftp file transfer use the 
        optional callback parameter of the put function

        '''        
        #print "Transferred: {0}\tOut of: {1}".format(transferred, toBeTransferred)

    #sftp.put("myfile","myRemoteFile",callback=printTotals)


win = CellRendererProgressWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
