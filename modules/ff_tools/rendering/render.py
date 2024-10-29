# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

from pathlib import Path
import bpy


def render_still_png(width: int, height: int, transparent: bool, file_path: Path|str):
    """
    Renders the current scene to a PNG file with the given width and height.
    """
    bpy.context.workspace.status_text_set(f"Rendering PNG frame to {file_path}")

    render = bpy.context.scene.render
    render.film_transparent = transparent
    
    render.resolution_x = width
    render.resolution_y = height
   
    render.image_settings.file_format = "PNG"
    render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    render.image_settings.compression = 80
    render.filepath = str(file_path)

    bpy.ops.render.render(write_still=True)


def render_still_jpeg(width: int, height: int, quality: int, file_path: Path|str):
    """
    Renders the current scene to a JPEG file with the given width, height and quality.
    """
    bpy.context.workspace.status_text_set(f"Rendering JPEG frame to {file_path}")

    render = bpy.context.scene.render
    render.film_transparent = False
    
    render.resolution_x = width
    render.resolution_y = height
    
    render.image_settings.file_format = "JPEG"
    render.image_settings.color_mode = "RGB"
    render.image_settings.quality = quality
    render.filepath = str(file_path)

    bpy.ops.render.render(write_still=True)


def render_viewport(width: int, height: int, quality: int, file_path: Path|str):
    """
    Renders the current viewport to the given file path.
    """
    bpy.context.workspace.status_text_set(f"Rendering viewport to {file_path}")

    render = bpy.context.scene.render
    render.film_transparent = False

    render.resolution_x = width
    render.resolution_y = height
    
    render.image_settings.file_format = "JPEG"
    render.image_settings.color_mode = "RGB"
    render.image_settings.quality = quality
    render.filepath = str(file_path)

    bpy.ops.render.opengl(write_still=True)