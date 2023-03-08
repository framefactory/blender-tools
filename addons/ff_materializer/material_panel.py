import bpy
from bpy import types as bt


class FF_MATERIALIZER_PT_material_panel(bt.Panel):
    bl_category = "Frame Factory"
    bl_label = "FF Material Builder"
    #bl_idname = "FF_MATERIALIZER_PT_material_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"

    def draw(self, context: bt.Context):
        grid = self.layout.grid_flow(columns=2)
        grid.operator("ff_materializer.import_material", icon="ADD")
        grid.operator("ff_materializer.create_material", icon="ADD")

        col = self.layout.column()
        col.operator("ff_materializer.reload", icon="FILE_REFRESH")
        #col.operator("script.reload", icon="FILE_REFRESH")

        #col = self.layout.column()
        #col.use_property_split = True
        #col.prop(context.scene.render, "film_transparent")


def register_module():
    bpy.utils.register_class(FF_MATERIALIZER_PT_material_panel)


def unregister_module():
    bpy.utils.unregister_class(FF_MATERIALIZER_PT_material_panel)
