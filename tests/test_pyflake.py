#!/usr/bin/python3
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

import unittest
import subprocess

class TestPylint(unittest.TestCase):
    def test_project_errors_only(self):
        '''run pyflake'''
        return_code = subprocess.call(["pyflakes3", 'typecatcher'])
        return_code = subprocess.call(["pyflakes3", 'typecatcher_lib'])

if __name__ == '__main__':
    'you will get better results with nosetests'
    unittest.main()
