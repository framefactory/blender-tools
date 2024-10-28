# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import bpy


def redraw():
    """
    Redraw the Blender window.
    """
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)