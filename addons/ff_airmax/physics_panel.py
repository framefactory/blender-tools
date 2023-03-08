from typing import cast

import bpy
from bpy import types as bt


class VIEW3D_PT_ff_airmax_physics_panel(bt.Panel):
    bl_category = "Frame Factory"
    bl_label = "FF Airmax Cloth Helper"
    bl_idname = "VIEW3D_PT_ff_airmax_physics_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "physics"

    def draw(self, context: bt.Context):
        grid = self.layout.grid_flow(columns=2)
        grid.operator("ff_airmax.add_sewn_pillow_cloth", icon="MOD_CLOTH")
        grid.operator("ff_airmax.bake_cloth_modifier", icon="PINNED")
        grid.operator("ff_airmax.remove_stitches", icon="AUTOMERGE_ON")

        col = self.layout.column()
        col.operator("ff_airmax.reload", icon="FILE_REFRESH")

        #col = self.layout.column()
        #col.use_property_split = True
        #render_settings = cast(bt.AnyType, context.scene.render)
        #col.prop(render_settings, "film_transparent")


def register_module():
    bpy.utils.register_class(VIEW3D_PT_ff_airmax_physics_panel)


def unregister_module():
    bpy.utils.unregister_class(VIEW3D_PT_ff_airmax_physics_panel)