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

import json
import urllib2
import os
from typecatcher_lib.xdg import cacheDir

# Should the really be publicly viewable?
API_KEY = 'AIzaSyDpvpba_5RvJSvmXEJS7gZDezDaMlVTo4c'

def FindFonts():
        data = get_fonts_json()
        fonts = process_json(data)
        cache_json(data)
        return fonts


def get_fonts_json():
    try:
        req = urllib2.Request(
          "https://www.googleapis.com/webfonts/v1/webfonts?key=%s" % API_KEY)
        opener = urllib2.build_opener()
        data = opener.open(req).read()
    except urllib2.URLError:
        data = open_local_json()
    return data


def open_local_json():
    local_json = os.path.join(cacheDir + "webfonts.json")
    data = open(local_json).read()
    return data


def process_json(data):
    json_data = json.loads(str(data), "utf-8")
    fonts = []
    for n in json_data['items']:
        f = []
        f.append(str(n['family']))
        fonts.append(f)
    return fonts


def cache_json(data):
    local_json = os.path.join(cacheDir + "webfonts.json")
    if os.path.exists(cacheDir):
        with open(local_json, 'wb') as local_json:
            local_json.write(data)
    else:
        os.makedirs(cacheDir)
        with open(local_json, 'wb') as local_json:
            local_json.write(data)


def get_font_variants(family):
    data = open_local_json()
    json_data = json.loads(str(data), "utf-8")
    variants = []
    for n in json_data['items']:
        if n['family'] == family:
            for v in n['variants']:
                variants.append(str(v))
    return variants
