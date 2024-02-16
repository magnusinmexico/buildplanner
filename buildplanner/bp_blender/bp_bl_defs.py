# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: build_planner_preferences.py
# Author: Magnus Pettersson
#
# This module defines preferences for the Build Planner add-on. Users can
# adjust settings such as decimal precision, cutting method, and maximum
# complexity of objects. These preferences ensure efficient and customizable
# operation of the Build Planner add-on within Blender.
#
#------------------------------------------------------------------------------

import bpy

from bpy.props import( 
    StringProperty, 
    FloatProperty,
    IntProperty,
    BoolProperty,
    IntVectorProperty,
    FloatVectorProperty
)

from bpy.types import PropertyGroup

class StringArrayItem(bpy.types.PropertyGroup):
    value: bpy.props.StringProperty(name="String Value") # type: ignore

# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class BuildPlannerProperties(PropertyGroup):

    bp_name: StringProperty( # type: ignore
        name="Starting with",
        description=":",
        default="",
        maxlen=64
        )
    
    bp_stock_0: FloatProperty(name="",default=4.2,precision=5,unit="LENGTH") # type: ignore
    bp_stock_1: FloatProperty(name="",default=3.6,precision=1,unit="LENGTH") # type: ignore
    bp_stock_2: FloatProperty(name="",default=4.8,precision=1,unit="LENGTH") # type: ignore
    bp_stock_3: FloatProperty(name="",default=3.0,precision=1,unit="LENGTH") # type: ignore
    bp_stock_4: FloatProperty(name="",default=5.4,precision=1,unit="LENGTH") # type: ignore

    bp_stock_avail_0: IntProperty(name="",default=100) # type: ignore
    bp_stock_avail_1: IntProperty(name="",default=100) # type: ignore
    bp_stock_avail_2: IntProperty(name="",default=100) # type: ignore
    bp_stock_avail_3: IntProperty(name="",default=100) # type: ignore
    bp_stock_avail_4: IntProperty(name="",default=100) # type: ignore

    bp_stock_variations: IntProperty( # type: ignore
        name="Stock Varations",
        description=":",
        default=2,
        min = 1,
        max = 5
        )
    
    bp_cut_width : FloatProperty( # type: ignore
        name="Cut width",
        default = 0.005,
        soft_min = 0.0,
        soft_max = 100.0,
        precision = 1,
        unit="LENGTH"
    )
    
    bp_cutter_file_path: StringProperty( # type: ignore
        name="Output folder",
        description="bp Cutter Output Folder",
        default="",
        maxlen= 1024,
        subtype='DIR_PATH')
    