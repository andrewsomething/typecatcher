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

import os
import urllib2
import re
import glob

from google_webfont_downloader_lib.xdg import fontDir, cacheDir

WEBFONTS_API_URL = "http://fonts.googleapis.com/css?family="


def DownloadFont(font_name, uri):
    font_url = extract_url(font_name)
    if font_url is not None:
        if uri is None:
            font_dir = fontDir
            write_font_file(font_url, font_dir, font_name)
        else:
            font_dir = os.path.dirname(uri)
            write_font_file(font_url, font_dir, font_name)
    else:
        pass


def write_font_file(font_url, font_dir, font_name):
    req = urllib2.Request(font_url)
    r = urllib2.urlopen(req)
    ext = os.path.splitext(font_url)[1]
    f = os.path.join(font_dir, font_name + ext)
    with open(f, 'wb') as f:
        f.write(r.read())


def extract_url(font_name):
    css_url = WEBFONTS_API_URL + font_name.replace(' ',
                                                   '%20',
                                                   -1) + "&subset=all"
    req = urllib2.Request(css_url)
    opener = urllib2.build_opener()
    try:
        css = str(opener.open(req).read())
        font_url = re.compile(r'url\((.*?)\)').search(css).group(1)
    except urllib2.URLError:
        font_url = None
    return font_url


def UninstallFont(font_name):
    font_file = glob.glob(fontDir + font_name + ".*")
    for f in font_file:
        os.remove(f)
