from typing import Union
from graphviz import Digraph
BLACK = 0
RED = 1


class RbPoint:
    parent = None
    left = None
    right = None
    color = -1  # 0: black 1:red

    def __init__(self, value, identifier):
        self.value = value
        self.info = [identifier] # type: [(int, list)]

    def add_depend(self, identifier):
        self.info.append(identifier)

    def change_color(self):
        if self.color == BLACK:
            self.color = RED
        else:
            self.color = BLACK

    def rotate(self, child):
        # Left-handed
        if child == self.left:
            if self.parent is not None:
                if self.parent.left == self:
                    self.parent.left = child
                else:
                    self.parent.right = child
            child.parent = self.parent
            self.parent = child
            self.left = child.right
            if child.right:
                child.right.parent = self
            child.right = self
            if child.parent is None:
                Rbtree.root = child
        # Right-handed
        else:
            if self.parent is not None:
                if self.parent.left == self:
                    self.parent.left = child
                else:
                    self.parent.right = child
            child.parent = self.parent
            self.right = child.left
            if child.left:
                child.left.parent = self
            child.left = self
            self.parent = child
            if child.parent is None:
                Rbtree.root = child

    def find(self, key):
        if key == self.value:
            return self
        if key < self.value:
            if self.left is None:
                return None
            else:
                return self.left.find(key)
        else:
            if self.right is None:
                return None
            else:
                return self.right.find(key)

    def add_child(self, child):
        if child.value < self.value:
            if self.left is None:
                self.left = child
                child.parent = self
                self.adjust(child)
            else:
                self.left.add_child(child)
            return

        if child.value > self.value:
            if self.right is None:
                self.right = child
                child.parent = self
                self.adjust(child)
            else:
                self.right.add_child(child)

        def view(self):
            graph = Digraph(self.name)
            if self.root is not None:
                self.root.draw(graph)
                graph.view(cleanup=True)

    def adjust(self, child):
        """ handle three condition
        g: grandparent node
        u: uncle node
        n: current node
        p: parent node

        condition1: u is None or black, child insert outside
        condition2: u is None or black, child insert inside
        condition3: u is red
        """

        def handle1(g, p):
            """
            change g and p color
            g rotate
            """
            g.rotate(p)
            g.change_color()
            p.change_color()

        def handle2(g, p, n):
            """
            1. p rotate
            2. handle condition1
            """
            p.rotate(n)
            g.rotate(n)
            n.change_color()
            g.change_color()

        def handle3(g, p, u):
            """
            1. change grandparent, parent and uncle color
            2. treat the grandparent node as a newly inserted node and continue to adjust
            """
            p.change_color()
            u.change_color()
            g.change_color()
            if g.parent is not None:
                g.parent.adjust(g)
            else:
                g.color = BLACK

        def handle4(g, p):
            p.change_color()
            g.change_color()
            if g.parent is not None:
                g.parent.adjust(g)
            else:
                # g为根节点
                g.color = BLACK

        # Insert nodes are red by default
        child.color = RED

        # If the parent node is black, the RBtree rule is still satisfied
        if self.color == BLACK:
            return

        g = self.parent

        # else grandparent node is red black
        if self == g.left:
            u = g.right
            if u is None or u.color == BLACK:
                if child == self.left:
                    handle1(g, self)
                else:
                    handle2(g, self, child)
            else:
                handle3(g, self, u)
        else:
            u = g.left
            if u is None or u.color == BLACK:
                if child == self.right:
                    handle1(g, self)
                else:
                    handle2(g, self, child)
            else:
                handle3(g, self, u)


class Rbtree:
    __root = None
    name = None

    def __init__(self, name='data analysis rbtree'):
        self.name = name
        self.number = 0
        Rbtree.__instance = self

    @property
    def root(self):
        return self.__root

    @root.setter
    def root(self, value):
        self.__root = value

    def insert(self, point: RbPoint):
        if self.root is None:
            point.color = BLACK
            self.root = point
            return
        self.number +=1
        self.root.add_child(point)

    def find(self, key) -> Union[RbPoint, None]:
        if self.root is None:
            return None
        return self.root.find(key)


