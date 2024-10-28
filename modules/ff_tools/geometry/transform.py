# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import bpy
from bpy import types as bt

from .inspect import get_bounding_box


def center_model_upright(obj: bt.Object):
    """Aligns the object such that is centered by x and y
       and its bottom aligned with the xy-plane."""
    # reset orientation
    obj.rotation_euler = (0, 0, 0)
    
    # ensure matrices are updated for bounding box calculation
    bpy.context.evaluated_depsgraph_get()

    bb = get_bounding_box(obj)
    center = (bb[0] + bb[1]) * 0.5
    extent = bb[1] - bb[0]
    obj.location -= center
    obj.location.z += extent.z * 0.5