# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import bpy

def set_cycles_device_type(device_type: str):
    """
    Sets the compute device type for Cycles rendering to the given type.
    The type must be one of "NONE", "CUDA", "OPTIX", "HIP" or "ONEAPI".
    The preferred type for NVIDIA GPUs is "OPTIX".
    """
    preferences = bpy.context.preferences
    cycles_prefs = preferences.addons["cycles"].preferences
    cycles_prefs.compute_device_type = device_type


def get_cycles_device_names():
    """
    Returns a list of names of all available compute devices for Cycles rendering.
    First call set_cycles_device_type() to set the device type for which to get the devices.
    """
    preferences = bpy.context.preferences
    cycles_prefs = preferences.addons["cycles"].preferences
    cycles_prefs.get_devices()

    return [ device.name for device in cycles_prefs.devices ]


def set_cycles_device(device_name: str):
    """
    Sets the compute device for Cycles rendering to the device with the given name.
    """
    preferences = bpy.context.preferences
    cycles_prefs = preferences.addons["cycles"].preferences
    cycles_prefs.get_devices()

    for device in cycles_prefs.devices:
        device.use = (device.name == device_name)
