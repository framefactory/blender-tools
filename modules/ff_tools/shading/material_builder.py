import bpy
import bpy.types as bt

from ..core.node import NodeBuilder


class PBRMaterialBuilder(NodeBuilder):
    """Helper class for building node-based PBR materials."""

    def __init__(self, tree: bt.NodeTree):
        """Constructs a new builder and initializes the given shader node tree.
           All nodes are removed and an output node and principled BSDF node are
           added."""
        
        super().__init__(tree)

        self.supported_map_types = [
            "color",
            "alpha",
            "roughness",
            "metallic",
            "normal",
            "displacement",
        ]

        self.clear()

        self.max_x = 0
        self.pos_y = 300

        self.out_node = self.add_node(bt.ShaderNodeOutputMaterial, [300, 300])
        self.bsdf_node = self.add_node(bt.ShaderNodeBsdfPrincipled, [0, 300])
        self.add_link(self.out_node.inputs["Surface"], self.bsdf_node.outputs["BSDF"])

        self.tc_node = self.add_node(bt.ShaderNodeTexCoord, [-900, 300])
        self.mapping_node = self.add_node(bt.ShaderNodeMapping, [-700, 300])
        self.add_link(self.mapping_node.inputs["Vector"], self.tc_node.outputs["UV"])

   
    def load_image_map(self, map_type: str, image_path: str):
        """Loads an image from the given path and adds it as a map of the given
           type and links the corresponding nodes."""
        image = bpy.data.images.load(image_path, check_existing=True)
        self.add_image_map(map_type, image)


    def add_image_map(self, map_type: str, image: bt.Image):
        """Adds an image map of the given type (color, alpha, roughness, metallic,
           normal, displacement) and links the corresponding nodes."""
        
        map_node = self.add_node(bt.ShaderNodeTexImage, [-500, self.pos_y])
        map_node.image = image
        print(image.colorspace_settings.name)

        self.add_link(map_node.inputs["Vector"], self.mapping_node.outputs["Vector"])

        if map_type == "color":
            self.add_link(self.bsdf_node.inputs["Base Color"], map_node.outputs["Color"])

        elif map_type == "alpha":
            self.add_link(self.bsdf_node.inputs["Alpha"], map_node.outputs["Color"])

        elif map_type == "roughness":
            image.colorspace_settings.name = "Non-Color"
            self.add_link(self.bsdf_node.inputs["Roughness"], map_node.outputs["Color"])
        
        elif map_type == "metallic":
            image.colorspace_settings.name = "Non-Color"
            self.add_link(self.bsdf_node.inputs["Metallic"], map_node.outputs["Color"])

        elif map_type == "normal":
            image.colorspace_settings.name = "Non-Color"
            normal_node = self.add_node(bt.ShaderNodeNormalMap, [-200, self.pos_y])
            self.add_link(self.bsdf_node.inputs["Normal"], normal_node.outputs["Normal"])
            self.add_link(normal_node.inputs["Color"], map_node.outputs["Color"])

        elif map_type == "displacement":
            image.colorspace_settings.name = "Non-Color"
            disp_node = self.add_node(bt.ShaderNodeDisplacement, [-200, self.pos_y])
            self.add_link(self.out_node.inputs["Displacement"], disp_node.outputs["Displacement"])
            self.add_link(disp_node.inputs["Height"], map_node.outputs["Color"])

        else:
            raise RuntimeError(f"unsupported map type: {map_type}")

        self.pos_y -= 280

        return self
