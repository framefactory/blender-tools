import bpy
from bpy import types as bt


class VIEW3D_PT_ff_materializer_material_panel(bt.Panel):
    bl_category = "Frame Factory"
    bl_label = "Material Builder"
    bl_idname = "VIEW3D_PT_ff_materializer_material_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context: bt.Context):
        col = self.layout.column()
        col.operator("ff_materializer.create_material", icon="ADD")
        col.operator("script.reload", icon="FILE_REFRESH")

        #col = self.layout.column()
        #col.use_property_split = True
        #col.prop(context.scene.render, "film_transparent")


def register_module():
    bpy.utils.register_class(VIEW3D_PT_ff_materializer_material_panel)


def unregister_module():
    bpy.utils.unregister_class(VIEW3D_PT_ff_materializer_material_panel)
