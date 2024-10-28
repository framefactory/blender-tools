# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from pathlib import Path
import logging

import bpy
from bpy import types as bt
from bpy import ops

from ff_tools.core.collection import move_obj_to_collection


logger = logging.getLogger(__name__)


def import_model(
    file_path: str|Path,
    collection: bt.Collection,
    obj_name: str = None
) -> bt.Object:
    """
    Import a model from a file and move it to the given collection.
    All imported elements are parented to a root object, which is returned.
    The root object is named `obj_name` if given, or else the file name.
    Supported file formats are .blend, .gltf, .glb, .usd, .usda, .usdz.
    Important: In order for the grouping to work, the root collection must not
    contain any other objects, only child collections.
    """
    file_path = Path(file_path)
    file_base = file_path.stem
    file_ext = file_path.suffix.lower()

    # blender doesn't like Path objects
    file_path = str(file_path)

    if not obj_name:
        obj_name = f"{file_base}_{file_ext[1:].lower()}"

    # get root collection
    scene_collection = bpy.context.scene.collection

    if file_ext.startswith(".blend"):
        try:
            with bpy.data.libraries.load(file_path) as (data_from, data_to):
                data_to.objects = [ name for name in data_from.objects ]

        except Exception as e:
            logger.warning(f"failed to import from blend file: '{file_path}'")
            logger.warning(e)
            return None

        if len(data_to.objects) == 0:
            return None

        imported_objs = list(data_to.objects)

    if file_ext in (".gltf", ".glb"):
        try:
            ops.import_scene.gltf(filepath=file_path, loglevel=50)
        except Exception as e:
            logger.warning(f"failed to import model from gltf/glb '{file_path}'")
            logger.warning(e)
            return None
        
        imported_objs = list(scene_collection.objects)

    elif file_ext in ("usd", ".usda", ".usdz"):
        try:
            ops.wm.usd_import(filepath=file_path)
        except Exception as e:
            logger.warning(f"failed to import model from usd: '{file_path}'")
            logger.warning(e)
            return None
        
        imported_objs = list(scene_collection.objects)

    # move imported objects to collection
    for imported_obj in imported_objs:
        move_obj_to_collection(imported_obj, collection)

    # create root object
    root_obj = bpy.data.objects.new(obj_name, None)
    move_obj_to_collection(root_obj, collection)

    for imported_obj in imported_objs:
        if imported_obj.parent == None:
            imported_obj.parent = root_obj

    # deselect all
    ops.object.select_all(action='DESELECT')

    return root_obj