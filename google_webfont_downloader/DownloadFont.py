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

import urllib2, re

WEBFONTS_API_URL="http://fonts.googleapis.com/css?family="

def DownloadFont(font_name):
    font_url = extract_url(font_name)
    print font_url

def extract_url(font_name):
    css_url =  WEBFONTS_API_URL + font_name.replace(' ', '%20', -1)
    req = urllib2.Request(css_url)
    opener = urllib2.build_opener()
    css = str(opener.open(req).read())
    font_url = re.compile(r'url\((.*?)\)').search(css).group(1)
    return font_url
