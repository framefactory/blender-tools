# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import logging

import bpy
from bpy import types as bt
from bpy import props as bp

logger = logging.getLogger(__name__)


class FF_SLIDER_OP_slide_edge(bt.Operator):
    bl_idname = "ff_slider.slide_edge"
    bl_label = "Slide Edge"
    bl_description = "Slide edge along adjacent edges"

    tool_mode: bp.StringProperty(name="MODE", default="DEFAULT") # type: ignore

    def execute(self, context):
        logger.info(f"FF_SLIDER_OP_slide_edge.execute: {self.tool_mode}")
        return {"FINISHED"}


    def draw(self, context):
        layout = self.layout
        layout.label(text="Edge Slide")

# ------------------------------------------------------------------------------

def register_module():
    bpy.utils.register_class(FF_SLIDER_OP_slide_edge)

def unregister_module():
    bpy.utils.unregister_class(FF_SLIDER_OP_slide_edge)
