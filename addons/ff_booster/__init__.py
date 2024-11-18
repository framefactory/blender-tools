# Blender Tools
# Copyright 2024 Ralph Wiedemeier, Frame Factory GmbH
# License: MIT

import importlib
import sys
import logging

logging.basicConfig(
    force=True,
    level=logging.DEBUG,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

package = "ff_booster"

bl_info = {
    "name": "FF Booster",
    "descriptor": "Collection of Blender power tools",
    "author": "Ralph Wiedemeier",
    "category": "Object",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
}

registered_modules = [
    "ff_booster.operators",
    "ff_booster.panel",
]

all_modules = registered_modules + [
]


logger = logging.getLogger(package)


def register():
    # ensure all modules are up to date
    for name in all_modules:
        logger.debug(f"reload module: {name}")
        importlib.import_module(name)
        module = sys.modules[name]
        importlib.reload(module)

    # call per-module registration
    for name in registered_modules:
        logger.debug(f"register module: {name}")
        sys.modules[name].register_module()


def unregister():
    for name in reversed(registered_modules):
        logger.debug(f"unregister module: {name}")
        sys.modules[name].unregister_module()


if __name__ == "__main__":
    register()