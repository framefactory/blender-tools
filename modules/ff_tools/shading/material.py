from typing import cast

import bpy
import bpy.types as bt


def create_node_material(name: str):
    """Creates and returns a new node-based shader material."""
    material = bpy.data.materials.new(name)
    material.use_nodes = True
    return material


def assign_material_to_active(material: bt.Material):
    """Assigns the given material to the active slot
       or to a new slot of the active mesh object."""
    
    slot = bpy.context.material_slot
    if slot:
        slot.material = material
        return

    obj = bpy.context.active_object
    if obj.type == "MESH":
        data = cast(bt.Mesh, obj.data)
        data.materials.append(material)

