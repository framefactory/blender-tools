from typing import Tuple, List

import bpy
import bpy.types as bt


def create_camera(name: str, collection: bt.Collection = None) -> Tuple[bt.Object, bt.Camera]:
    camera = bpy.data.cameras.new(name)
    object = bpy.data.objects.new(name, camera)

    collection = collection or bpy.context.collection
    collection.objects.link(object)
    return object, camera


def remove_camera_by_name(name: str):
    camera = bpy.data.cameras[name]
    bpy.data.cameras.remove(camera)


def get_objects_for_camera(camera: bt.Camera) -> List[bt.Object]:
    return [ obj for obj in bpy.data.objects if obj.type == "CAMERA" and obj.data == camera ]


def get_all_camera_objects() -> List[bt.Object]:
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
