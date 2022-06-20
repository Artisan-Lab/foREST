BLACK = 0
RED = 1


def data_RBtree():
    """ Accessor for the FuzzingMonitor singleton """
    return Rbtree.Instance()


class Rbtree:
    __instance = None
    root = None
    name = None

    @staticmethod
    def Instance():
        """ Singleton's instance accessor

        @return FuzzingMonitor instance
        @rtype  FuzzingMonitor

        """
        if Rbtree.__instance is None:
            raise Exception("foREST Monitor not yet initialized.")
        return Rbtree.__instance

    def __init__(self, name='data analysis rbtree'):
        self.name = name
        self.__instance = self


    def insert(self, point):
        if self.root is None:
            point.color = BLACK
            self.root = point
            return
        self.root.add_child(point)

    def find(self, key):
        if self.root is None:
            print('该树为空树!')
            return None
        return self.root.find(key)


class RbPoint:
    parent = None
    left = None
    right = None
    color = -1  # 节点颜色 0 黑 1红
    key = None
    tree = None

    def __init__(self, key, value:list):
        self.key = key
        self.value = value

    def change_color(self):
        if self.color == BLACK:
            self.color = RED
        else:
            self.color = BLACK

    def rotate(self, child):
        # 和左孩子进行旋转
        if child == self.left:
            print('从左往右旋')
            if self.parent is not None:
                if self.parent.left == self:
                    self.parent.left = child
                else:
                    self.parent.right = child
            child.parent = self.parent
            self.parent = child
            self.left = child.right
            child.right = self
            if child.parent is None:
                # 该节点变为根节点
                print('根节点变更')
                tree.root = child
        # 和右孩子进行旋转
        else:
            print('从右往左旋')
            if self.parent is not None:
                if self.parent.left == self:
                    self.parent.left = child
                else:
                    self.parent.right = child
            child.parent = self.parent
            self.right = child.left
            child.left = self
            self.parent = child
            if child.parent is None:
                # 该节点变为根节点
                print('根节点变更')
                tree.root = child

    def find(self, key):
        print('当前节点值:', self.key, '查找值:', key)
        if key == self.key:
            return self
        if key < self.key:
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
        if child.key < self.key:
            if self.left is None:
                self.left = child
                child.parent = self
                print('键为', child.key, '的节点插入到键为', self.key, '的节点的左孩子处')
                self.adjust(child)
            else:
                self.left.add_child(child)
            return

        if child.key > self.key:
            if self.right is None:
                self.right = child
                child.parent = self
                print('键为', child.key, '的节点插入到键为', self.key, '的节点的右孩子处')
                self.adjust(child)
            else:
                self.right.add_child(child)

    def adjust(self, child):
        def handle1(g, p):
            g.rotate(p)
            g.change_color()
            p.change_color()
            print('状况1调整完毕')

        def handle2(g, p, n):
            p.rotate(n)
            # 状况2->状况1
            g.rotate(n)
            n.change_color()
            g.change_color()
            print('状况2')

        def handle3(g, p, u):
            print('状况3')
            p.change_color()
            u.change_color()
            g.change_color()
            if g.parent is not None:
                g.parent.adjust(g)
            else:
                # g为根节点
                g.color = BLACK

        def handle4(g, p):
            p.change_color()
            g.change_color()
            if g.parent is not None:
                g.parent.adjust(g)
            else:
                # g为根节点
                g.color = BLACK

        print('开始调整')
        # 子节点默认红色
        child.color = RED
        # 根据p节点(父节点)颜色判断是否需要调整
        if self.color == BLACK:
            # 黑色，不需要调整
            return

        # 父节点也为红色，必须调整
        # 父节点为红色，G节点(父节点的父节点)必存在且必为黑色
        # 状况1:U节点(叔叔节点)为黑色，n节点(新增加的节点)外侧插入
        # 状况2:u为黑色，n内侧插入
        # 状况3:u为红色
        g = self.parent
        if self == g.left:
            # 父节点为祖父节点的左孩子,叔叔节点为祖父节点的右孩子
            u = g.right
            if u is None or u.color == BLACK:
                # u节点为黑色，状况1或2
                if child == self.left:
                    # 状况1
                    handle1(g, self)
                else:
                    # 状况2
                    handle2(g, self, child)
            else:
                # u节点为红色，状况3
                handle3(g, self, u)
        # 孩子节点为父节点的左孩子，状况1
        else:
            # 父节点为祖父节点的右孩子
            u = g.left
            if u is None or u.color == BLACK:
                if child == self.right:
                    # 状况1
                    handle1(g, self)
                else:
                    # 状况2
                    handle2(g, self, child)
            else:
                # 状况3,u节点为红色
                handle3(g, self, u)


if __name__ == '__main__':
    tree = Rbtree('t2')
    for i in ["a", "b", "c"]:
        p = RbPoint(i)
        tree.insert(p)
    a= tree.find("d")