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
from google_webfont_downloader_lib.xdg import cacheDir

def FindFonts():
    try:
        req = urllib2.Request("https://www.googleapis.com/webfonts/v1/webfonts")
        opener = urllib2.build_opener()
        data = opener.open(req).read()
        fonts = process_json(data)
        cache_json(data)
        return fonts
    except urllib2.URLError:
        local_json = os.path.join(cacheDir + "webfonts.json")
        data = open(local_json).read()
        fonts = process_json(data)
        return fonts

def process_json(data):
    json_data = json.loads(str(data),"utf-8")
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
