from typing import Optional
from dataclasses import dataclass
from zipfile import ZipFile
import os
import re

import bpy
from bpy import types as bt

from ff_tools.core.node_tools import find_node_by_type


_re_type = {
    "color": re.compile(r"[\W_](color|clr|col)[\W_]"),
    "alpha": re.compile(r"[\W_](alpha|alphamasked)[\W_]"),
    "overlay": re.compile(r"[\W_](overlay|over|ovl)[\W_]"),
    "occlusion": re.compile(r"[\W_](ao|occlusion)[\W_]"),
    "displacement": re.compile(r"[\W_](displacement|disp)[\W_]"),
    "displacement16": re.compile(r"[\W_](displacement|disp)16[\W_]"),
    "roughness": re.compile(r"[\W_](roughness|rough)[\W_]"),
    "metalness": re.compile(r"[\W_](metalness|metal)[\W_]"),
    "gloss": re.compile(r"[\W_](glossiness|gloss)[\W_]"),
    "reflection": re.compile(r"[\W_](reflection|refl)[\W_]"),
    "bump": re.compile(r"[\W_](bump|bmp)[\W_]"),
    "bump16": re.compile(r"[\W_](bump|bmp)16[\W_]"),
    "normal": re.compile(r"[\W_](normals?|norm|nrm)[\W_]")
}

_re_resolution = re.compile(r"[\W_](\d)[kK][\W_]")


_resolution_items = {
    "1": ("1", "1k", "1024 x 1024 pixels"),
    "2": ("2", "2k", "2048 x 2048 pixels"),
    "3": ("3", "3k", "3072 x 3072 pixels"),
    "4": ("4", "4k", "4096 x 4096 pixels"),
    "6": ("6", "6k", "6144 x 6144 pixels"),
    "8": ("8", "8k", "8192 x 8192 pixels"),
}


MapFileDict = dict[str, dict[str, str]]
EnumItems = list[tuple[str, str, str]]


class MaterialFactory:
    def __init__(self):
        self._base_name = ""
        self._map_files: Optional[MapFileDict] = None

    def load_textures(self, file_path: str):
        base_name, _ = os.path.splitext(os.path.basename(file_path))
        #self.create_material(base_name)
        pass


    def create_material(self, name: str, context: bt.Context):
        material = bpy.data.materials.new(name)
        material.use_nodes = True

        nodes = material.node_tree.nodes
        links = material.node_tree.links

        bsdf_node = find_node_by_type(nodes, bt.ShaderNodeBsdfPrincipled)
        if bsdf_node is None:
            raise RuntimeError("material is missing Principled BSDF node")


    def analyze_file_path(self, file_path: str) -> EnumItems:
        _, ext = os.path.splitext(file_path.lower())

        if ext == ".zip":
            self._analyze_zip(file_path)
        if ext in [".jpg", ".png", ".tif", ".exr"]:
            pass

        if self._map_files:
            return [ _resolution_items[key] for key in self._map_files ]

        return []
        

    def _analyze_zip(self, file_path: str):
        try:
            with ZipFile(file_path, 'r') as zip_file:
                infos = zip_file.infolist()
            map_files = self._map_files = {}
            for info in infos:
                self._find_map_type(info.filename, map_files)

            self._base_name, _ = os.path.splitext(file_path)
        except:
            print(f"[MaterialFactory] failed to analyze {file_path}")


    @staticmethod
    def _find_map_type(file_name: str, map_dict: MapFileDict):
        base_name, ext = os.path.splitext(file_name.lower())
        for map_type, pattern in _re_type.items():
            if pattern.search(base_name):
                result =_re_resolution.search(base_name)
                if result:
                    res = result.group(1)
                    if res not in map_dict:
                        map_dict[res] = {}
                    map_dict[res][map_type] = file_name

