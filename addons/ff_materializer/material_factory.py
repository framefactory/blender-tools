from dataclasses import dataclass
from enum import Enum
from zipfile import ZipFile
import os

import bpy
from bpy import types as bt

from ff_tools.node_tools import find_node_by_type


@dataclass
class MapFiles:
    color: str = ""
    normals: str = ""
    roughness: str = ""
    displacement: str = ""


class MaterialFactory:
    def __init__(self, context: bt.Context):
        self.context = context

    @staticmethod
    def can_import(file_path: str):
        base_name, ext = os.path.splitext(file_path)
        return ext.lower() == ".zip"

    def load_textures(self, file_path: str):
        base_name, _ = os.path.splitext(os.path.basename(file_path))
        files = MapFiles()
        self.create_material(base_name, files)
        pass

    def create_material(self, name: str, files: MapFiles):
        material = bpy.data.materials.new(name)
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        bsdf_node = find_node_by_type(nodes, bt.ShaderNodeBsdfPrincipled)
        if bsdf_node is None:
            raise RuntimeError("material is missing Principled BSDF node")

    def open_zip(self, file_path: str):
        with ZipFile(file_path, 'r') as zip_file:
            infos = zip_file.infolist()
            for info in infos:
                print(info.filename)
