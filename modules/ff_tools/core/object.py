from typing import List, Any, Optional

import bpy
import bpy.types as bt

def set_named_object_visibility(name: str, visible: bool = True, recursive: bool = True):
    obj = bpy.data.objects.get(name)
    if obj:
        set_object_visibility(obj, visible, recursive)

def set_object_visibility(obj: bt.Object, visible=True, recursive=True):
    obj.hide_viewport = not visible
    obj.hide_render = not visible
    
    # Recursively process all children
    if recursive:
        for child in obj.children:
            set_object_visibility(child, visible, True)            


def get_objects_by_type(type: str) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.type == type ]


def get_objects_for_data(data: Any) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.data == data ]


def get_first_object_for_data(data: Any) -> Optional[bt.Object]:
    for obj in bpy.data.objects:
        if obj.data == data:
            return obj
    return None
