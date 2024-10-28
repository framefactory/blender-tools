# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from typing import cast
from bpy import types as bt
from mathutils import Vector
from math import inf


def get_bounding_box(obj: bt.Object, camera: bt.Object=None, recursive=True):
    """returns a tuple of (min, max) vectors describing the axis aligned
       bounding box of the given object (in world or camera coordinates)"""
    v_min = Vector((inf, inf, inf))
    v_max = Vector((-inf, -inf, -inf))
    _get_bound_box_recursive(v_min, v_max, obj, camera, recursive)
    return (v_min, v_max)


def _get_bound_box_recursive(v_min: Vector, v_max: Vector, obj: bt.Object, camera: bt.Object, recursive=True):
    mat = obj.matrix_world
    if camera:
        mat = camera.convert_space(matrix=mat, from_space='WORLD', to_space='LOCAL')

    bb = [ mat @ Vector(corner) for corner in obj.bound_box ] # world or camera space
    for v in bb:
        for i in range(3):
            v_min[i] = min(v_min[i], v[i])
            v_max[i] = max(v_max[i], v[i])

    if recursive:
        for child in obj.children:
            _get_bound_box_recursive(v_min, v_max, child, camera, recursive)


def get_pose_info(obj: bt.Object) -> dict:
    """Returns a dictionary with information about the center,
    dimensions and boundaries of the object."""
    # dimensions in cm
    bb = get_bounding_box(obj)
    mins = bb[0]
    maxs = bb[1]
    dimensions = (bb[1] - bb[0])
    center = (bb[0] + bb[1]) * 0.5

    pose = {
        "axis": "blender",
        "unit": "m",
        "center": {
            "x": center.x,
            "y": center.y,
            "z": center.z,
        },
        "dimensions": {
            "x": dimensions.x,
            "y": dimensions.y,
            "z": dimensions.z,
        },
        "bounds": {
            "min": {
                "x": mins.x,
                "y": mins.y,
                "z": mins.z,
            },
            "max": {
                "x": maxs.x,
                "y": maxs.y,
                "z": maxs.z,
            },
        }
    }

    return pose

def get_vertex_count(obj: bt.Object) -> int:
    """returns the total number of vertices in the object and all its children."""
    if obj.type == 'MESH':
        data = cast(bt.Mesh, obj.data)
        count = len(data.vertices)
    else:
        count = 0
    
    for child in obj.children:
        count += get_vertex_count(child)

    return count


def get_face_count(obj: bt.Object) -> int:
    """returns the total number of faces in the object and all its children."""
    if obj.type == 'MESH':
        data = cast(bt.Mesh, obj.data)
        count = len(data.polygons)
    else:
        count = 0
    
    for child in obj.children:
        count += get_face_count(child)

    return count


def get_polygon_types(obj: bt.Object) -> tuple[int, int, int]:
    """returns the number of triangles, quads, and ngons in the object
       and all its children."""
    tris = 0
    quads = 0
    ngons = 0

    if obj.type == 'MESH':
        data = cast(bt.Mesh, obj.data)

        for poly in data.polygons:
            if len(poly.vertices) == 3:
                tris += 1
            elif len(poly.vertices) == 4:
                quads += 1
            else:
                ngons += 1

    for child in obj.children:
        t, q, n = get_polygon_types(child)
        tris += t
        quads += q
        ngons += n

    return tris, quads, ngons


def get_materials(obj: bt.Object) -> set[bt.Material]:
    """returns a list of all materials assigned to the object
       and its children."""
    materials = set()

    for slot in obj.material_slots:
        if slot and slot.material:
            materials.add(slot.material)

    for child in obj.children:
        materials = materials.union(get_materials(child))

    return materials

