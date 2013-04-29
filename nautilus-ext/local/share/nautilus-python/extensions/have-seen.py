#!/usr/bin/python

"""Have Seen Menu Extension."""

import urllib2
import urllib
import os
import httplib2
import simplejson
import re

from gi.repository import Nautilus, GObject, Gio, Gtk

SERVER_ADDRESS = "127.0.0.1"
REST_FETCH_URL = "http://127.0.0.1/~user/have-seen/api/fetch.rb"
REST_APPEND_URL= "http://127.0.0.1/~user/have-seen/api/append.rb"
LOCAL_FILE_FOR_APPEND = "/tmp/.have-seen.txt"
#sftp://user@127.0.0.1/home/user/dir/file.name.long.one.999-UPER.
REGEXP_URI = "^sftp:\/\/(\w+)@([\.\d]+)\/(.+)$"
LABEL_HAVE_SEEN = "Matyta"#Lithuanian Have seen

class HaveSeenMenuExtension(GObject.GObject, Nautilus.MenuProvider):

	
    def __init__(self):
        pass


    # Sync folders
    def syncFoldersWithRemote(self, parent_uri):
        req = urllib2.Request(REST_FETCH_URL, None, {'content-type':'application/json', 'accept':'application/json'})
        opener = urllib2.build_opener()
        f = opener.open(req)
        json_object = simplejson.load(f)
        for value in json_object:
			#print "[syncFoldersWithRemote]" + parent_uri+"/"+value # example usage
			haveSeenFile = parent_uri+"/"+value.encode('utf-8')
			self.markAsSeen(haveSeenFile)
	
	#add emebeded icon
    def markAsSeen(self, file_uri):
        command = "gvfs-set-attribute \"" + file_uri + "\" -t stringv metadata::emblems OK"
        print "[markAsSeen]"+command
        os.system(command)
        
    #store file localy 
    def storeLocaly(self, file_uri):
        open(os.path.expanduser(LOCAL_FILE_FOR_APPEND),"a+b").write(file_uri+"\n")
        print "[storeLocaly]"+LOCAL_FILE_FOR_APPEND

    def storeRemotly(self, file_uri, file_name):
        userName = ""
        match = re.search(REGEXP_URI, file_uri)
        if match:
            userName = match.group(1)
        f = { 'user' : userName, 'fullPath' : file_uri, 'fileName':file_name}
        url_enc_param = urllib.urlencode(f)
        resp, content = httplib2.Http().request(REST_APPEND_URL+"?"+url_enc_param)
        print "[menu_activate_cb]", url_enc_param


	# main method  to visualize "HaveSeen" property and store information localy and remotely
    def menu_activate_cb(self, menu, file):
        print "[menu_activate_cb]",file.get_uri()

        dialog = Gtk.MessageDialog(message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.CLOSE,
                               text='%s: "%s" ' % (LABEL_HAVE_SEEN,file.get_uri()))
        dialog.show()
        dialog.show_all()
        response = dialog.run()
        dialog.destroy()
        self.markAsSeen(file.get_uri())
        self.storeLocaly(file.get_uri())
        self.storeRemotly(file.get_uri(),file.get_name())
        self.syncFoldersWithRemote(file.get_parent_info().get_uri())

        
     

        
	#### Provider implementation
    def get_file_items(self, window, files):
        if len(files) != 1:
            return
        
        file = files[0]

        item = Nautilus.MenuItem(
            name="HaveSeenMenuExtension::Have_Seen_File",
            label="%s: %s" % (LABEL_HAVE_SEEN,file.get_name()),
            tip="%s: %s" % (LABEL_HAVE_SEEN,file.get_name())
        )

        match = re.search(REGEXP_URI, file.get_uri())
        if match:
            item.connect('activate', self.menu_activate_cb, file)
            return [item]
        return []
