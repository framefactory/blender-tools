from typing import cast

import bpy
from bpy import types as bt

from . import register, unregister


# ------------------------------------------------------------------------------

class FF_AIRMAX_OP_add_sewn_pillow_cloth(bt.Operator):
    bl_idname = "ff_airmax.add_sewn_pillow_cloth"
    bl_label = "Add Sewn Pillow Cloth"
    bl_description = "Add cloth modifier with custom settings"

    @classmethod
    def poll(cls, context: bt.Context):
        return True

    def execute(self, context: bt.Context):
        obj = context.active_object
        mod = cast(bt.ClothModifier, obj.modifiers.new("Pillow Cloth", 'CLOTH'))

        mod.settings.quality = 7
        mod.settings.mass = 0.01
        mod.settings.shear_stiffness = 5.0
        mod.settings.bending_stiffness = 15.0

        mod.settings.use_pressure = True
        mod.settings.uniform_pressure_force = 3.5

        mod.settings.use_sewing_springs = True

        mod.collision_settings.use_self_collision = True
        mod.collision_settings.distance_min = 0.001
        mod.collision_settings.self_distance_min = 0.001
        mod.collision_settings.collision_quality = 5

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class FF_AIRMAX_OP_bake_cloth_modifier(bt.Operator):
    bl_idname = "ff_airmax.bake_cloth_modifier"
    bl_label = "Bake Cloth Modifier"
    bl_description = "Duplicate with baked cloth modifier"

    @classmethod
    def poll(cls, context: bt.Context):
        return True

    def execute(self, context: bt.Context):
        obj = context.active_object
        base_name = obj.name
        obj.name = f"{base_name} BAKE"

        bpy.ops.object.duplicate(mode='DUMMY')
        bpy.context.active_object.name = base_name

        context.view_layer.objects.active = obj

        for modifier in obj.modifiers:
            bpy.ops.object.modifier_apply(modifier=modifier.name)
            if modifier.type == 'CLOTH':
                break

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class FF_AIRMAX_OP_remove_stitches(bt.Operator):
    bl_idname = "ff_airmax.remove_stitches"
    bl_label = "Remove Stitches"
    bl_description = "Delete loose edges"

    @classmethod
    def poll(cls, context: bt.Context):
        return True

    def execute(self, context: bt.Context):
        obj = context.active_object
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.delete_loose(use_verts=False, use_edges=True)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='OBJECT')

        return {'FINISHED'}

# ------------------------------------------------------------------------------

class FF_AIRMAX_OP_reload(bt.Operator):
    bl_idname = "ff_airmax.reload"
    bl_label = "Reload"
    bl_description = "Reload add-on"

    def execute(self, context: bt.Context):
        unregister()
        register()

        return {'FINISHED'}

# ------------------------------------------------------------------------------

def register_module():
    bpy.utils.register_class(FF_AIRMAX_OP_add_sewn_pillow_cloth)
    bpy.utils.register_class(FF_AIRMAX_OP_bake_cloth_modifier)
    bpy.utils.register_class(FF_AIRMAX_OP_remove_stitches)
    bpy.utils.register_class(FF_AIRMAX_OP_reload)


def unregister_module():
    bpy.utils.unregister_class(FF_AIRMAX_OP_reload)
    bpy.utils.unregister_class(FF_AIRMAX_OP_remove_stitches)
    bpy.utils.unregister_class(FF_AIRMAX_OP_bake_cloth_modifier)
    bpy.utils.unregister_class(FF_AIRMAX_OP_add_sewn_pillow_cloth)
