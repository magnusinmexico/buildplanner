# SPDX-FileCopyrightText: 2023-2024 Magnus Pettersson
#
# SPDX-License-Identifier: GPL-3.0-or-later

#------------------------------------------------------------------------------
#
# File: bp_bl_cutter.py
# Author: Magnus Pettersson
#
# This module defines Blender operators for the Build Planner add-on. These
# operators facilitate actions such as opening a result HTML file, resetting
# wood cutting data, and cutting wood using Blender's tools. The cutting
# process involves several steps including refining dimensions, calculating
# demand, aligning wood pieces, and orchestrating the cutting operation. Each
# step is carefully executed to ensure efficient wood cutting based on the
# specified parameters and preferences.
#
#------------------------------------------------------------------------------

import math
import webbrowser

import bpy
import bmesh
import mathutils

from bp import BPCutter, BPDataStockPieces
from bp import bp_defs
from bp.bp_utils import sround, vround

from buildplanner import BPBlender

class BuildPlanner_OT_bp_ShowHTML(bpy.types.Operator):
    bl_idname = "bp.bp_show_html"
    bl_label = "Open as HTML"

    def execute(self, context):
        bp = BPBlender.cutter_data
        html = bp["html"]

        html_file_path = context.scene.build_planner.bp_cutter_file_path
        html_file_name = html_file_path +"\\cutter.html"
        with open(html_file_name, 'w') as html_file:
            html_file.write(html)
        webbrowser.open(html_file_name)
        return {'FINISHED'}


class BuildPlanner_OT_bp_ResetCutWood(bpy.types.Operator):
    bl_idname = "bp.bp_reset_cutwood"
    bl_label = "Reset"

    def execute(self, context):
        bp = BPBlender.cutter_data
        bp["html"] = None
        bp["bp_cutter_state"]["HAS_DATA"] = False
        return {'FINISHED'}

