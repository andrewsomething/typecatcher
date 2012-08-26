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

try:
    import xdg.BaseDirectory
except ImportError:
    home = os.environ.get('HOME')
    xdg_config_home = os.path.join(home, '.config/')
    xdg_cache_home = os.path.join(home, '.cache/')
else:
    xdg_config_home = xdg.BaseDirectory.xdg_config_home
    xdg_cache_home = xdg.BaseDirectory.xdg_cache_home
    
confDir =  os.path.join(xdg_config_home, 'google-webfont-downloader')
cacheDir =  os.path.join(xdg_cache_home, 'google-webfont-downloader')
