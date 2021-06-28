import random

from tree import *


class Mutation:
    """
    mutation strategies
    """

    def __init__(self):
        pass

    @staticmethod
    def node_manipulated_using_random(tree: Tree) -> Node:
        """
        select the node by random strategy
        """
        index = random.randrange(2, tree.get_node_num() + 1)
        for node in PreOrderIter(tree.root):
            index -= 1
            if index == 0:
                return node

    @staticmethod
    def two_nodes_manipulated_using_random(tree: Tree) -> list:
        """
        select two nodes by random strategy,[copied_tree_node,source_tree_node]
        """
        two_nums = random.sample(range(2, tree.get_node_num() + 1), 2)
        tree_copied = tree.copy()
        tree_copied.export_img("output/tree_copied.png")
        ret = []
        index = two_nums[0]
        for node in PreOrderIter(tree_copied.root):
            index -= 1
            if index == 0:
                ret.append(node)
        index = two_nums[1]
        for node in PreOrderIter(tree.root):
            index -= 1
            if index == 0:
                ret.append(node)
        return ret

    @staticmethod
    def drop(tree: Tree):
        """
            removes one child node c of node n,
            and Other child nodes remain unchanged.
        """
        node = Mutation.node_manipulated_using_random(tree)
        print(f'#{node.id} node will be dropped!')
        node.parent = None

    @staticmethod
    def select(tree: Tree):
        """
           keeps only one child node c of node n,
           where (n, c) ∈ E. All other child nodes of n are removed.
        """
        node = Mutation.node_manipulated_using_random(tree)
        print(f'#{node.id} node will be selected, and other siblings will be dropped!')
        for _ in node.siblings:
            _.parent = None

    @staticmethod
    def duplicate(tree: Tree):
        """
           adds a new child node r to n by copying an existing child c of n. The descendant nodes of
           c (i.e., the subtrees) are also copied
        """
        two_nodes = Mutation.two_nodes_manipulated_using_random(tree)
        print(f'#{two_nodes[0].id} will be copied to {two_nodes[1].id}')
        two_nodes[0].parent = two_nodes[1]

    @staticmethod
    def type(tree: Tree):
        """
            changes the labeled type of a node
            e.g. primitive type <-> array/object type
            e.g. boolean <-> string
            e.g. number <-> string
        """

        pass

    def single(self):
        pass

    def path(self):
        pass

    def all(self):
        pass
