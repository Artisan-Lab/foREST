import commons.mutateConstants
from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from commons.sequence import Sequence
from mutation.jsonTree.tree import *
from mutation.mutation import Mutation


class JsonMutation(Mutation):
    """
    mutation strategies
    """

    def __init__(self, tree: Tree):
        self.tree = tree

    def random_select_one_node(self) -> Node:
        """
        select the node by random strategy
        note,we cannot select the jsonTree root node
        """
        ids = self.tree.get_node_ids()
        # delete root id
        ids.remove(self.tree.root.id)
        if len(ids) <= 0:
            print("There is no child in the jsonTree.")
            return None
        else:
            the_selected_id = random.choice(ids)
            for node in PreOrderIter(self.tree.root):
                if node.id == the_selected_id:
                    return node

    def random_select_one_leaf_node(self) -> Node:
        """
        select a leaf node randomly
        """
        ids = self.tree.get_leaf_node_ids()
        if len(ids) <= 0:
            print("There is no child in the jsonTree.")
            return None
        else:
            the_selected_id = random.choice(ids)
            for node in PreOrderIter(self.tree.root):
                if node.id == the_selected_id:
                    return node

    def random_select_two_nodes(self) -> list:
        """
        select two nodes by random strategy,[copied_tree_node,source_tree_node]

        """
        tree_copied = self.tree.copy()
        return [tree_copied.random_select_one_node(), self.random_select_one_node()]

    def drop(self):
        """
            removes one child node c of node n,
            and Other child nodes remain unchanged.
        """
        node = self.random_select_one_node()
        print(f'#{node.id} node will be dropped!')
        node.parent = None

    def select(self):
        """
           keeps only one child node c of node n,
           where (n, c) ∈ E. All other child nodes of n are removed.
        """
        node = self.random_select_one_node()
        if node is None:
            return
        else:
            print(f'#{node.id} node will be selected, and other siblings will be dropped!')
            for _ in node.siblings:
                _.parent = None

    def duplicate(self):
        """
           adds a new child node r to n by copying an existing child c of n. The descendant nodes of
           c (i.e., the subtrees) are also copied
        """
        two_nodes = self.random_select_two_nodes()
        if two_nodes[0] is not None and two_nodes[1] is not None:
            print(f'#{two_nodes[0].id} will be copied to {two_nodes[1].id}')
            two_nodes[0].parent = two_nodes[1]

    def type(self):
        """
            changes the labeled type of a node
            e.g. primitive type <-> array/object type
            e.g. boolean <-> string
            e.g. number <-> string
        """

        pass

    def mutate_value(self):
        """
        mutate primitive values
        """
        selected_node = self.random_select_one_leaf_node()
        # if random.randint(0, 1) == 0:
        if selected_node.type == constants.STRING:
            selected_node.value = random.choice(commons.mutateConstants.STRINGS_FOR_MUTATED)
        elif selected_node.type == constants.NUMBER:
            selected_node.value = random.choice(commons.mutateConstants.INTEGERS_FOR_MUTATED)
        elif selected_node.type == constants.BOOLEAN:
            selected_node.value = (bool(selected_node.value) != True)
        # else:
        #     selected_node.value = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        # pass

    def single(self):
        """
        single
        """
        pass

    def path(self):
        """
        path
        """
        pass

    def all(self):
        """
        all
        """
        pass

    def start(self):
        """
        start mutating
        """

        print("json mutating...")

        if Utils.decision(FUZZ_FROM_DATA_CONFIG.json_drop_mutation_probability):
            self.drop()

        if Utils.decision(FUZZ_FROM_DATA_CONFIG.json_value_mutation_probability):
            self.mutate_value()

        if Utils.decision(FUZZ_FROM_DATA_CONFIG.json_selection_mutation_probability):
            self.select()

    def result(self):
        Sequence.seq_num = 0
        return self.tree.dump()
