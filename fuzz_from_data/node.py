from anytree import NodeMixin

from sequence import Sequence


class Node(NodeMixin):  # Add Node feature
    """
    primitive values:leaf nodes
    object or array values : parent nodes
    """

    def __init__(self, key, value, type, parent=None, children=None):
        super(Node, self).__init__()
        self.id = Sequence.get_seq()
        self.key = key
        self.value = value
        self.type = type
        self.parent = parent
        if children:  # set children only if given
            self.children = children
        # used for Visualization
        self.name = f'#{self.id}.{self.key}:{self.type}({self.value})'

    def __str__(self):
        return self.key + " " + self.value + " " + self.type
