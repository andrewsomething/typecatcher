# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

from locale import gettext as _

import logging
logger = logging.getLogger('google_webfont_downloader')

from google_webfont_downloader_lib.AboutDialog import AboutDialog

# See google_webfont_downloader_lib.AboutDialog.py for more details about how this class works.
class AboutGoogleWebfontDownloaderDialog(AboutDialog):
    __gtype_name__ = "AboutGoogleWebfontDownloaderDialog"
    
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the about dialog"""
        super(AboutGoogleWebfontDownloaderDialog, self).finish_initializing(builder)

        # Code for other initialization actions should be added here.

