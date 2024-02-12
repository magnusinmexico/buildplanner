# ##### BEGIN GNU LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software 
# Foundation; either version 3 of the License, or (at your option) any later 
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT 
# ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more 
# details.
#
# You should have received a copy of the GNU General Public License along with 
# this program. If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

#------------------------------------------------------------------------------
#
# File: __init__.py
# Author: Magnus Pettersson
#
#------------------------------------------------------------------------------

bl_info = {
    "name" : "Build Planner",
    "author" : "Magnus Pettersson",
    "description" : "",
    "blender" : (4, 0, 0),
    "version" : (0, 1, 0),
    "location" : "3D View > Sidebar",
    "warning" : "",
    "category" : "Construction",
    "documentation:url" : "https://github.com/magnusinmexico/buildplanner/blob/v0.1.0/README.md"
}

import bpy
import sys
from pathlib import Path

PROJECT_DIR = Path(str(Path(__file__).parents[1])+"/buildplanner")
sys.path.append(str(PROJECT_DIR))

import bp

class BPBlender:

    bl_idname = 'bp.bp_blender'

    icons = None
    cutter_data = {}

from . import auto_load

bp = BPBlender.cutter_data

bp["bp_cutter_state"] = {"CLOSED":True,"RUNNING":False,"HAS_DATA":False}
bp["progress_step"] = [0,0,0,0,0]
bp["progress"] = ["","","","",""]
bp["bp_status_icon"] = ["bp_icon_status_none","bp_icon_status_yellow","bp_icon_status_green","bp_icon_status_red"]

auto_load.init()

def register():
    auto_load.register()

def unregister():
    bpy.types.Object.bp_data = None
    auto_load.unregister()
