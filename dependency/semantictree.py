from anytree import NodeMixin, RenderTree
import os

from tool.tools import Tool
from open_api_parse.parser import Parser



class SemanticNode(NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(SemanticNode, self).__init__()
        self.name = name
        self.method_dic = {}
        self.parent = parent
        if children:
            self.children = children

class CreateSemanticTree:

    def __init__(self, api_list):
        self.api_list = api_list
        self.root = SemanticNode('root')

    def create_tree(self):
        for api_info in self.api_list:
            self.find_node(api_info.path.split('/'), api_info.http_method, api_info.api_id, self.root)
        for pre, fill, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.method_dic)
        return self.root

    @staticmethod
    def find_node(api_path_nodes, api_method, api_id, parent_node):
        if not api_path_nodes:
            parent_node.method_dic[api_method] = api_id
            return
        flag = 0
        if parent_node.children:
            for child in parent_node.children:
                if child.name == api_path_nodes[0]:
                    flag = 1
                    child_node = child
                    break
        if flag == 0:
            child_node = SemanticNode(api_path_nodes[0], parent=parent_node)
        CreateSemanticTree.find_node(api_path_nodes[1:], api_method, api_id, child_node)


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Tool.readconfig('api_file', 'file_path'))
    api_parser = Parser(path)
    api_list = api_parser.get_api_list()
    tree = CreateSemanticTree(api_list)
    tree.create_tree()
    root = tree.root


if __name__ == '__main__':
    main()
