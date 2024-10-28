# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from typing import Optional
import logging

import bpy
from bpy import types as bt


logger = logging.getLogger(__name__)


def create_collection(name: str, parent: Optional[bt.Collection] = None) -> bt.Collection:
    """Creates a new collection with the given name and parent."""
    collection = bpy.data.collections.get(name)
    
    if collection is not None:
        logger.warning(f"Collection '{name}' already exists.")
        return collection
    
    collection = bpy.data.collections.new(name)
    parent = parent or bpy.context.scene.collection
    parent.children.link(collection)

    return collection


def remove_collection(collection: bt.Collection):
    """Removes the given collection and all its children."""
    for child in collection.children:
        remove_collection(child)

    # First remove all objects in the collection
    for obj in collection.objects:
        collection.objects.unlink(obj)
        
        # If the object is not linked to any other collections, remove it completely
        if len(obj.users_collection) == 0:
            bpy.data.objects.remove(obj, do_unlink=True)
    
    # Now remove the collection itself
    bpy.data.collections.remove(collection, do_unlink=True)


def move_obj_to_collection(obj: bt.Object, collection: bt.Collection):
    """Moves an object to a collection and unlinks it from all other collections."""
    # unlink obj from other collections
    for col in obj.users_collection:
        col.objects.unlink(obj)

    # link obj to target collection
    collection.objects.link(obj)


def get_root_objects(collection: bt.Collection) -> list[bt.Object]:
    """returns a list of all objects in the collection that have no parent."""
    return [ obj for obj in collection.objects if obj.parent is None ]


def get_first_root_object(collection: bt.Collection) -> Optional[bt.Object]:
    """returns the first object in the collection that has no parent."""

    for obj in collection.objects:
        if obj.parent is None:
            return obj

    return None