from typing import cast

import bpy
from bpy import types as bt


class VIEW3D_PT_ff_materializer_world_panel(bt.Panel):
    bl_category = "Frame Factory"
    bl_label = "World Builder"
    bl_idname = "VIEW3D_PT_ff_materializer_world_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "world"

    def draw(self, context: bt.Context):
        col = self.layout.column()
        col.operator("ff_materializer.create_world", icon="ADD")
        col.operator("ff_materializer.reload", icon="FILE_REFRESH")

        col = self.layout.column()
        col.use_property_split = True
        render_settings = cast(bt.AnyType, context.scene.render)
        col.prop(render_settings, "film_transparent")


def register_module():
    bpy.utils.register_class(VIEW3D_PT_ff_materializer_world_panel)


def unregister_module():
    bpy.utils.unregister_class(VIEW3D_PT_ff_materializer_world_panel)
