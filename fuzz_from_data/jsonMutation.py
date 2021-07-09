import string

import commons.mutateConstants
from tree import *


class JsonMutation:
    """
    mutation strategies
    """

    def __init__(self):
        pass

    @staticmethod
    def random_select_one_node(tree: Tree) -> Node:
        """
        select the node by random strategy
        note,we cannot select the tree root node
        """
        # index = random.randrange(2, tree.get_node_num() + 1)
        ids = tree.get_node_ids()
        # delete root id
        ids.remove(tree.root.id)
        if len(ids) <= 0:
            print("There is no child in the tree.")
            return None
        else:
            the_selected_id = random.choice(ids)
            for node in PreOrderIter(tree.root):
                if node.id == the_selected_id:
                    return node

    @staticmethod
    def random_select_one_leaf_node(tree: Tree) -> Node:
        ids = tree.get_leaf_node_ids()
        if len(ids) <= 0:
            print("There is no child in the tree.")
            return None
        else:
            the_selected_id = random.choice(ids)
            for node in PreOrderIter(tree.root):
                if node.id == the_selected_id:
                    return node

    @staticmethod
    def random_select_two_nodes(tree: Tree) -> list:
        """
        select two nodes by random strategy,[copied_tree_node,source_tree_node]

        """
        tree_copied = tree.copy()
        # tree_copied.export_img("output/tree_copied.png")

        return [JsonMutation.random_select_one_node(tree_copied), JsonMutation.random_select_one_node(tree)]

        # node_num = tree.get_node_num()
        # print(node_num)
        # two_nums = random.sample(range(2, tree.get_node_num() + 1), 2)
        # tree_copied = tree.copy()
        # tree_copied.export_img("output/tree_copied.png")
        # ret = []
        # index = two_nums[0]
        # for node in PreOrderIter(tree_copied.root):
        #     index -= 1
        #     if index == 0:
        #         ret.append(node)
        # index = two_nums[1]
        # for node in PreOrderIter(tree.root):
        #     index -= 1
        #     if index == 0:
        #         ret.append(node)
        # return ret

    @staticmethod
    def drop(tree: Tree):
        """
            removes one child node c of node n,
            and Other child nodes remain unchanged.
        """
        node = JsonMutation.random_select_one_node(tree)
        print(f'#{node.id} node will be dropped!')
        node.parent = None

    @staticmethod
    def select(tree: Tree):
        """
           keeps only one child node c of node n,
           where (n, c) ∈ E. All other child nodes of n are removed.
        """
        node = JsonMutation.random_select_one_node(tree)
        if node is None:
            return
        else:
            print(f'#{node.id} node will be selected, and other siblings will be dropped!')
            for _ in node.siblings:
                _.parent = None

    @staticmethod
    def duplicate(tree: Tree):
        """
           adds a new child node r to n by copying an existing child c of n. The descendant nodes of
           c (i.e., the subtrees) are also copied
        """
        two_nodes = JsonMutation.random_select_two_nodes(tree)
        if two_nodes[0] is not None and two_nodes[1] is not None:
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

    @staticmethod
    def mutate_value(tree: Tree):
        """
        mutate primitive values
        """
        selected_node = JsonMutation.random_select_one_leaf_node(tree)
        if random.randint(0, 1) == 0:
            if selected_node.type == constants.STRING:
                selected_node.value = random.choice(commons.mutateConstants.STRINGS_FOR_MUTATED)
            elif selected_node.type == constants.NUMBER:
                selected_node.value = random.choice(commons.mutateConstants.INTEGERS_FOR_MUTATED)
            elif selected_node.type == constants.BOOLEAN:
                selected_node.value = (bool(selected_node.value) != True)
        else:
            selected_node.value = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        pass

    def single(self):
        pass

    def path(self):
        pass

    def all(self):
        pass
