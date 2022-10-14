import importlib
import sys


package = "ff_materializer"

bl_info = {
    "name": "FF Materializer",
    "descriptor": "PBR Material import helper",
    "author": "Ralph Wiedemeier",
    "category": "Material",
    "version": (1, 0, 0),
    "blender": (3, 3, 0)
}

registered_modules = [
    "ff_materializer.operators",
    "ff_materializer.world_panel",
    "ff_materializer.material_panel",
]

all_modules = registered_modules + [
    "ff_tools.node_tools",
    "ff_materializer.material_factory",
    "ff_materializer.world_factory",
]


def register():
    # ensure all modules are up to date
    for name in all_modules:
        importlib.import_module(name)
        module = sys.modules[name]
        importlib.reload(module)
        print("[ff_materializer] reload", name)

    # call per-module registration
    for name in registered_modules:
        sys.modules[name].register_module()
        print("[ff_materializer] register", name)


def unregister():
    for name in reversed(registered_modules):
        sys.modules[name].unregister_module()
        print("[ff_materializer] unregister", name)


if __name__ == "__main__":
    register()
