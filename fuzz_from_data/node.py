from anytree import NodeMixin


class Node(NodeMixin):  # Add Node feature
    def __init__(self, key, value, type, parent=None, children=None):
        super(Node, self).__init__()
        self.key = key
        self.value = value
        self.type = type
        self.parent = parent
        if children:  # set children only if given
            self.children = children

    def __str__(self):
        return self.key + " " + self.value + " " + self.type




