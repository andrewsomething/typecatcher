#!/usr/bin/python
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

import sys
import os.path
import unittest
sys.path.insert(0, os.path.realpath(os.path.join(os.path.dirname(__file__), "..")))
import tempfile
import json
from google_webfont_downloader import AboutGoogleWebfontDownloaderDialog
from google_webfont_downloader.DownloadFont import extract_url, write_font_file
from google_webfont_downloader.FindFonts import process_json, cache_json, get_fonts_json
from google_webfont_downloader_lib.xdg import cacheDir

class TestCases(unittest.TestCase):
    def setUp(self):
        self.AboutGoogleWebfontDownloaderDialog_members = [
        'AboutDialog', 'AboutGoogleWebfontDownloaderDialog', 'logger', 'logging']
        self.font_url = 'http://themes.googleusercontent.com/static/fonts/alfaslabone/v2/Qx6FPcitRwTC_k88tLPc-Yjjx0o0jr6fNXxPgYh_a8Q.ttf'
        self.font_name = 'Alfa Slab One'
        self.font_list = [["Abel"], ["Abril Fatface"]]


    def test_AboutGoogleWebfontDownloaderDialog_members(self):
        all_members = dir(AboutGoogleWebfontDownloaderDialog)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.AboutGoogleWebfontDownloaderDialog_members, public_members)

    def test_extract_url(self):
        returned_url = extract_url(self.font_name)
        self.assertEqual(self.font_url, returned_url)

    def text_write_font_file(self):
        fake_font_dir = tempfile.mkdtemp() + "-fonts"
        font_url, font_dir, font_name = self.font_url, fake_font_dir, self.font_name
        write_font_file(font_url, font_dir, font_name)
        self.assertTrue(os.path.isfile(os.path.join(fake_font_dir, self.font_name)))

    def test_process_json(self):
        returned_list = process_json(fake_json_data)
        self.assertEqual(self.font_list, returned_list)

    def test_cache_json(self):
        cache_json(fake_json_data)
        with open(os.path.join(cacheDir + "webfonts.json")) as f:
            self.assertEqual(f.read(), fake_json_data)

    def test_get_fonts_json(self):
        returned_data = get_fonts_json()
        self.assertTrue(json.loads(str(returned_data),"utf-8"))

fake_json_data = """{
 "kind": "webfonts#webfontList",
 "items": [
  {
   "kind": "webfonts#webfont",
   "family": "Abel",
   "variants": [
    "regular"
   ],
   "subsets": [
    "latin"
   ]
  },
  {
   "kind": "webfonts#webfont",
   "family": "Abril Fatface",
   "variants": [
    "regular"
   ],
   "subsets": [
    "latin-ext",
    "latin"
   ]
  }
 ]
}"""

if __name__ == '__main__':
    unittest.main()
