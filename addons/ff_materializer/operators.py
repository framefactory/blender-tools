import bpy
from bpy import types as bt
from bpy import props as bp
from bpy_extras.io_utils import ImportHelper

from ff_tools.shading.world_builder import IBLWorldBuilder

from . import register, unregister
from .material_factory import MaterialFactory, ResolutionEnumItems


resolution_enum_items: ResolutionEnumItems = []


def _get_resolution_items(self, context):
    return resolution_enum_items 


class FF_MATERIALIZER_OP_create_material(bt.Operator, ImportHelper):
    bl_idname = "ff_materializer.create_material"
    bl_label = "Create Material"
    bl_description = "Import textures and create PBR material"

    filepath: bp.StringProperty(subtype="FILE_PATH") #type:ignore
    filter_glob: bp.StringProperty(default="*.zip;*.jpg;*.png;*.tif;*.exr;*.webp") #type:ignore
    resolution: bp.EnumProperty(name="Resolution", items=_get_resolution_items) #type:ignore

    def __init__(self):
        super().__init__()
        self._factory = MaterialFactory()

    @classmethod
    def poll(cls, context: bt.Context):
        return True

    def check(self, _context: bt.Context):
        if self.filepath:
            global resolution_enum_items
            self._factory.set_path(self.filepath)
            resolution_enum_items = self._factory.get_resolution_enum()
            self._factory.dump()
            return True

        return False

    def execute(self, context: bt.Context):
        resolution = str(self.resolution)
        tex_path = bpy.path.abspath("//textures")
        self._factory.create_material(resolution, tex_path)

        return {"FINISHED"}

    def draw(self, _context):
        layout = self.layout
        layout.label(text="Texture Resolution")
        layout.prop(self, "resolution", expand=True)

# ------------------------------------------------------------------------------

class FF_MATERIALIZER_OP_create_world(bt.Operator):
    bl_idname = "ff_materializer.create_world"
    bl_label = "Create World"
    bl_description = "Import environment image and create world"

    filepath: bp.StringProperty(subtype="FILE_PATH") #type:ignore

    @classmethod
    def poll(cls, context: bt.Context): #type:ignore
        return context.scene.world is not None

    def execute(self, context: bt.Context):
        world = context.scene.world
        world.use_nodes = True
        builder = IBLWorldBuilder(world.node_tree)
        builder.load_environment_image(self.filepath)
        return {"FINISHED"}

    def invoke(self, context: bt.Context, event: bt.Event):
        context.window_manager.fileselect_add(self)
        return {"RUNNING_MODAL"}

# ------------------------------------------------------------------------------

class FF_MATERIALIZER_OP_reload(bt.Operator):
    bl_idname = "ff_materializer.reload"
    bl_label = "Reload"
    bl_description = "Reload add-on"

    def execute(self, context: bt.Context):
        unregister()
        register()
        return {"FINISHED"}

# ------------------------------------------------------------------------------

def register_module():
    bpy.utils.register_class(FF_MATERIALIZER_OP_create_material)
    bpy.utils.register_class(FF_MATERIALIZER_OP_create_world)
    bpy.utils.register_class(FF_MATERIALIZER_OP_reload)


def unregister_module():
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_reload)
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_create_world)
    bpy.utils.unregister_class(FF_MATERIALIZER_OP_create_material)
