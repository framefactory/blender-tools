import json

import bpy
from bpy import types as bt
from bpy import props as bp
from bpy_extras.io_utils import ImportHelper

from . import register, unregister
from .material_factory import MaterialFactory
from .world_factory import WorldFactory


class FF_MATERIALIZER_OP_reload(bt.Operator):
    bl_idname = "ff_materializer.reload"
    bl_label = "Reload"
    bl_description = "Reload add-on"

    def execute(self, context: bt.Context):
        unregister()
        register()
        return {"FINISHED"}

_resolution_items = []

def _get_resolution_items(self, context):
    return _resolution_items 

class FF_MATERIALIZER_OP_create_material(bt.Operator, ImportHelper):
    bl_idname = "ff_materializer.create_material"
    bl_label = "Create Material"
    bl_description = "Import textures and create PBR material"

    filepath: bp.StringProperty(subtype="FILE_PATH")
    filter_glob: bp.StringProperty(default="*.zip;*.jpg;*.png;*.tif;*.exr")
    resolution: bp.EnumProperty(name="Resolution", items=_get_resolution_items)

    def __init__(self):
        super().__init__()
        self._factory = MaterialFactory()

    @classmethod
    def poll(cls, context: bt.Context):
        return True

    def check(self, _context: bt.Context):
        if self.filepath:
            global _resolution_items
            _resolution_items = self._factory.analyze_file_path(self.filepath)
            return True

        return False

    def execute(self, context: bt.Context):
        #factory = MaterialFactory(context)
        #factory.open_zip(self.filepath)
        # if factory.get_environment_texture_node() is None:
        #     factory.create_world()

        # factory.load_environment_image(self.filepath)
        return {"FINISHED"}

    # def invoke(self, context: bt.Context, event: bt.Event):
    #     context.window_manager.fileselect_add(self)
    #     return {"RUNNING_MODAL"}

    def draw(self, _context):
        layout = self.layout
        layout.label(text="Texture Resolution")
        layout.prop(self, "resolution", expand=True)

class FF_MATERIALIZER_OP_create_world(bt.Operator):
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
    bpy.utils.register_class(FF_MATERIALIZER_OP_reload)
    bpy.utils.register_class(FF_MATERIALIZER_OP_create_material)
    bpy.utils.register_class(FF_MATERIALIZER_OP_create_world)


def unregister_module():
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_create_world)
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_create_material)
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_reload)
