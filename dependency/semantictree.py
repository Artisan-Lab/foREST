from anytree import NodeMixin, RenderTree
import os
from module.string_march import StringMatch
from utils.utils import Tool
from open_api_parse.parser import Parser
from entity.resource_pool import foREST_POST_resource_pool
import nltk

sno = nltk.stem.SnowballStemmer('english')


class SemanticNode(NodeMixin):

    def __init__(self, name, parent=None, children=None):
        super(SemanticNode, self).__init__()
        self.name = name
        self.resource = []
        self.method_dic = {}
        self.parent = parent
        if children:
            self.children = children


class CreateSemanticTree:

    def __init__(self, api_list):
        self.api_list = api_list
        self.root = SemanticNode('root')

    @property
    def create_tree(self):
        for api_info in self.api_list:
            self.find_node(api_info.path.split('/'), api_info.http_method, api_info.api_id, self.root)
        for pre, fill, node in RenderTree(self.root):
            treestr = u"%s%s" % (pre, node.name)
            print(treestr.ljust(8), node.method_dic)
        self.add_close_api(self.root)
        return self.root

    def add_close_api(self, node):
        close_api_list = []
        if node.method_dic:
            if node.ancestors:
                for ancestors_node in node.ancestors:
                    close_api_list += self.add_close_node_api(ancestors_node)
            close_api_list += self.add_close_node_api(node)
            if node.parent and node.parent.children:
                for parent_children_node in node.parent.children:
                    close_api_list += self.add_close_node_api(parent_children_node)
            for method in node.method_dic:
                self.api_list[node.method_dic[method]].close_api += close_api_list
        if node.children:
            for children_node in node.children:
                self.add_close_api(children_node)

    @staticmethod
    def add_close_node_api(node):
        close_api = []
        if node.method_dic:
            for method in node.method_dic:
                close_api.append(node.method_dic[method])
        return close_api

    @staticmethod
    def find_node(api_path_nodes, api_method, api_id, parent_node):
        if not api_path_nodes:
            if api_method == 'post' and not StringMatch.is_path_variable(parent_node.name):
                foREST_POST_resource_pool.resource_name_dict[sno.stem(parent_node.name)] = []
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
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Tool.read_config('api_file', 'file_path'))
    api_parser = Parser(path)
    api_list = api_parser.get_api_list()
    tree = CreateSemanticTree(api_list)
    root = tree.create_tree


if __name__ == '__main__':
    main()
