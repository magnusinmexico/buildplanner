# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: load_icons.py
# Author: Magnus Pettersson
#
# This script manages the registration and unregistration of custom icons
# for the Build Planner add-on. Upon registration, it loads custom icons
# from the specified directory and assigns them unique identifiers for
# use within Blender. These icons represent various states and tools
# within the add-on, enhancing the user interface and visual feedback.
# The script also provides functionality to unregister the icons when
# they are no longer needed, ensuring proper resource management.
#
#------------------------------------------------------------------------------

import os

import bpy
import bpy.utils.previews

from . import BPBlender

def register():
    
    BPBlender.icons = bpy.utils.previews.new()
    bp_custom_icons = BPBlender.icons
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    bp_custom_icons.load("bp_icon_status_none", os.path.join(icons_dir, "bp_icon_status_none.png"), 'IMAGE')
    bp_custom_icons.load("bp_icon_status_red", os.path.join(icons_dir, "bp_icon_status_red.png"), 'IMAGE')
    bp_custom_icons.load("bp_icon_status_yellow", os.path.join(icons_dir, "bp_icon_status_yellow.png"), 'IMAGE')
    bp_custom_icons.load("bp_icon_status_green", os.path.join(icons_dir, "bp_icon_status_green.png"), 'IMAGE')
    bp_custom_icons.load("bp_icon_saw", os.path.join(icons_dir, "bp_icon_saw.png"), 'IMAGE')

    print("ICONS DIRECTORY: ",icons_dir)

def unregister():
    if BPBlender.icons:
        bpy.utils.previews.remove(BPBlender.icons)
        BPBlender.icons = None