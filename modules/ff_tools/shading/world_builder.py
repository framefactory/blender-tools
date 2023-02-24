import bpy
import bpy.types as bt

from ..core.node import NodeBuilder


class IBLWorldBuilder(NodeBuilder):
    """Helper class for building a node-based world shader."""

    def __init__(self, tree: bt.NodeTree):
        """Constructs a new builder and initializes the given shader node tree.
           All nodes and links are removed."""
        
        super().__init__(tree)
        self.clear()

        out_node = self.add_node(bt.ShaderNodeOutputWorld, [600, 300])
        bg_node = self.add_node(bt.ShaderNodeBackground, [400, 300])
        #gamma_node = self.add_node(bt.ShaderNodeGamma, [200, 300])
        bc_node = self.add_node(bt.ShaderNodeBrightContrast, [200, 300])
        self.env_node = self.add_node(bt.ShaderNodeTexEnvironment, [-100, 300])
        map_node = self.add_node(bt.ShaderNodeMapping, [-300, 300])
        tc_node = self.add_node(bt.ShaderNodeTexCoord, [-500, 300])
     
        self.add_link(out_node.inputs["Surface"], bg_node.outputs["Background"])
        self.add_link(bg_node.inputs["Color"], bc_node.outputs["Color"])
        self.add_link(bc_node.inputs["Color"], self.env_node.outputs["Color"])
        self.add_link(self.env_node.inputs["Vector"], map_node.outputs["Vector"])
        self.add_link(map_node.inputs["Vector"], tc_node.outputs["Generated"])

    def load_environment_image(self, file_path: str):
        env_image = None

        try:
            env_image = bpy.data.images.load(file_path)
        except:
            print(f"[IBLWorldBuilder] failed to load environment image: '{file_path}'")
        else:
            self.env_node.image = env_image
            print(f"[IBLWorldBuilder] envionment image loaded: {file_path}")