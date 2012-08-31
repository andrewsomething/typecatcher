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
from google_webfont_downloader_lib.helpers import get_media_file
import urllib2
from random import choice

def internet_on():
    try:
        response = urllib2.urlopen('http://74.125.113.99',timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False

def html_font_view(font=None, text=None):

    start_page_icon_name = "font-x-generic"
    start_page_theme = Gtk.IconTheme()
    start_page_theme.set_custom_theme("gnome")
    start_page_info = start_page_theme.lookup_icon(start_page_icon_name, 256, 0)
    start_page_icon_uri = start_page_info.get_filename()

    con_icon_name = "network-error"
    con_theme = Gtk.IconTheme.get_default()
    con_info = con_theme.lookup_icon(con_icon_name, 64, 0)
    con_icon_uri = con_info.get_filename()

    installed_icon_name = "gtk-apply"
    installed_theme = Gtk.IconTheme.get_default()
    installed_info = installed_theme.lookup_icon(installed_icon_name, 64, 0)
    installed_icon_uri = installed_info.get_filename()

    loader = get_media_file("ajax-loader.gif")

    text_preview = select_text_preview(text)

#     .wf-loading #text_preview { visibility: hidden; }
#     .wf-active #text_preview .wf-#text_preview body { visibility: visible; }

    html = """
<html>
  <head>

    <script src="//ajax.googleapis.com/ajax/libs/webfont/1/webfont.js"></script>

    <style>
      body { font-size: 36px; }
      #installed { float: right; font-size: 12px; width:50px; text-align:center; display: None; }
      textarea { font: inherit; font-size: 36px; border: None; overflow: hidden; outline: none; width: 90%%; height: 100%%; }
      #text_preview { display: None; }
      #no_connect { text-align: center; display: None; }
     .wf-loading { height: 100%%; overflow: hidden; background: url(%s) center center no-repeat fixed;}
     .wf-loading * { opacity: 0; }
    </style>

  </head>

  <body>

     <div id="installed">
       <img src="file://%s" width=64 height=64>
       <p>%s</p>
     </div>

     <div id='no_connect'>
       <img src="file://%s" width=64 height=64 > %s
     </div>

    <div id='text_preview'>
      %s
    </div>

    <div id='start_page'>
      <center><div><img src="file://%s" ></div></center>
      <center><p>Google Webfont Downloader</p><center>
    </div>

  </body>

</html>
""" % (loader, installed_icon_uri, _("Installed"),
       con_icon_uri, _("No network connection."),
       text_preview, start_page_icon_uri)

    return html

def select_text_preview(text):
    ipsum = """Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."""
    kafka = _("One morning, when Gregor Samsa woke from troubled dreams, he found himself transformed in his bed into a horrible vermin. He lay on his armour-like back, and if he lifted his head a little he could see his brown belly, slightly domed and divided by arches into stiff sections.")
    hgg = "Far out in the uncharted backwaters of the unfashionable end of the Western Spiral arm of the Galaxy lies a small unregarded yellow sun. Orbiting this at a distance of roughly ninety-eight million miles is an utterly insignificant little blue-green planet..."
    ggm = _("Many years later, as he faced the firing squad, Colonel Aureliano Buendia was to remember that distant afternoon when his father took him to discover ice.")
    ralph = _("I am an invisible man. No, I am not a spook like those who haunted Edgar Allan Poe; nor am I one of your Hollywood-movie ectoplasms. I am a man of substance, of flesh and bone, fiber and liquids — and I might even be said to possess a mind. I am invisible, understand, simply because people refuse to see me.")
    jj = _("Stately, plump Buck Mulligan came from the stairhead, bearing a bowl of lather on which a mirror and a razor lay crossed. A yellow dressinggown, ungirdled, was sustained gently behind him on the mild morning air.")

    text_pool = [ipsum, kafka, ggm, hgg, ralph, jj]

    if text == None or text == "random":
        selected_text = choice(text_pool)
        return "<p> %s </p>" % selected_text
    elif text == "ipsum":
        return "<p> %s </p>" % ipsum
    elif text == "kafka":
        return "<p> %s </p>" % kafka
    elif text == "hgg":
        return "<p> %s </p>" % hgg
    elif text == "ggm":
        return "<p> %s </p>" % ggm
    elif text == "ralph":
        return "<p> %s </p>" % ralph
    elif text == "jj":
        return "<p> %s </p>" % jj
    elif text == "custom":
        return "<textarea> %s </textarea>" % (_('Enter text...'))
