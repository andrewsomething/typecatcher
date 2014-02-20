# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2014 Andrew Starr-Bochicchio <a.starr.b@gmail.com>
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

from gi.repository import Gtk, Gio # pylint: disable=E0611

from typecatcher import TypeCatcherWindow
from . helpers import get_builder, add_simple_action, running_gnome_shell

class TypeCatcherApplication(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self, application_id="apps.andrewsomething.typecatcher",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.on_activate)

    def on_activate(self, data=None):
        self.window = TypeCatcherWindow.TypeCatcherWindow()
        # Use ApplicationMenu under GNOME
        if running_gnome_shell():
            self.create_app_menu()
        self.add_window(self.window)
        self.window.show()

    def create_app_menu(self):
        builder = get_builder('AppMenu')
        appmenu = builder.get_object('appmenu')
        self.set_app_menu(appmenu)
        add_simple_action(self, 'save_as', 
            self.on_save_as_activated)
        add_simple_action(self, 'help', 
            self.on_help_activated)
        add_simple_action(self, 'about', 
            self.on_about_activated)
        add_simple_action(self, 'quit', 
            self.on_quit_activated)

    def on_save_as_activated(self, action, data=None):
        self.window.on_mnu_save_as_activate(action)

    def on_help_activated(self, action, data=None):
        self.window.on_mnu_contents_activate(action)

    def on_about_activated(self, action, data=None):
        self.window.on_mnu_about_activate(action)

    def on_quit_activated(self, action, data=None):
        self.window.on_mnu_close_activate(action)
