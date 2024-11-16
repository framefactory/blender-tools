from typing import Optional, TypeVar, cast

from bpy import types as bt


#Nodes = Union[dict[str, bt.Node], list[bt.Node], bt.bpy_prop_collection, bt.Nodes]
T = TypeVar("T", bound=bt.Node)


def find_node_by_type(nodes: bt.Nodes, type: type[bt.Node]) -> Optional[bt.Node]:
    """Returns the first node in the given list which is an instance
       of the given node type, or None if none found."""
    for node in nodes:
        if isinstance(node, type):
            return node

    return None


def find_node_by_name(nodes: bt.Nodes, name: str) -> Optional[bt.Node]:
    """Returns the first node in the given list which has the given
       name, or None if none found."""
    for node in nodes:
        if node.name == name:
            return node

    return None


def find_node_by_label(nodes: bt.Nodes, label: str) -> Optional[bt.Node]:
    """Returns the first node in the given list which has the given
       label, or None if none found."""
    for node in nodes:
        if node.label == label:
            return node

    return None


def create_node(nodes: bt.Nodes, type: type[T], location: list[int], *, label: str="", name: str="") -> T:
    """Creates a node of the given type at the given location and
       adds it to the given list of nodes."""
    node = cast(T, nodes.new(type.__name__))
    node.location = location

    if label:
        node.label = label
    if name:
        node.name = name

    return node


class NodeBuilder:
    """Helper class for adding, grouping, and linking nodes to the
       given node tree."""
    def __init__(self, tree: bt.NodeTree):
        self.tree = tree

    def clear(self):
        self.tree.nodes.clear()
        self.tree.links.clear()

    def find_node_by_type(self, type: type[bt.Node]) -> Optional[bt.Node]:
        return find_node_by_type(self.tree.nodes, type)
    
    def find_node_by_name(self, name: str) -> Optional[bt.Node]:
        return find_node_by_name(self.tree.nodes, name)
    
    def find_node_by_label(self, label: str) -> Optional[bt.Node]:
        return find_node_by_label(self.tree.nodes, label)

    def add_node(self, type: type[T], location: list[int], *, label: str="", name: str="") -> T:
        return create_node(self.tree.nodes, type, location, label=label, name=name)
    
    def get_or_add_node(self, type: type[T], location: list[int]) -> T:
        node = find_node_by_type(self.tree.nodes, type)
        if node is None:
            node = self.add_node(type, location)
        
        return node

    def add_link(self, in_socket: bt.NodeSocket, out_socket: bt.NodeSocket) -> bt.NodeLink:
        links = self.tree.links
        return links.new(in_socket, out_socket)
