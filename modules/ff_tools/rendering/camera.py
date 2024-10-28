# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from math import radians, tan

import bpy
import bpy.types as bt

from ff_tools.geometry.inspect import get_bounding_box


def create_camera(name: str, collection: bt.Collection = None) -> tuple[bt.Object, bt.Camera]:
    """
    Creates a new camera object with the given name and adds it to the given collection.
    """
    camera = bpy.data.cameras.new(name)
    object = bpy.data.objects.new(name, camera)

    collection = collection or bpy.context.collection
    collection.objects.link(object)
    return object, camera


def remove_camera_by_name(name: str):
    """
    Removes a camera by its name.
    """
    camera = bpy.data.cameras[name]
    bpy.data.cameras.remove(camera)


def get_objects_for_camera(camera: bt.Camera) -> list[bt.Object]:
    """
    Returns all objects in the scene that are linked to the given camera.
    """
    return [ obj for obj in bpy.data.objects if obj.type == "CAMERA" and obj.data == camera ]


def get_all_camera_objects() -> list[bt.Object]:
    """
    Returns all camera objects in the scene.
    """
    return [ obj for obj in bpy.data.objects if obj.type == "CAMERA" ]


def load_background_image(camera: bt.Camera, image_path: str, check_existing=False) -> bt.CameraBackgroundImage:
    image = bpy.data.images.load(image_path, check_existing=check_existing)
    return set_background_image(camera, image)


def set_background_image(camera: bt.Camera, image: bt.Image) -> bt.CameraBackgroundImage:
    bg_image = camera.background_images.new()
    bg_image.image = image
    bg_image.alpha = 1.0
    bg_image.show_background_image = True
    return bg_image

def camera_dolly_frame_object(
    camera: bt.Object,
    dolly: bt.Object,
    target: bt.Object,
    orientation: float,
    tilt: float,
    zoom: float = 1.0,
):
    """
    Adjusts the camera and dolly to frame the target object.
    The camera must be a direct child of the dolly object.
    The tilt angle (in degrees) affects the dolly's tilt.
    The orientation angle (in degrees) affects the target orientation.
    The zoom factor scales the distance to the target. Values < 1
    zoom in on the target, values > 1 move further away.
    """
    cam_data: bt.Camera = camera.data
    fov = cam_data.angle

    # set camera, dolly, and object rotation
    camera.rotation_euler = (radians(90), 0, 0)
    dolly.rotation_euler = (radians(tilt), 0, 0)
    target.rotation_euler = (0, 0, radians(orientation))

    # ensure matrices are updated for bounding box calculation
    bpy.context.evaluated_depsgraph_get()
    
    # Aligns the object such that is centered by x and y
    # and its bottom aligned with the xy-plane.
    bb = get_bounding_box(target)
    center = (bb[0] + bb[1]) * 0.5
    extent = bb[1] - bb[0]
    target.location -= center
    target.location.z += extent.z * 0.5

    # center dolly on object
    dolly.location = (0, 0, extent.z * 0.5)

    # calculate and set camera distance
    bb = get_bounding_box(target, camera) # bounding box in camera space
    extent = bb[1] - bb[0]
    distance = extent.y * 0.4
    distance += max(extent) / (2 * tan(fov / 2))
    camera.location = (0, -distance * zoom, 0)