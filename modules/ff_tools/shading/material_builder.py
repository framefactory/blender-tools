import bpy.types as bt

from ..core import NodeBuilder


class PBRMaterialBuilder(NodeBuilder):
    """Helper class for building node-based PBR materials."""

    def __init__(self, tree: bt.NodeTree):
        super().__init__(tree)
        self.clear()
        
        out_node = self.add_node(bt.ShaderNodeOutputMaterial, [300, 300])
        self.bsdf_node = self.add_node(bt.ShaderNodeBsdfPrincipled, [30, 300])
        self.add_link(out_node.inputs["Surface"], self.bsdf_node.outputs["BSDF"])

        tc_node = self.add_node(bt.ShaderNodeTexCoord, [-700, 300])
        self.mapping_node = self.add_node(bt.ShaderNodeMapping, [-540, 300])
        self.add_link(self.mapping_node.inputs["Vector"], tc_node.outputs["UV"])
    
    def add_image_map(self, type: str, image: bt.Image):
        map_node = self.add_node(bt.ShaderNodeTexImage, [-400, 300])
        
        self.add_link(map_node.inputs["Vector"], self.mapping_node.outputs["Vector"])
        self.add_link(self.bsdf_node.inputs["Base Color"], map_node.outputs["Color"])
