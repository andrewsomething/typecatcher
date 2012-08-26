# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

from gi.repository import Gtk # pylint: disable=E0611
from gi.repository import WebKit
import logging
logger = logging.getLogger('google_webfont_downloader')

from google_webfont_downloader_lib import Window
from google_webfont_downloader.AboutGoogleWebfontDownloaderDialog import AboutGoogleWebfontDownloaderDialog
from google_webfont_downloader.PreferencesGoogleWebfontDownloaderDialog import PreferencesGoogleWebfontDownloaderDialog

# See google_webfont_downloader_lib.Window.py for more details about how this class works
class GoogleWebfontDownloaderWindow(Window):
    __gtype_name__ = "GoogleWebfontDownloaderWindow"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(GoogleWebfontDownloaderWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutGoogleWebfontDownloaderDialog
        self.PreferencesDialog = PreferencesGoogleWebfontDownloaderDialog

        # Code for other initialization actions should be added here.
        self.toolbar = builder.get_object("toolbar1")
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        self.view = WebKit.WebView()
        webview = builder.get_object("viewport1")
        webview.add(self.view)


