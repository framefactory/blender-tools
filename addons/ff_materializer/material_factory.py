from typing import Optional
from collections import defaultdict
from pathlib import Path
from zipfile import ZipFile
import shutil
import os
import re

import bpy
from bpy import types as bt

from ff_tools.shading.material_builder import PBRMaterialBuilder

from ff_tools.shading.material import create_node_material, assign_material_to_active


_re_type = {
    "color": re.compile(r"[\W_](color|clr|col|diff)[\W_]"),
    "alpha": re.compile(r"[\W_](alpha|alphamasked)[\W_]"),
    "overlay": re.compile(r"[\W_](overlay|over|ovl)[\W_]"),
    "occlusion": re.compile(r"[\W_](ao|occlusion)[\W_]"),
    "displacement": re.compile(r"[\W_](displacement|disp)[\W_]"),
    "displacement16": re.compile(r"[\W_](displacement|disp)16[\W_]"),
    "roughness": re.compile(r"[\W_](roughness|rough)[\W_]"),
    "metalness": re.compile(r"[\W_](metalness|metallic)[\W_]"),
    "gloss": re.compile(r"[\W_](glossiness|gloss)[\W_]"),
    "reflection": re.compile(r"[\W_](reflection|refl)[\W_]"),
    "bump": re.compile(r"[\W_](bump|bmp)[\W_]"),
    "bump16": re.compile(r"[\W_](bump|bmp)16[\W_]"),
    "normal": re.compile(r"[\W_](normals?|norm|nrm|nor)[\W_]")
}

_re_resolution = re.compile(r"[\W_](\d)[kK]")


_resolution_items = {
    "1": ("1", "1k", "1024 x 1024 pixels"),
    "2": ("2", "2k", "2048 x 2048 pixels"),
    "3": ("3", "3k", "3072 x 3072 pixels"),
    "4": ("4", "4k", "4096 x 4096 pixels"),
    "6": ("6", "6k", "6144 x 6144 pixels"),
    "8": ("8", "8k", "8192 x 8192 pixels"),
}


MapFileDict = defaultdict[str, dict[str, str]]
ResolutionEnumItems = list[tuple[str, str, str]]


class MaterialFactory:
    def __init__(self):
        self.base_path = ""
        self.base_name = ""
        self.map_files: Optional[MapFileDict] = None
        self.is_zipped = False


    def create_material(self, resolution: str, maps_path: str):
        if self.map_files is None:
            return
        
        material = create_node_material(self.base_name)
        builder = PBRMaterialBuilder(material.node_tree)
 
        maps = self.map_files[resolution]
        if maps:
            for map_type, image_path in maps.items():
                if map_type in builder.supported_map_types:
                    if self.is_zipped:
                        image_path = self._extract_file(image_path, maps_path)
                    builder.load_image_map(map_type, str(image_path))
            
            assign_material_to_active(material)


    def set_path(self, path: str):
        print(f"[MaterialFactory.set_path] {path}")
        self.base_path = path
        self.map_files = defaultdict(dict)

        base_path = Path(path)
        if base_path.suffix == ".zip":
            self._analyze_zip(base_path)
        elif base_path.is_dir():
            self._analyze_folder(base_path)
        elif base_path.suffix in [".jpg", ".png", ".tif", ".exr"]:
            self._analyze_folder(base_path.parent)


    def get_resolution_enum(self) -> ResolutionEnumItems:
        if self.map_files:
            return [ _resolution_items[key] for key in self.map_files ]
        else:
            return []


    def dump(self):
        print(f"[MaterialFactory] dump, base path: {self.base_path}")
        if self.map_files:
            for res, maps in self.map_files.items():
                print(f"   Resolution: {res}k")
                for map, path in maps.items():
                    print(f"      {map}: {path}")
        else:
            print("   No map files found")


    def _extract_file(self, file_path: str, destination_path: str) -> str:
        assert(self.is_zipped)

        Path(destination_path).mkdir(parents=True, exist_ok=True)

        with ZipFile(self.base_path, 'r') as zip_file:
            dest_path = Path(destination_path).absolute() / Path(file_path).name
            print(f'[MaterialFactory] extract "{file_path}" to "{dest_path}"')

            with zip_file.open(file_path, 'r') as src_file:
                with open(dest_path, 'wb') as dst_file:
                    shutil.copyfileobj(src_file, dst_file)

        return str(dest_path)


    def _analyze_folder(self, folder_path: Path):
        self.is_zipped = False


    def _analyze_zip(self, file_path: Path):
        try:
            with ZipFile(file_path, 'r') as zip_file:
                infos = zip_file.infolist()
            for info in infos:
                self._find_map_type(info.filename)

            self.base_name = file_path.name.split(".")[0]
            self.is_zipped = True
        except:
            print(f"[MaterialFactory] failed to analyze {file_path}")


    def _find_map_type(self, file_name: str):
        """Parses the file name for the type and size of the map
           and adds the information to the given dictionary."""
        
        assert(self.map_files is not None)
        base_name, _ext = os.path.splitext(file_name.lower())
        if _ext in [ ".jpg", ".tif", ".png", ".exr" ]:
            for map_type, pattern in _re_type.items():
                if pattern.search(base_name):
                    result =_re_resolution.search(base_name)
                    if result:
                        res = result.group(1)
                        self.map_files[res][map_type] = file_name

