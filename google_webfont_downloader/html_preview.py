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

import glob
from locale import gettext as _
from gi.repository import Gtk
import urllib2
from google_webfont_downloader_lib.xdg import fontDir

def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False

def html(font):
    if internet_on() == True:
        if glob.glob(fontDir + font + '.*'):
            icon_name = "gtk-apply"
            theme = Gtk.IconTheme.get_default()
            info = theme.lookup_icon(icon_name, 64, 0)
            icon_uri = info.get_filename()
            html_icon = """
     <div class="installed"><img src="file://%s" width=64 height=64>
     <p>Installed</p></div>""" % icon_uri
        else:
            html_icon = ""
        html = """
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=%s">
    <style>
      body { font-family: '%s', serif; font-size: 36px; }
      div.installed { float: right; font-size: 12px;}
    </style>
  </head>
  <body>
    %s
    <div><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p></div>
  </body>
</html>
""" % (font, font, html_icon)
    else:
        icon_name = "network-error"
        theme = Gtk.IconTheme.get_default()
        info = theme.lookup_icon(icon_name, 64, 0)
        icon_uri = info.get_filename()
        html = """
<html>
  <head>
    <style>
      body { font-family: Ubuntu, sans-serif; font-size: 36px; }
    </style>
  </head>
  <body>
    <center><div><img src="file://%s" width=64 height=64 > %s</div></center>
  </body>
</html>
""" % (icon_uri, "No network connection.")
    return html
