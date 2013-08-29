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
import glob
from typecatcher import AboutTypeCatcherDialog
from typecatcher.DownloadFont import extract_url, write_font_file, UninstallFont
from typecatcher.FindFonts import process_json, cache_json, get_fonts_json, get_font_variants
from typecatcher_lib.xdg import cacheDir

class TestCases(unittest.TestCase):
    def setUp(self):
        self.AboutTypeCatcherDialog_members = [
        'AboutDialog', 'AboutTypeCatcherDialog', 'logger', 'logging']

        self.font_name = 'Abril Fatface'
        self.font_dict = {"regular": "http://themes.googleusercontent.com/static/fonts/abrilfatface/v5/X1g_KwGeBV3ajZIXQ9VnDojjx0o0jr6fNXxPgYh_a8Q.ttf"}
        self.font_list = [["Abel"], ["Abril Fatface"]]
        self.fake_font_dir = tempfile.mkdtemp() + "-fonts"

    def test_AboutTypeCatcherDialog_members(self):
        all_members = dir(AboutTypeCatcherDialog)
        public_members = [x for x in all_members if not x.startswith('_')]
        public_members.sort()
        self.assertEqual(self.AboutTypeCatcherDialog_members, public_members)

    def test_extract_url(self):
        returned_dict = extract_url(self.font_name)
        self.assertEqual(self.font_dict, returned_dict)

    def test_write_font_file(self):
        for n in self.font_dict.items():
            font_url = n[-1]
            variant = n[0]
        write_font_file(font_url,  self.fake_font_dir,
                        self.font_name, variant)
        ext = os.path.splitext(font_url)[1]
        full_name = self.font_name + "_" + variant + ext
        downloaded_font = os.path.join( self.fake_font_dir, full_name)
        self.assertTrue(os.path.isfile(downloaded_font))

    def test_UninstallFont(self):
        font_file = self.fake_font_dir + self.font_name + "_normal-400.ttf"
        with open(font_file, 'wb') as f:
            f.write('Test')
        UninstallFont(self.font_name, self.fake_font_dir)
        self.assertFalse(os.path.isfile(font_file))

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

    def test_get_font_variants(self):
        variants= get_font_variants(self.font_name)
        self.assertTrue(variants, ['regular'])

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
   ],
   "version": "v3",
   "lastModified": "2012-07-25",
   "files": {
    "regular": "http://themes.googleusercontent.com/static/fonts/abel/v3/RpUKfqNxoyNe_ka23bzQ2A.ttf"
   }
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
   ],
   "version": "v5",
   "lastModified": "2012-07-25",
   "files": {
    "regular": "http://themes.googleusercontent.com/static/fonts/abrilfatface/v5/X1g_KwGeBV3ajZIXQ9VnDojjx0o0jr6fNXxPgYh_a8Q.ttf"
   }
  }
 ]
}"""

if __name__ == '__main__':
    unittest.main()
