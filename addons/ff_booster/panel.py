# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import logging

import bpy
from bpy import types as bt


logger = logging.getLogger(__name__)


class VIEW3D_PT_ff_booster(bt.Panel):
    bl_category = "FF Booster"
    bl_label = "Booster"
    bl_idname = "VIEW3D_PT_ff_booster"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context: bt.Context):
        layout = self.layout
        scene = context.scene

        box3 = layout.box()
        box3.label(text="Development")
        box3.operator("ff_booster.test")
        box3.operator("ff_booster.reload")


def register_module():
    bpy.utils.register_class(VIEW3D_PT_ff_booster)


def unregister_module():
    bpy.utils.unregister_class(VIEW3D_PT_ff_booster)