from typing import cast, Optional

import bpy
from bpy import types as bt

from ff_tools.core.node import find_node_by_type


class WorldFactory:
    def __init__(self, context: bt.Context):
        self.context = context

    @staticmethod
    def has_active_world(context: bt.Context) -> bool:
        if context.scene is None:
            return False
        if context.scene.world is None:
            return False

        return True

    def get_environment_texture_node(self):
        world = self.context.scene.world
        nodes = world.node_tree.nodes
        env_node = find_node_by_type(nodes, bt.ShaderNodeTexEnvironment)
        return cast(Optional[bt.ShaderNodeTexEnvironment], env_node)

    def load_environment_image(self, file_path: str):
        env_node = self.get_environment_texture_node()
        if env_node is None:
            raise RuntimeError("no environment texture node found in world node tree")

        env_image = None

        try:
            env_image = bpy.data.images.load(file_path)
        except:
            print(f"[WorldFactory] failed to load environment image: '{file_path}'")
        else:
            env_node.image = env_image
            print(f"[World Factory] envionment image loaded: {file_path}")

    def create_world(self):
        world = self.context.scene.world
        world.use_nodes = True
        nodes = world.node_tree.nodes
        links = world.node_tree.links

        # clear world node tree
        nodes.clear()
        
        # create nodes
        out_node = nodes.new("ShaderNodeOutputWorld")
        out_node.location = [600, 300]

        bg_node = nodes.new("ShaderNodeBackground")
        bg_node.location = [400, 300]

        gamma_node = nodes.new("ShaderNodeGamma")
        gamma_node.location = [200, 300]

        env_node = nodes.new("ShaderNodeTexEnvironment")
        env_node.location = [-100, 300]

        map_node = nodes.new("ShaderNodeMapping")
        map_node.location = [-300, 300]
        
        tc_node = nodes.new("ShaderNodeTexCoord")
        tc_node.location = [-500, 300]

        # link nodes
        links.new(out_node.inputs["Surface"], bg_node.outputs["Background"])
        links.new(bg_node.inputs["Color"], gamma_node.outputs["Color"])
        links.new(gamma_node.inputs["Color"], env_node.outputs["Color"])
        links.new(env_node.inputs["Vector"], map_node.outputs["Vector"])
        links.new(map_node.inputs["Vector"], tc_node.outputs["Generated"])
    