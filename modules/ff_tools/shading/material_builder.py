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
            "occlusion",
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
        self.mapping_node.vector_type = 'TEXTURE'
        self.add_link(self.mapping_node.inputs["Vector"], self.tc_node.outputs["UV"])

   
    def load_image_map(self, map_type: str, image_path: str):
        """Loads an image from the given path and adds it as a map of the given
           type and links the corresponding nodes."""
        print(f'[PBRMaterialBuilder.load_image_map] load "{map_type}" from "{image_path}"')
        image = bpy.data.images.load(image_path, check_existing=True)
        self.add_image_map(map_type, image)


    def add_image_map(self, map_type: str, image: bt.Image|None = None):
        """Adds an image map of the given type (color, alpha, occlusion,
           roughness, metallic, normal, displacement) and links the
           corresponding nodes."""
        
        map_node = self.add_node(bt.ShaderNodeTexImage, [-500, self.pos_y])
        if image is not None:
            map_node.image = image

        self.add_link(map_node.inputs["Vector"], self.mapping_node.outputs["Vector"])

        if map_type == "color":
            map_node.label = "Base Color"
            bc_node = self.add_node(bt.ShaderNodeBrightContrast, [-200, self.pos_y], label="Adjust Color")

            occ_node = self.find_node_by_label("Occlusion")
            if occ_node:
                mix_node = self.add_node(bt.ShaderNodeMixRGB, [-200, occ_node.location[1]])
                mix_node.blend_type = "MULTIPLY"
                mix_node.inputs["Fac"].default_value = 1.0 #type:ignore
                self.add_link(mix_node.inputs["Color1"], bc_node.outputs["Color"])
                self.add_link(mix_node.inputs["Color2"], occ_node.outputs["Color"])
                self.add_link(self.bsdf_node.inputs["Base Color"], mix_node.outputs["Color"])
            else:
                self.add_link(self.bsdf_node.inputs["Base Color"], bc_node.outputs["Color"])
                self.add_link(bc_node.inputs["Color"], map_node.outputs["Color"])

        elif map_type == "alpha":
            map_node.label = "Alpha"
            self.add_link(self.bsdf_node.inputs["Alpha"], map_node.outputs["Color"])

        elif map_type == "occlusion":
            map_node.label = "Occlusion"
            if image is not None:
                image.colorspace_settings.name = "Non-Color"

            bc_node = self.find_node_by_label("Adjust Color")
            if bc_node:
                mix_node = self.add_node(bt.ShaderNodeMixRGB, [-200, self.pos_y])
                mix_node.blend_type = "MULTIPLY"
                mix_node.inputs["Fac"].default_value = 1.0 #type:ignore
                self.add_link(mix_node.inputs["Color1"], bc_node.outputs["Color"])
                self.add_link(mix_node.inputs["Color2"], map_node.outputs["Color"])
                self.add_link(self.bsdf_node.inputs["Base Color"], mix_node.outputs["Color"])
            else:
                self.add_link(self.bsdf_node.inputs["Base Color"], map_node.outputs["Color"])


        elif map_type == "roughness":
            map_node.label = "Roughness"
            if image is not None:
                image.colorspace_settings.name = "Non-Color"
            math_node = self.add_node(bt.ShaderNodeMath, [-200, self.pos_y])
            math_node.operation = 'MULTIPLY_ADD'
            math_node.inputs[1].default_value = 1.0 #type:ignore multiplier
            math_node.inputs[2].default_value = 0.0 #type:ignore addend
            self.add_link(self.bsdf_node.inputs["Roughness"], math_node.outputs["Value"])
            self.add_link(math_node.inputs[0], map_node.outputs["Color"])
        
        elif map_type == "metallic":
            map_node.label = "Metalness"
            if image is not None:
                image.colorspace_settings.name = "Non-Color"
            self.add_link(self.bsdf_node.inputs["Metallic"], map_node.outputs["Color"])

        elif map_type == "normal":
            map_node.label = "Normal"
            if image is not None:
                image.colorspace_settings.name = "Non-Color"
            normal_node = self.add_node(bt.ShaderNodeNormalMap, [-200, self.pos_y])
            self.add_link(self.bsdf_node.inputs["Normal"], normal_node.outputs["Normal"])
            self.add_link(normal_node.inputs["Color"], map_node.outputs["Color"])

        elif map_type == "displacement":
            map_node.label = "Displacement"
            map_node.interpolation = "Cubic"
            if image is not None:
                image.colorspace_settings.name = "Non-Color"
            disp_node = self.add_node(bt.ShaderNodeDisplacement, [-200, self.pos_y])
            self.add_link(self.out_node.inputs["Displacement"], disp_node.outputs["Displacement"])
            self.add_link(disp_node.inputs["Height"], map_node.outputs["Color"])

        else:
            raise RuntimeError(f"unsupported map type: {map_type}")

        self.pos_y -= 280

        return self
