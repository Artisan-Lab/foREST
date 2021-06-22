import random

from tree import *


class Mutation:
    def __init__(self):
        pass

    """
    select the node by random strategy
    """

    @staticmethod
    def node_manipulated_using_random(tree: Tree) -> Node:
        index = random.randrange(2, tree.get_node_num() + 1)
        for node in PreOrderIter(tree.root):
            index = index - 1
            if index == 0:
                return node

    """
    select two nodes by random strategy,[copied_tree_node,source_tree_node]
    """

    @staticmethod
    def two_nodes_manipulated_using_random(tree: Tree) -> list:
        two_nums = random.sample(range(2, tree.get_node_num() + 1), 2)
        tree_copied = tree.copy()
        tree_copied.export_img("tree_copied.png")
        ret = []
        index = two_nums[0]
        for node in PreOrderIter(tree_copied.root):
            index = index - 1
            if index == 0:
                ret.append(node)
        index = two_nums[1]
        for node in PreOrderIter(tree.root):
            index = index - 1
            if index == 0:
                ret.append(node)
        return ret

    """
    removes one child node c of node n,
    and Other child nodes remain unchanged.
    """

    @staticmethod
    def drop(tree: Tree):
        node = Mutation.node_manipulated_using_random(tree)
        print(f'#{node.id} node will be dropped!')
        node.parent = None

    """
    keeps only one child node c of node n, 
    where (n, c) ∈ E. All other child nodes of n are removed.
    """

    @staticmethod
    def select(tree: Tree):
        node = Mutation.node_manipulated_using_random(tree)
        print(f'#{node.id} node will be selected, and other siblings will be dropped!')
        for _ in node.siblings:
            _.parent = None

    """
    adds a new child node r to n by copying an existing child c of n. The descendant nodes of
    c (i.e., the subtrees) are also copied
    """

    @staticmethod
    def duplicate(tree: Tree):
        two_nodes = Mutation.two_nodes_manipulated_using_random(tree)
        print(f'#{two_nodes[0].id} will be copied to {two_nodes[1].id}')
        two_nodes[0].parent = two_nodes[1]

    """
    changes the labeled type of a node 
    e.g. primitive type <-> array/object type
    e.g. boolean <-> string
    e.g. number <-> string
    """

    @staticmethod
    def type(tree: Tree):

        pass

    def single(self):
        pass

    def path(self):
        pass

    def all(self):
        pass
