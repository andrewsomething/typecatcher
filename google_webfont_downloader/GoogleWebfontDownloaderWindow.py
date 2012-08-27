# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2012 Andrew Starr-Bochicchio <a.starr.b@gmail.com>
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

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
from gi.repository import WebKit
import itertools, re
import logging
logger = logging.getLogger('google_webfont_downloader')

from google_webfont_downloader_lib import Window
from google_webfont_downloader.AboutGoogleWebfontDownloaderDialog import AboutGoogleWebfontDownloaderDialog
from google_webfont_downloader.PreferencesGoogleWebfontDownloaderDialog import PreferencesGoogleWebfontDownloaderDialog
from google_webfont_downloader.FindFonts import FindFonts
from google_webfont_downloader.DownloadFont import DownloadFont
from google_webfont_downloader.html_preview import html

# See google_webfont_downloader_lib.Window.py for more details about how this class works
class GoogleWebfontDownloaderWindow(Window):
    __gtype_name__ = "GoogleWebfontDownloaderWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        self.fonts = FindFonts()
        """Set up the main window"""
        super(GoogleWebfontDownloaderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutGoogleWebfontDownloaderDialog
        self.PreferencesDialog = PreferencesGoogleWebfontDownloaderDialog

        # Code for other initialization actions should be added here.
        self.toolbar = builder.get_object("toolbar")
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.view = WebKit.WebView()
        webview = builder.get_object("webview")
        webview.add(self.view)
        webview.show_all()

        # the data in the model (three strings for each row, one for each column)
        listmodel = builder.get_object("liststore")
        # append the values in the model
        for i in range(len(self.fonts)):
            listmodel.append(self.fonts[i])

        # a treeview to see the data stored in the model
        self.listview = builder.get_object("font_list")
        cell = Gtk.CellRendererText()
        col = Gtk.TreeViewColumn(_("Fonts"), cell, text=0)
        self.listview.append_column(col)
        self.listview.columns_autosize()
        # when a row is selected, it emits a signal
        self.listview.get_selection().connect("changed", self.on_changed)

        self.search_field = self.builder.get_object('search_field')
        self.search_field.connect('activate', self.on_search_entered)
        self.search_field.connect("icon-press", self.clear_search)

        completion = self.builder.get_object('entrycompletion')
        completion.set_model(listmodel)
        completion.set_text_column(0)
        self.search_field.set_completion(completion)

        self.mnu_save = self.builder.get_object('mnu_save')
        self.mnu_save.connect("activate", self.on_download_btn_clicked)
        self.mnu_save_as = self.builder.get_object('mnu_save_as')
        self.mnu_save_as.connect("activate", self.on_mnu_save_as_clicked)

    def on_search_entered(self, widget):
        fonts = list(itertools.chain(*self.fonts))
        entered_text = self.search_field.get_text()
        matcher = re.compile(entered_text, re.IGNORECASE)
        if any(itertools.ifilter(matcher.match, fonts)):
            for position, item in enumerate(fonts):
                if item.lower() == entered_text.lower():
                    self.listview.set_cursor(position)
        else:
            pass

    def on_changed(self, selection):
        (model, iter) =  selection.get_selected()
        self.font = model[iter][0]
        self.load_html()

    def clear_search(self, widget, icon_pos, event):
        self.search_field.set_text("")

    def on_download_btn_clicked(self, button):
        try:
            DownloadFont(self.font, uri='None')
            self.load_html()
        except AttributeError:
            pass

    def on_info_btn_clicked(self, button):
        try:
            info_url = "http://www.google.com/webfonts/specimen/" + \
                       self.font.replace(' ', '+', -1)
            Gtk.show_uri(None, info_url, 0)
        except AttributeError:
            pass

    def on_mnu_save_as_clicked(self, button):
        try:
            dialog = Gtk.FileChooserDialog("Please choose a file", self,
                                           Gtk.FileChooserAction.SAVE,
                                          (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                           Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
            filename = self.font + ".ttf"
            dialog.set_current_name(filename)
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                uri = dialog.get_filename()
                DownloadFont(self.font, uri)
            elif response == Gtk.ResponseType.CANCEL:
                pass
            dialog.destroy()
        except AttributeError:
            pass

    def load_html(self):
        htmlfile = html(self.font)
        self.view.load_html_string(htmlfile, "file:///")