class BuildPlanner_OT_bp_CutWood(bpy.types.Operator):
    bl_idname = "wm.bp_cutwood"
    bl_label = "Cut Wood Modal"
    _willcont = None

    def refine_dimensions(self, dimensions):
        result = []  # List to store the refined dimensions
        xyz = {}  # Dictionary to count occurrences of each dimension
        number_of_wood = len(dimensions)  # Total number of wood pieces
        count_1 = 0  # Counter for the first loop
        count_2 = 0  # Counter for the second loop

        # First loop: Count occurrences of each dimension
        for wood in dimensions:
            count_1 += 1
            key_mem = []  # List to remember keys for each dimension
            for i in range(3):
                # Calculate occurrences of each dimension and create a unique key
                occurrences_of_dimension = sum(1 for dimension in key_mem if dimension == wood[i])
                key = f"{wood[i]}:{occurrences_of_dimension}"
                if key in xyz:
                    xyz[key] += 1
                else:
                    xyz[key] = 1
                key_mem.append(wood[i])
            yield (False, f"{count_1}/{number_of_wood} - {count_2}/{number_of_wood}", None)

        # Find the two most common dimensions
        value_max_1 = 0
        value_max_2 = 0
        key_max_1 = 0
        key_max_2 = 0
        for key in xyz:
            if xyz[key] > value_max_1:
                key_max_1 = key
                value_max_1 = xyz[key]
        for key in xyz:
            if key != key_max_1 and xyz[key] > value_max_2:
                key_max_2 = key
                value_max_2 = xyz[key]

        w = max(float(key_max_1.split(':')[0]), float(key_max_2.split(':')[0]))
        h = min(float(key_max_1.split(':')[0]), float(key_max_2.split(':')[0]))

        # Second loop: Refine dimensions based on most common dimensions
        for wood in dimensions:
            count_2 += 1
            indexes = []

            # Calculate differences between wood dimensions and the two most common dimensions (w and h)
            dx = abs(wood[0] - w)
            dy = abs(wood[1] - w)
            dz = abs(wood[2] - w)

            # Find the index of the minimum difference (w_index)
            w_index = [dx, dy, dz].index(min(dx, dy, dz))

            # Set the dimension not relevant for calculating h to positive infinity
            dx = abs(wood[0] - h) if w_index != 0 else float('inf')
            dy = abs(wood[1] - h) if w_index != 1 else float('inf')
            dz = abs(wood[2] - h) if w_index != 2 else float('inf')

            # Find the index of the minimum difference for the remaining dimension (h_index)
            h_index = [dx, dy, dz].index(min(dx, dy, dz))

            # Determine the index for the longest dimension (l_index)
            l_index = 2 if w_index + h_index == 1 else 1 if w_index + h_index == 2 else 0

            # Append the refined wood dimensions to the result list
            result.append((wood[l_index], wood[w_index], wood[h_index]))

            # Yield a progress update
            yield (False, f"{count_1}/{number_of_wood} - {count_2}/{number_of_wood}", None)

        # Yield the final result
        yield (True, f"{count_1}/{number_of_wood} - {count_2}/{number_of_wood}", result)
    
    def get_demand(self, dimensions, precision):
        raw_demand = {}
        demand = {}
        for wood in dimensions:
            key = wood[0]
            if key in raw_demand: 
                raw_demand[key] += 1
            else:
                raw_demand[key] = 1
        #print(raw_demand)
        sorted_keys = sorted(raw_demand.keys(), reverse=True)
        for key in sorted_keys:
            demand[key] = raw_demand[key]
        
        # Round the demand based on blender units and the precision set in addon preferences
        rounded_demand = {}
        for key,value in demand.items():
            rounded_demand[round(key,precision)]=value

        return BPDataStockPieces(rounded_demand)

    def calculate_max_distance(self,vertices):
        # Calculate the maximum distance between the aligned vertices
        max_distance = 0.0
        farthest_vertices = (mathutils.Vector(), mathutils.Vector())

        for i, vert1 in enumerate(vertices):
            for vert2 in vertices[i+1:]:
                distance = (vert2 - vert1).length
                if distance > max_distance:
                    max_distance = distance
                    farthest_vertices = (vert1, vert2)

        vector_between = (farthest_vertices[1] - farthest_vertices[0]).normalized()

        return max_distance, vector_between

    def rotate_vector_around_axis(self, vector, axis, angle):
        # Rotate the vector around the axis by the specified angle
        rotation_matrix = mathutils.Matrix.Rotation(angle, 4, axis)
        rotated_vector = rotation_matrix @ vector
        return rotated_vector

    def iter_angle(self, angle,steps):
        yield angle
        for i in range(steps):
            angle = angle / 2
            yield angle

    def align_and_calculate_max_distance(self, wood, precision):
        
        if bpy.context.active_object: bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        wood.select_set(True)
        bpy.context.view_layer.objects.active = wood
        bpy.ops.object.mode_set(mode='EDIT')

        obj = bpy.context.edit_object
        mesh = bmesh.from_edit_mesh(obj.data)


        #
        # Calculate Length and vector for first axis
        #

        # Find the longest edge
        longest_edge = max(mesh.edges, key=lambda edge: edge.calc_length())

        # Calculate the alignment vector
        first_axis_vector = (longest_edge.verts[1].co - longest_edge.verts[0].co).normalized()

        # Align all vertices along the longest edge and store their representations
        aligned_vertices = [vert.co.dot(first_axis_vector) * first_axis_vector for vert in mesh.verts]

        # Calculate the maximum distance between the aligned vertices
        max_distance, vec = self.calculate_max_distance(aligned_vertices)

        # Set the result for the first axis
        res_x = (round(max_distance,precision),vround(first_axis_vector,precision))

        #
        # Calculate Length and vector for second axis
        #
          
        projected_vertices = []
        # Project all vertices onto the plane defined by the normal align_vector
        for vert in mesh.verts:
            # Project onto the plane: v' = v - (v dot n) * n
            projected_vert = vert.co - vert.co.dot(first_axis_vector) * first_axis_vector
            projected_vertices.append(projected_vert)

        # Get the max distance and vector for the vertices projected on the plane, to get an orthogonal vector to start with
        max_distance, start_vector = self.calculate_max_distance(projected_vertices)

        next_center_angle = 0.0
        min_distance = max_distance
        second_axis_vector = start_vector

        #Start with +/0/- 90, then go from the most succesful angle +/v/- 45... 
        for angle in self.iter_angle(90,15):
            center_angle = next_center_angle
            #for rot_angle in [center_angle-angle,center_angle,center_angle+angle]:
            for rot_angle in [center_angle-angle,center_angle+angle]:
                rotated_vec = self.rotate_vector_around_axis(start_vector, first_axis_vector, math.radians(rot_angle))  
                # Align all vertices along the rotated vector
                aligned_vertices = [vert.dot(rotated_vec) * rotated_vec for vert in projected_vertices]
                # Get the maximum length between vecrtices with the new rotation
                distance, vec = self.calculate_max_distance(aligned_vertices)
                if distance<min_distance:
                    next_center_angle = rot_angle
                    min_distance = distance
                    second_axis_vector = vec
        
        res_y = (round(min_distance,precision),vround(second_axis_vector,precision))
        
        #
        # Calculate Length and vector for third axis
        #

        third_axis_vector = first_axis_vector.cross(second_axis_vector)

        # Align all vertices along the longest edge and store their representations
        aligned_vertices = [vert.co.dot(third_axis_vector) * third_axis_vector for vert in mesh.verts]

        # Calculate the maximum distance between the aligned vertices
        max_distance, vec = self.calculate_max_distance(aligned_vertices)

        # Set the result for the first axis
        res_z = (round(max_distance,precision),vround(third_axis_vector,precision))

        bpy.ops.object.mode_set(mode='OBJECT')

        return (res_x,res_y,res_z)

    def orchestrator(self, context):

        bp = BPBlender.cutter_data

        # Define the scale, and suffix (unit) used for output result of cutter
        length_unit = bpy.context.scene.unit_settings.length_unit

        # Read the unit scale to modify values
        unit_scale = bpy.context.scene.unit_settings.scale_length

        # Read decimal precision value from addon preferences and correct with regards to length_unit
        precision = context.preferences.addons["buildplanner"].preferences.precision + int(round(math.log10(bp_defs.length_unit_scale_factor[length_unit])))

        self.report({"INFO"},"Precision: "+str(precision))

        for i in range(5): bp["progress_step"][i] = 0
    
        #
        # Step one 
        # Select wood starting wuth a specific name
        #    

        prefix = bpy.context.scene.build_planner.bp_name

        complexity = context.preferences.addons["buildplanner"].preferences.complexity

        bp["progress_step"][0] = 1
        yield True
        nwoods = 0
        woods = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH' and obj.name.startswith(prefix)]
        for wood in woods:
            nwoods += 1
            vertices_count = len(wood.data.vertices)
            if (vertices_count>complexity):
                self.report({"ERROR"},f"Build Planner: To complex object ({wood.name}) with {vertices_count} vertices. Maximum set to {complexity}. Increase if needed in addon preferences")
                yield False
            bp["progress"][0] = "Finding objects: "+str(nwoods)
            # Toggle progress to blink (0/1)
            bp["progress_step"][0] = (bp["progress_step"][1] + 1) % 2
            yield True
        bp["progress_step"][0] = 2
        if nwoods == 0:
            yield False
        else:
            yield True

        #    
        # Step two 
        # Get assumed length
        # Project all vertices along the longest edge and calculate max distance metween vertices
        # for each object. This will be base for the assumption for one of the axis 
        #

        count = 0

        # Array to store the wood size, including vectors
        wood_info = []

        for wood in woods:
            # Toggle progress to blink (0/1)
            bp["progress_step"][1] = (bp["progress_step"][1] + 1) % 2
            wood_info.append(self.align_and_calculate_max_distance(wood,precision))
            count += 1
            bp["progress"][1] = f"Identifying lengths: {count}/{nwoods}"
            yield True

        # Get a list of only dimensions
        dimensions = [(a, b, c) for ((a, _), (b, _), (c, _)) in wood_info]

        # Set step 2 to done (2)
        bp["progress_step"][1] = 2

        #
        # Step three
        # Refine Dimensions and make sure width and height is not to be confused with length
        #

        for result in self.refine_dimensions(dimensions):
            yield True
            if not result[0]:
                # Toggle progress to blink (0/1)
                bp["progress_step"][2] = (bp["progress_step"][2] + 1) % 2
                bp["progress"][2] = f"Refining dimensions: {result[1]}"

        demand = self.get_demand(result[2],precision)

        # Set step 3 to done (2)
        bp["progress_step"][2] = 2

        #
        # Step four
        # Cut the wood

        # Get the available stock lengths
        stock_inf = [
            context.scene.build_planner.bp_stock_0,
            context.scene.build_planner.bp_stock_1,
            context.scene.build_planner.bp_stock_2,
            context.scene.build_planner.bp_stock_3,
            context.scene.build_planner.bp_stock_4
        ][:context.scene.build_planner.bp_stock_variations]

        stock_inf = [round((num*unit_scale),precision) for num in stock_inf]

        # Get the available stock amounts
        stock_amount = [
            context.scene.build_planner.bp_stock_avail_0,
            context.scene.build_planner.bp_stock_avail_1,
            context.scene.build_planner.bp_stock_avail_2,
            context.scene.build_planner.bp_stock_avail_3,
            context.scene.build_planner.bp_stock_avail_4
        ][:context.scene.build_planner.bp_stock_variations]
        
        # Get cut_with and stock_inf, multiplied by unit_scale, rounded by precision
        cut_width = round(context.scene.build_planner.bp_cut_width * unit_scale, precision)
        
        stock_inf_amount = dict(zip(stock_inf,stock_amount))

        # Scale the demand to unit_scale
        if (unit_scale!=1.0):
            scaled_demand = BPDataStockPieces()
            for key,value in demand.items():
                scaled_demand[round(key*unit_scale,precision)] = value
            demand = scaled_demand

        stock = BPDataStockPieces()
        for length, amount in stock_inf_amount.items():
            if length in stock:
                stock[length] += amount 
            else:
                stock[length] = amount
            
  
        bp_cutter = BPCutter(stock,demand,cut_width,length_unit=length_unit, precision=precision)

        method = {"BOTH":BPCutter.METHOD.OPT,
                  "GREEDY":BPCutter.METHOD.GREEDY,
                  "EXPERIMENTAL":BPCutter.METHOD.EXPERIMENTAL
                  }[context.preferences.addons["buildplanner"].preferences.method]

        for result in bp_cutter.cut_iter(method):
            bp["progress_step"][3] = (bp["progress_step"][3] + 1) % 2
            bp["progress"][3] = f"Cutting ({result[1]}): {result[3]}"
            yield True

        # Set step 4 to done (2)
        bp["progress_step"][3] = 2
        
        bp["progress_step"][4] = 2
        bp["progress"][4] = f"Done, using {bp_cutter.result.method}"
        self.report({"INFO"},"Build Planner: Cutting finished")
        self.report({"INFO"},str(result[2]))

        bp["html"] = bp_cutter.result.to_html()

        bp["bp_cutter_state"]["HAS_DATA"] = True

        yield False

    def modal(self, context, event):

        # Check if user presses ESC key to cancel the operation
        if event.type in {'ESC'}:
            self.cancel(context)
            return{'CANCELLED'}
        
        # Update the UI with a timer initated in execute
        if event.type == 'TIMER':
            context.area.tag_redraw()
        
        bp = BPBlender.cutter_data
        if not bp["bp_cutter_state"]["RUNNING"]:
            context.area.tag_redraw()
            return {'FINISHED'}

        return {'RUNNING_MODAL'}
    
    def execute(self,context):

        bp = BPBlender.cutter_data

        if bp["bp_cutter_state"]["RUNNING"]:
            return {'FINISHED'}

        bp["bp_cutter_state"]["RUNNING"] = True
        
        # Initialize progress variables
        for i in range(5):
            bp["progress"][i] = ""
            bp["progress_step"][i] = 0

        # Define iterator for execution of cutter
        self._willcont = iter(self.orchestrator(context))

        # Initiate modal - making it possible to cacel the operation by clicking ESC
        context.window_manager.modal_handler_add(self)

        # Initiate the cutting by using a timer for each step of the iteration
        bpy.app.timers.register(self.cut_wood, first_interval=0.0)

        # Initiate a timer to udate the UI with progress info
        self._timer = context.window_manager.event_timer_add(0.1, window=context.window)

        return {'RUNNING_MODAL'}
    
    def cut_wood(self):

        # bp data
        bp = BPBlender.cutter_data

        # Repeat the cutting steps until finished. If the process is cancelled, the object will be deleted, creating a reference error
        try:
            if next(self._willcont):
                return 0.0
            else:
                bp["bp_cutter_state"]["RUNNING"] = False
                return None
        except ReferenceError:
            bp["bp_cutter_state"]["RUNNING"] = False
            return None


    def cancel(self, context):

        # bp data
        bp = BPBlender.cutter_data

        # Update operation state to not running and redraw area
        bp["bp_cutter_state"]["RUNNING"] = False

        context.window_manager.event_timer_remove(self._timer)

        # Update UI
        context.area.tag_redraw()

        # Report cancellation
        self.report({"WARNING"}, "Build Planner: Cutting cancelled by user [ESC]")