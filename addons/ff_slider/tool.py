# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import logging

import bpy
from bpy import types as bt
from bpy import props as bp


logger = logging.getLogger(__name__)


class FF_SLIDER_TOOL_slide_edge(bt.WorkSpaceTool):
    bl_space_type = 'VIEW_3D'
    bl_context_mode = 'EDIT_MESH'

    bl_idname = "ff_slider.slide_edge"
    bl_label = "Slide Edge"
    bl_description = "Slide edge along adjacent edges"
    
    #bl_icon = "ops.transform.edge_slide"
    bl_icon = "ops.mesh.loopcut_slide"

    bl_keymap = (
        ("ff_slider.slide_edge", {"type": 'LEFTMOUSE', "value": 'PRESS'}, {"properties": [("tool_mode", "DEFAULT" )]}),
        ("ff_slider.slide_edge", {"type": 'LEFTMOUSE', "value": 'PRESS', "shift": True}, {"properties": [("tool_mode", "SHIFT")]}),
        ("ff_slider.slide_edge", {"type": 'LEFTMOUSE', "value": 'PRESS', "ctrl": True}, {"properties": [("tool_mode", "CONTROL")]}),
        ("ff_slider.slide_edge", {"type": 'LEFTMOUSE', "value": 'PRESS', "alt": True}, {"properties": [("tool_mode", "ALT")]}),
        ("ff_slider.slide_edge", {"type": 'LEFTMOUSE', "value": 'PRESS', "shift": True, "ctrl": True}, {"properties": [("tool_mode", "SHIFT_CONTROL")]}),
    )

    def draw_settings(context, layout, tool):
        pass
        #layout.prop(tool, "use_even")
        #layout.prop(tool.operator_properties, "some_property")


# ------------------------------------------------------------------------------

def register_module():
    bpy.utils.register_tool(FF_SLIDER_TOOL_slide_edge, separator=True, group=True)

def unregister_module():
    bpy.utils.unregister_tool(FF_SLIDER_TOOL_slide_edge)

