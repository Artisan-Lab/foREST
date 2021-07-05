import json
import random

from anytree import PreOrderIter
from anytree import RenderTree
from anytree.exporter import DotExporter

from commons import constants
from commons.utils import Utils
from node import Node


class Tree:
    """
    tree implementation
    """

    def __init__(self, data: str):
        self.root = Node(None, None, None)
        self.data = json.loads(data)
        self.create(None, self.data, self.root)
        self.dump_data = {} if Utils.json_type(data) == constants.OBJECT else []

    def create(self, key, data, parent):
        """
        create a tree by a recursive way
        """
        # complex type(object or array)
        if Utils.is_complex_type(data):
            json_type = Utils.json_type(data)
            node = Node(key, None, json_type, parent=parent)
            # array
            if json_type == constants.ARRAY:
                for item in data:
                    self.create(None, item, node)
            # object
            else:
                for k, v in data.items():
                    self.create(k, v, node)
        # primitive type
        else:
            Node(key, data, Utils.json_type(data), parent=parent)

    def get_node_num(self):
        """
        get number of nodes
        """
        num = 0
        for _ in PreOrderIter(self.root):
            num += 1
        return num

    def dump(self) -> str:
        """
        convert a tree to formatted json str
        """
        if len(self.root.children) <= 0:
            return random.choice(['[]', '{}'])
        return json.dumps(self._dump(self.root.children[0]))

    def _dump(self, node):
        if Utils.in_primitive_type(node.type):
            return node.value

        if node.type == constants.OBJECT:
            ret = {}
            for child in node.children:
                ret[child.key] = self._dump(child)
            return ret

        if node.type == constants.ARRAY:
            ret = []
            for child in node.children:
                ret.append(self._dump(child))
            return ret

    def print(self):
        """
        pretty print for debug
        """
        for pre, fill, node in RenderTree(self.root):
            tree_str = u"%s%s" % (pre, node.key)
            print(tree_str.ljust(8), node.value, node.type)

    def export_img(self, img_name):
        """
        export current tree structure to an image
        """
        DotExporter(self.root).to_picture(img_name)

    def copy(self):
        """
        duplicate a new tree from current tree
        """
        return Tree(self.dump())

    def get_node_ids(self):
        """
        return ids of all nodes
        """
        node_ids = []
        for _ in PreOrderIter(self.root):  # type:Node
            node_ids.append(_.id)
        return node_ids

    def get_leaf_node_ids(self):
        """
        return ids of leaf nodes
        """
        node_ids = []
        for _ in PreOrderIter(self.root):  # type:Node
            if _.is_leaf:
                node_ids.append(_.id)
        return node_ids
