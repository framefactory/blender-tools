from typing import List

import bpy
import bpy.types as bt


def get_objects_by_type(type: str) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.type == type ]