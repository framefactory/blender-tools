import bpy
from bpy import types as bt
from bpy import props as bp

from . import register, unregister
from .material_factory import MaterialFactory
from .world_factory import WorldFactory


class OP_ff_materializer_reload(bt.Operator):
    bl_idname = "ff_materializer.reload"
    bl_label = "Reload"
    bl_description = "Reload add-on"

    def execute(self, context: bt.Context):
        unregister()
        register()
        return {"FINISHED"}


class OP_ff_materializer_create_material(bt.Operator):
    bl_idname = "ff_materializer.create_material"
    bl_label = "Create Material"
    bl_description = "Import textures and create PBR material"

    filepath: bp.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context: bt.Context):
        return True
        #return MaterialFactory.has_active_world(context)

    def check(self, _context: bt.Context):
        print(f"check: {self.filepath}")
        return False

    def execute(self, context: bt.Context):
        factory = MaterialFactory(context)
        factory.open_zip(self.filepath)
        # if factory.get_environment_texture_node() is None:
        #     factory.create_world()

        # factory.load_environment_image(self.filepath)
        return {"FINISHED"}

    def invoke(self, context: bt.Context, event: bt.Event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


class OP_ff_materializer_create_world(bt.Operator):
    bl_idname = "ff_materializer.create_world"
    bl_label = "Create World"
    bl_description = "Import environment image and create world"

    filepath: bp.StringProperty(subtype="FILE_PATH")

    @classmethod
    def poll(cls, context: bt.Context):
        return WorldFactory.has_active_world(context)

    def execute(self, context: bt.Context):
        factory = WorldFactory(context)
        if factory.get_environment_texture_node() is None:
            factory.create_world()

        factory.load_environment_image(self.filepath)
        return {"FINISHED"}

    def invoke(self, context: bt.Context, event: bt.Event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}


def register_module():
    bpy.utils.register_class(OP_ff_materializer_reload)
    bpy.utils.register_class(OP_ff_materializer_create_material)
    bpy.utils.register_class(OP_ff_materializer_create_world)


def unregister_module():
    bpy.utils.unregister_class(OP_ff_materializer_create_world)
    bpy.utils.unregister_class(OP_ff_materializer_create_material)
    bpy.utils.unregister_class(OP_ff_materializer_reload)
