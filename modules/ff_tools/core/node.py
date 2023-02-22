from typing import Optional, TypeVar, cast

from bpy import types as bt


#Nodes = Union[dict[str, bt.Node], list[bt.Node], bt.bpy_prop_collection, bt.Nodes]


def find_node_by_type(nodes: bt.Nodes, type: type[bt.Node]) -> Optional[bt.Node]:
    """Returns the first node in the given list which is an instance
       of the given node type, or None if none found."""
    for node in nodes:
        if isinstance(node, type):
            return node

    return None


def create_node(nodes: bt.Nodes, type: type[bt.ShaderNode], location: list[int]):
    """Creates a node of the given type at the given location and
       adds it to the given list of nodes."""
    node = nodes.new(type.__name__)
    node.location = location
    return node

T = TypeVar("T", bound=bt.Node)

class NodeBuilder:
    """Helper class for adding, grouping, and linking nodes to the
       given node tree."""
    def __init__(self, tree: bt.NodeTree):
        self.tree = tree

    def clear(self):
        self.tree.nodes.clear()
        self.tree.links.clear()

    def add_node(self, type: type[T], location: list[int]) -> T:
        nodes = self.tree.nodes
        node = cast(T, nodes.new(type.__name__))
        node.location = location
        return node

    def add_link(self, in_socket: bt.NodeSocket, out_socket: bt.NodeSocket) -> bt.NodeLink:
        links = self.tree.links
        return links.new(in_socket, out_socket)
