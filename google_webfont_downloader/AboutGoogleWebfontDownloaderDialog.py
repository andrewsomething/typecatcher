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

