import json

from anytree import PreOrderIter
from anytree import RenderTree
from anytree.exporter import DotExporter

from constants import *
from node import Node
from utils import *


class Tree:
    def __init__(self, data: str):
        self.root = Node(None, None, None)
        self.data = json.loads(data)
        self.create(None, self.data, self.root)
        self.dump_data = {} if Utils.json_type(data) == constants.OBJECT else []

    def create(self, key, data, parent):

        # complex type(object or array)
        if Utils.is_complex_type(data):
            json_type = Utils.json_type(data)
            node = Node(key, None, json_type, parent=parent)
            # array
            if json_type == ARRAY:
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
        num = 0
        for _ in PreOrderIter(self.root):
            num = num + 1
        return num

    def dump(self) -> str:
        if len(self.root.children) <= 0:
            print("dump error: the tree is empty!")
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
        for pre, fill, node in RenderTree(self.root):
            tree_str = u"%s%s" % (pre, node.key)
            print(tree_str.ljust(8), node.value, node.type)

    def export_img(self, img_name):
        DotExporter(self.root).to_picture(img_name)

    def copy(self):
        return Tree(self.dump())
