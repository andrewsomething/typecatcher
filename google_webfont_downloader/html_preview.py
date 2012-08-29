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
from random import choice
from google_webfont_downloader_lib.xdg import fontDir

def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False

def html_font_view(font, text=None):
    if internet_on() == True:
        text_preview = select_text_preview(text)
        icon_name = "gtk-apply"
        theme = Gtk.IconTheme.get_default()
        info = theme.lookup_icon(icon_name, 64, 0)
        icon_uri = info.get_filename()
        if glob.glob(fontDir + font + '.*'):
            html_icon = """
     <div id="installed"><img src="file://%s" width=64 height=64>
     <p>%s</p></div>""" % (icon_uri, _("Installed"))
        else:
            html_icon = """
     <div id="installed"> <style display = 'none'><img src="file://%s" width=64 height=64>
     <p>%s</p></style></div>""" % (icon_uri, _("Installed"))
        html = """
<html>
  <head>
    <link id="stylesheet" rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=%s">
    <style>
      body { font-family: '%s', serif; font-size: 36px; }
      #installed { float: right; font-size: 12px; width:50px;}
      textarea { font-family: %s; font-size: 36px; border: None; overflow: hidden; outline: none; width: 90%%; height: 100%%; }
    </style>
  </head>
  <body>
    %s
    <div><p>%s</p></div>
  </body>
</html>
""" % (font, font, font, html_icon, text_preview)
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
""" % (icon_uri, _("No network connection."))
    return html

def start_page():
    icon_name = "font-x-generic"
    theme = Gtk.IconTheme()
    theme.set_custom_theme("gnome")
    info = theme.lookup_icon(icon_name, 256, 0)
    icon_uri = info.get_filename()
    html = """
<html>
  <head>
    <style>
      body { font-family: Ubuntu, sans-serif; font-size: 28px; }
    </style>
  </head>
  <body>
    <center><div><img src="file://%s" ></div></center>
    <center><p>Google Webfont Downloader</p><center>
  </body>
</html>
""" % icon_uri
    return html

def select_text_preview(text):
    ipsum = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
    kafka = _("One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections.")
    hgg = "Far out in the uncharted backwaters of the unfashionable end of the Western Spiral arm of the Galaxy lies a small unregarded yellow sun. Orbiting this at a distance of roughly ninety-eight million miles is an utterly insignificant little blue-green planet..."
    ggm = _("Many years later, as he faced the firing squad, Colonel Aureliano Buendia was to remember that distant afternoon when his father took him to discover ice.")
    ralph = _("I am an invisible man. No, I am not a spook like those who haunted Edgar Allan Poe; nor am I one of your Hollywood-movie ectoplasms. I am a man of substance, of flesh and bone, fiber and liquids — and I might even be said to possess a mind. I am invisible, understand, simply because people refuse to see me.")
    jj = _("Stately, plump Buck Mulligan came from the stairhead, bearing a bowl of lather on which a mirror and a razor lay crossed. A yellow dressinggown, ungirdled, was sustained gently behind him on the mild morning air.")
    custom = "<textarea id='custom'> %s </textarea>" % (_("Enter text..."))
    text_pool = [ipsum, kafka, ggm, hgg, ralph, jj]
    if text == None or text == "random":
        selected_text = choice(text_pool)
        return selected_text
    elif text == "ipsum":
        return ipsum
    elif text == "kafka":
        return kafka
    elif text == "hgg":
        return hgg
    elif text == "ggm":
        return ggm
    elif text == "ralph":
        return ralph
    elif text == "jj":
        return jj
    elif text == "custom":
        return custom
