# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_bl_menu.py
# Author: Magnus Pettersson
#
# This module defines a Blender panel for the Build Planner add-on. The panel,
# named "Cutter," is located in the "Build Planner" category within the sidebar
# of the 3D Viewport. It provides options for cutting wood and displaying HTML
# results. Users can adjust settings such as wood cutting width, stock
# variations, and file paths. The panel's layout is designed to facilitate
# efficient interaction with the Build Planner functionalities.
#
#------------------------------------------------------------------------------

import bpy

from bp import bp_defs

from buildplanner import BPBlender

class VIEW3D_PT_bp_cutter(bpy.types.Panel):  # class naming convention ‘CATEGORY_PT_name’

    bl_space_type = "VIEW_3D"  # 3D Viewport area (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/space_type_items.html#rna-enum-space-type-items)
    bl_region_type = "UI"  # Sidebar region (find list of values here https://docs.blender.org/api/current/bpy_types_enum_items/region_type_items.html#rna-enum-region-type-items)

    bl_category = "Build Planner"  # found in the Sidebar
    bl_label = "Cutter"  # found at the top of the Panel
    #bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        icons = BPBlender.icons
        bp = BPBlender.cutter_data

        """define the layout of the panel"""
        unit = bp_defs.length_unit_suffix[bpy.context.scene.unit_settings.length_unit]
        box = self.layout.box()
        row = box.row()
        row.enabled = not bp["bp_cutter_state"]["RUNNING"]
        row.operator("wm.bp_cutwood", text="Cut Wood", icon_value=icons["bp_icon_saw"].icon_id)

        #print(bp["bp_cutter_state"])

        if bp["bp_cutter_state"]["RUNNING"] or bp["bp_cutter_state"]["HAS_DATA"]:
            for i in range(5):
                row = box.row()
                row.label(text=bp["progress"][i],icon_value=icons[bp["bp_status_icon"][bp["progress_step"][i]]].icon_id)
            row = box.row()
            show_html = row.column()
            show_html.enabled = bp["bp_cutter_state"]["HAS_DATA"] and context.scene.build_planner.bp_cutter_file_path != ""
            show_html.operator("bp.bp_show_html")
            row.operator("bp.bp_reset_cutwood")

        column = self.layout.column()
        column.prop(context.scene.build_planner, "bp_name")
        column.prop(context.scene.build_planner, "bp_cut_width")
        column.prop(context.scene.build_planner, "bp_stock_variations")
        row = self.layout.row()
        col1 = row.column()
        col2 = row.column()
        col3 = row.column()
        col1.label(text="Stock #")
        col2.label(text = f"Length in {unit}")
        col3.label(text = "Available amount")
        for i in range(context.scene.build_planner.bp_stock_variations):
            col1.label(text=f"{i+1}")
            col2.prop(context.scene.build_planner, "bp_stock_"+str(i))
            col3.prop(context.scene.build_planner, "bp_stock_avail_"+str(i))

        row = self.layout.row()
        row.prop(context.scene.build_planner, "bp_cutter_file_path")
            