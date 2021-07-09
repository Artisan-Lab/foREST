#!/usr/bin/env python
import os

import numpy as np
from treelib import Tree

from parse import parse


class Method:

    def __init__(self, method, path):
        self.method = method
        self.path = path

    def __setitem__(self, key, value):
        self.method[key] = value


class CreateTree:

    def __init__(self, api_list):
        self.api_list = api_list
        self.path_tree = Tree()
        self.node_id = 1

    def create_tree(self):
        for api_info in self.api_list:
            api_path_nodes = api_info.path.split('/')[0:]
            api_method = api_info.http_method
            api_id = api_info.api_id
            self.find_node(api_path_nodes, api_method, api_id)
        self.path_tree.show(idhidden=False, data_property='method')

    def find_node(self, api_path_nodes, api_method, api_id):
        current_node = self.path_tree.get_node('/'.join(api_path_nodes))
        if not current_node:
            current_node = self.path_tree.root
            for i in range(len(api_path_nodes)):
                new_node_id = '/'.join(api_path_nodes[:i + 1])
                if not self.path_tree.contains(new_node_id):
                    self.path_tree.create_node(identifier=new_node_id, parent=current_node,
                                               data=Method({}, api_path_nodes[i]))
                current_node = self.path_tree.get_node(new_node_id)
        data = current_node.data
        data.method[api_method] = api_id
        self.path_tree.update_node(current_node.identifier, data=data)

    def find_dependency(self):
        node_number = len(self.api_list)
        matrix_zero = np.zeros([node_number + 1, node_number + 1], dtype=int)
        matrix_one = np.ones([node_number + 1, node_number + 1], dtype=int)
        matrix = matrix_zero - matrix_one
        all_nodes = self.path_tree.all_nodes()
        for node in all_nodes:
            post_id = self.find_last_post(node)
            if post_id:
                if 'post' in node.data.method:
                    if self.path_tree.parent(node.identifier):
                        last_post = self.find_last_post(self.path_tree.parent(node.identifier))
                        if last_post:
                            matrix[node.data.method['post']][last_post] = 1
                if 'get' in node.data.method:
                    matrix[node.data.method['get']][post_id] = 1
                if 'delete' in node.data.method:
                    matrix[node.data.method['delete']][post_id] = 1
                if 'put' in node.data.method:
                    matrix[node.data.method['put']][post_id] = 1
        return matrix

    def find_last_post(self, node):
        if 'post' in node.data.method:
            return node.data.method['post']
        elif self.path_tree.parent(node.identifier):
            return self.find_last_post(self.path_tree.parent(node.identifier))
        else:
            return None


# class Node:
#
#     def __init__(self, name, parent=None, children=None):
#         self.children = []
#         self.name = name
#         self.method_and_id = {}
#         self.parent = parent
#         self.children_list = []
#         if children:
#             self.children.append(children)
#             self.children_list.append(children.name)
#
#     def add_info(self, method, api_id):
#         self.method_and_id[method] = api_id
#
#     def add_child(self,child):
#         self.children.append(child)
#         self.children_list.append(child.name)
#
#
# class PathTree:
#
#     def __init__(self, api_list):
#         self.root = Node(None, None, None)
#         self.current_node = self.root
#         self.api_list = api_list
#
#     @staticmethod
#     def creat_node(self,api_path_nodes, parent_node):
#         node = Node(api_path_nodes, parent=parent_node)
#         parent_node.add_child(node)
#
#     def find_node(self, api_path_nodes, api_id, api_method):
#         if api_path_nodes[0] not in self.current_node.children_list:
#             self.creat_node(self, api_path_nodes[0], self.current_node)
#         for child in self.current_node.children:
#             if child.name == api_path_nodes[0]:
#                 if len(api_path_nodes) == 1:
#                     child.add_info(api_method, api_id)
#                 else:
#                     self.current_node = child
#                     self.find_node(api_path_nodes[1:], api_id, api_method)
#
#     def creat_tree(self):
#         for api in self.api_list:
#             self.current_node = self.root
#             api_path_nodes = api.path.split('/')[3:]
#             api_method = api.http_method
#             api_id = api.api_id
#             self.find_node(api_path_nodes, api_id, api_method)
#         self.postorder_traversal(self.root, 0)
#         return self.root
#
#     def postorder_traversal(self, node, depth):
#         print('-' * depth + str(node.name) + str(node.method_and_id))
#         if node.children:
#             for child in node.children:
#                 self.postorder_traversal(child,depth+1)
#
#
# class FindDependency:
#
#     def __init__(self, root, matrix):
#         self.root = root
#         self.matrix = matrix
#
#     def postorder_traversal(self, node):
#         if node.children:
#             for child in node.children:
#                 self.postorder_traversal(child)
#         self.find_dependency(node)
#
#     def find_dependency(self, node):
#         if 'get' in node.method_and_id:
#             if self.find_last_post(node):
#                 self.matrix[node.method_and_id['get'], self.find_last_post(node)] = 1
#         if 'post' in node.method_and_id:
#             pass
#         if 'delete' in node.method_and_id:
#             pass
#         if 'put' in node.method_and_id:
#             pass
#
#     def find_full_path(self, node, full_path):
#         if node.parent:
#             full_path = self.find_full_path(node.parent, node.name + full_path)
#         return full_path
#
#     def find_last_post(self, node):
#         last_post_id = None
#         if 'post' in node.method_and_id:
#             return node.method_and_id['post']
#         if node.parent:
#             last_post_id = self.find_last_post(node.parent)
#         return last_post_id
#
#     def exec(self):
#         self.postorder_traversal(self.root)
#
#
# def main():
#     path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/openapi.yaml")
#     api_list = parse.get_api_info(1, path)
#     num = len(api_list)
#     matrix = np.zeros([num,num],dtype=int)
#     jsonTree = PathTree(api_list)
#     path_tree = jsonTree.creat_tree()
#     dependence = FindDependency(path_tree, matrix)
#     dependence.exec()
#     print()
#
#


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/elastic.yaml")
    api_list = parse.get_api_info(1, path)
    tree = CreateTree(api_list)
    tree.create_tree()
    matrix = tree.find_dependency()
    print(matrix)


if __name__ == '__main__':
    main()
