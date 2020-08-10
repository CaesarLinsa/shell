class AVLTree(object):
    class Node(object):

        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.left = None
            self.right = None
            self.height = 1

    def __init__(self):
        self.root = None
        self._size = 0

    def get_hight(self, node):
        if node is None:
            return 0
        return node.height

    def left_rotation(self, node):
        r = node.right
        node.right = r.left
        r.left = node
        r.height = max(self.get_hight(r.left), self.get_hight(r.right)) + 1
        node.height = max(self.get_hight(node.left) + self.get_hight(node.right)) + 1

    def right_rotation(self, node):
        l = node.left
        node.left = l.right
        l.right = node
        l.height = max(self.get_hight(l.left), self.get_hight(l.right)) + 1
        node.height = max(self.get_hight(node.left) + self.get_hight(node.right)) + 1

    def put(self, key, value):
        self.root = self._add(self.root, key, value)

    def get_balance_factor(self, node):

        if node is None:
            return 0

        return self.get_hight(node.left) - self.get_hight(node.right)

    def balance(self, node):

        # 左左
        if self.get_balance_factor(node) > 1 and self.get_balance_factor(node.left) >= 0:
            node = self.right_rotation(node)

        # 左右
        if self.get_balance_factor(node) > 1 and self.get_balance_factor(node.left) < 0:
            node = self.left_rotation(node)
            node = self.right_rotation(node)
        # 右右
        if self.get_balance_factor(node) < -1 and self.get_balance_factor(node.right) < 0:
            node = self.left_rotation(node)
        # 右左
        if self.get_balance_factor(node) < -1 and self.get_balance_factor(node.right) >= 0:
            node = self.right_rotation(node)
            node = self.left_rotation(node)
        node.height = max(self.get_hight(node.left), self.get_hight(node.right)) + 1
        return node

    def _add(self, node, key, value):

        if node is None:
            self._size += 1
            return self.Node(key, value)

        if key < node.key:
            node.left = self._add(node.left, key, value)
        elif key > node.key:
            node.right = self._add(node.right, key, value)
        else:
            node.value = value

        return self.balance(node)

    def in_order(self):
        self._in_order(self.root)

    def _in_order(self, node):
        if node.left:
            self._in_order(node.left)
        print(node.key)
        if node.right:
            self._in_order(node.right)

    def get_right_min(self, node):
        if node.left is None:
            return node
        self.get_right_min(node.left)

    def get_node(self, node, key):

        if node is None:
            return None

        if key < node.key:
            return self.get_node(node.left, key)
        elif key > node.key:
            return  self.get_node(node.right, key)
        else:
            return node

    def delete(self, key):

        node = self.get_node(self.root, key)
        if node is not None:
            self._delete(self.root, key)
            return node.value
        return None

    def _delete(self, node, key):

        ret_node = None
        if node is None:
            return None

        if key == node.key:
            if node.right is None:
                self._size -= 1
                ret_node = node.left
            elif node.left is None:
                self._size -= 1
                ret_node = node.right
            else:
                right_min = self.get_right_min(node.right)
                if right_min is not None:
                    right_min.right = self._delete(node.right, right_min.key)
                    right_min.left = node.left
                    self._size -= 1
                ret_node = right_min
        elif key <node.key:
            node.left = self._delete(node.left, key)
            ret_node = node
        elif key > node.key:
            node.right = self._delete(node.right, key)
            ret_node = node

        if ret_node is None:
            return None
        ret_node.height =  max(self.get_hight(ret_node.left), self.get_hight(ret_node.right)) + 1
        return self.balance(ret_node)




avl = AVLTree()
avl.put(12, "ca")
avl.put(23, "cae")
avl.put(6, "ci")
avl.put(16, "yy")
avl.put(10, "ww")
avl.in_order()
print("########")
print(avl.root.key)
print("########")
avl.delete(16)
print("########")
avl.in_order()
print("########")
