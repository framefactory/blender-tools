from typing import List, Any, Optional

import bpy
import bpy.types as bt


def get_objects_by_type(type: str) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.type == type ]


def get_objects_for_data(data: Any) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.data == data ]


def get_first_object_for_data(data: Any) -> Optional[bt.Object]:
    for obj in bpy.data.objects:
        if obj.data == data:
            return obj
    return None
