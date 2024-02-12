# SPDX-License-Identifier: GPL-3.0-or-later
#------------------------------------------------------------------------------
#
# File: build_planner_preferences.py
# Author: [Author Name]
#
# This module defines preferences for the Build Planner add-on. Users can adjust
# settings such as decimal precision, cutting method, and maximum complexity of
# objects. These preferences ensure efficient and customizable operation of the
# Build Planner add-on within Blender.
#
#------------------------------------------------------------------------------


import bpy
from bpy.types import Operator, AddonPreferences
from bpy.props import StringProperty, IntProperty, BoolProperty, EnumProperty

class BuildPlannerPreferences(AddonPreferences):
    # this must match the add-on name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = "buildplanner"

    #context.preferences.addons["buildplanner"].preferences.precision
    precision: IntProperty(
        name="Decimal precision",
        description="Decimal precision in relation to Blender units",
        default=1,
        soft_min=-2,
        soft_max=6
    )

    #context.preferences.addons["buildplanner"].preferences.method
    method: bpy.props.EnumProperty(
        name="Cutting Method",
        description="Select an option from the dropdown list",
        items=[
            ("GREEDY", "Greedy Cut", "Use the Greedy Cut only"),
            ("EXPERIMENTAL", "Experimental Cut", "Use the Experimental Cut only"),
            ("BOTH", "Both", "Use both Greedy and Experimental Cut and select the best result"),
        ],
        default="BOTH"  
    )

    #context.preferences.addons["buildplanner"].preferences.complexity
    complexity: IntProperty(
        name="Max Complexity (vertices)",
        description="Maximum complexity of objects. Increse with caution as the operations might hang if too complex objects.",
        default=128,
        soft_min=8,
        soft_max=1024
    )

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.prop(self, "method")
        row = layout.row()
        row.prop(self, "precision")
        row.prop(self, "complexity")

