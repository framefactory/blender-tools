# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import logging

import bpy
from bpy import types as bt

from . import register, unregister


logger = logging.getLogger(__name__)


class FF_BOOSTER_OP_test(bt.Operator):
    bl_idname = "ff_booster.test"
    bl_label = "Test"
    bl_description = "Test add-on"

    def execute(self, context: bt.Context):
        return {"FINISHED"}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Test")


# ------------------------------------------------------------------------------

class FF_BOOSTER_OP_reload(bt.Operator):
    bl_idname = "ff_booster.reload"
    bl_label = "Reload"
    bl_description = "Reload add-on"

    def execute(self, context: bt.Context):
        unregister()
        register()
        return {"FINISHED"}
    
# ------------------------------------------------------------------------------

def register_module():
    bpy.utils.register_class(FF_BOOSTER_OP_test)
    bpy.utils.register_class(FF_BOOSTER_OP_reload)


def unregister_module():
    bpy.utils.unregister_class(FF_BOOSTER_OP_reload)
    bpy.utils.unregister_class(FF_BOOSTER_OP_test)