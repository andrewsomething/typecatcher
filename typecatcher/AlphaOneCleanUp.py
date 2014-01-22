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
from typecatcher_lib.xdg import fontDir, cacheDir, confDir


def fix_file_names():
    """
    We changed the naming of the font files now that we fetch all the weights.
    So now we need to clean up the file names on old installs of Alpha 1.
    This can be removed after awhile.
    """

    alpha_clean_up_check = os.path.join(confDir + "alpha_clean_up_check")
    if not os.path.isfile(alpha_clean_up_check):
        rename_font_files()
        write_alpha_clean_up_file()
    else:
        pass

def write_alpha_clean_up_file():
    f = os.path.join(confDir + "alpha_clean_up_check")
    if not os.path.exists(confDir):
        os.makedirs(confDir)
    with open(f, 'a'):
        os.utime(f, None)

def rename_font_files():
    if os.path.isdir(fontDir):
        for f in os.listdir(fontDir):
            font_fam = os.path.splitext(f)[0]
            ext = os.path.splitext(f)[1]
            old = os.path.join(fontDir, f)
            new = os.path.join(fontDir, font_fam + "_normal" + ext)
            os.rename(old, new)
    else:
        pass
