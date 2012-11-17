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

from typecatcher_lib.xdg import fontDir, cacheDir
from typecatcher.FindFonts import get_font_variants

WEBFONTS_API_URL = "http://fonts.googleapis.com/css?family="


def DownloadFont(font_name, uri):
    font_dict = extract_url(font_name)
    if font_dict is not None:
        for n in font_dict.items():
            font_url = n[-1]
            variant = n[0]
            if font_url is not None:
                if uri is None:
                    font_dir = fontDir
                    write_font_file(font_url, font_dir, font_name, variant)
                else:
                    font_dir = os.path.dirname(uri)
                    write_font_file(font_url, font_dir, font_name, variant)
    else:
        pass


def write_font_file(font_url, font_dir, font_name, variant):
    req = urllib2.Request(font_url)
    r = urllib2.urlopen(req)
    full_name = font_name + "_" + variant
    ext = os.path.splitext(font_url)[1]
    f = os.path.join(font_dir, full_name + ext)
    if not os.path.exists(font_dir):
        os.makedirs(font_dir)
    with open(f, 'wb') as f:
        f.write(r.read())


def extract_url(font_name):
    variants = get_font_variants(font_name)
    css_url = WEBFONTS_API_URL + font_name.replace(' ',
                                                   '%20',
                                                   -1) + ":" + \
                                                   ','.join(variants) + \
                                                   "&subset=all"

    font_urls = []
    styles = []
    weights = []
    desc = []

    req = urllib2.Request(css_url)
    opener = urllib2.build_opener()
    try:
        css = opener.open(req).readlines()
        for line in css:
            style = re.search(r'font-style\:\ (.*?)\;', line)
            if style:
                styles.append(style.group(1))
            weight = re.search(r'font-weight\:\ (.*?)\;', line)
            if weight:
                weights.append(weight.group(1))
            font_url = re.search(r'url\((.*?)\)', line)
            if font_url:
                font_urls.append(font_url.group(1))

        for n in range(len(styles)):
            desc.append(str(styles[n] + "-" + weights[n]))
        font_dict = dict(zip(desc, font_urls))

        return font_dict

    except urllib2.URLError:
        return None


def UninstallFont(font_name):
    font_file = glob.glob(fontDir + font_name + "_*.*")
    for f in font_file:
        os.remove(f)
