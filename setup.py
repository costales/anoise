#!/usr/bin/env python3

# ANoise 0.0.30 - http://launchpad.net/anoise
# Copyright (C) 2015-2019 Marcos Alvarez Costales https://launchpad.net/~costales
#
# ANoise is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
# 
# ANoise is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with ANoise; if not, see http://www.gnu.org/licenses 
# for more information.


import os, sys, glob, DistUtilsExtra.auto

# Create data files
data = [ ('/usr/share/anoise',                      glob.glob('anoise/*')),
         ('/usr/share/icons/hicolor/scalable/apps', glob.glob('icons/hicolor/scalable/apps/*.svg')),
         ('/usr/share/icons/hicolor/48x48/apps',    glob.glob('icons/hicolor/48x48/apps/*.png')),
         ('/usr/share/icons/hicolor/16x16/apps',    glob.glob('icons/hicolor/16x16/apps/*.png'))]

# Setup stage
DistUtilsExtra.auto.setup(
    name         = "anoise",
    version      = "0.0.30",
    description  = "Ambient Noise",
    author       = "Marcos Alvarez Costales https://launchpad.net/~costales",
    author_email = "https://launchpad.net/~costales",
    url          = "https://launchpad.net/anoise",
    license      = "GPL3",
    data_files   = data
    )

