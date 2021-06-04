from node import Node
from constants import *
from anytree import RenderTree
import json
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


json_str = '''
[
  {
    "id": "ed899a2f4b50b4370feeea94676502b42383c746",
    "short_id": "ed899a2f4b5",
    "title": "Replace sanitize with escape once",
    "author_name": "Example User",
    "author_email": "user@example.com",
    "authored_date": "2012-09-20T11:50:22+03:00",
    "committer_name": "Administrator",
    "committer_email": "admin@example.com",
    "committed_date": "2012-09-20T11:50:22+03:00",
    "created_at": "2012-09-20T11:50:22+03:00",
    "message": "Replace sanitize with escape once",
    "parent_ids": [
      "6104942438c14ec7bd21c6cd5bd995272b3faff6"
    ],
    "web_url": "https://gitlab.example.com/thedude/gitlab-foss/-/commit/ed899a2f4b50b4370feeea94676502b42383c746"
  },
  {
    "id": "6104942438c14ec7bd21c6cd5bd995272b3faff6",
    "short_id": "6104942438c",
    "title": "Sanitize for network graph",
    "author_name": "randx",
    "author_email": "user@example.com",
    "committer_name": "ExampleName",
    "committer_email": "user@example.com",
    "created_at": "2012-09-20T09:06:12+03:00",
    "message": "Sanitize for network graph",
    "parent_ids": [
      "ae1d9fb46aa2b07ee9836d49862ec4e2c46fbbba"
    ],
    "web_url": "https://gitlab.example.com/thedude/gitlab-foss/-/commit/ed899a2f4b50b4370feeea94676502b42383c746"
  }
]
    '''
tree = Tree(json_str)
tree.print()
print(tree.dump())
