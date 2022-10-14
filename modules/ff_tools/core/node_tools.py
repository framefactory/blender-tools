from typing import Dict, List, Union, Optional

from bpy import types as bt


Nodes = Union[Dict[str, bt.Node], List[bt.Node], bt.bpy_prop_collection, bt.Nodes]


def find_node_by_type(nodes: Nodes, type: type[bt.Node]) -> Optional[bt.Node]:
    for node in nodes:
        if isinstance(node, type):
            return node

    return None
