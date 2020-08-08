# -*-coding:utf-8-*-


class Node(object):

    def __init__(self, left=None, right=None, value=None, height=None, color="RED"):
        self.left = left
        self.right = right
        self.value = value
        self.height = height
        self.color = color

    def set_black_node(self):
        self.color = "BLACK"

    def set_red_node(self):
        self.color = "RED"

    def __str__(self):
        return "Node({},{})".format(self.value, self.color)


def is_red_node(node):
    if node is None:
        return False
    return node.color == "RED"


class RBTree(object):

    def __init__(self):
        self.root = None

    def left_rotation(self, node):
        r = node.right
        node.right = r.left
        r.left = node
        r.color = node.color
        node.set_red_node()
        r.height = node.height
        node.height = int(node.left.height if node.left is not None else 0) + int(
            node.right.height if node.right is not None else 0) + 1
        return r

    def right_rotation(self, node):
        l = node.left
        node.left = l.right
        l.right = node
        l.color = node.color
        node.set_red_node()
        l.height = node.height
        node.height = int(node.left.height if node.left is not None else 0) + int(
            node.right.height if node.right is not None else 0) + 1
        return l

    def flip_color(self, node):
        if not is_red_node(node):
            node.set_red_node()
        else:
            node.set_black_node()
        if is_red_node(node.left):
            node.left.set_black_node()
        else:
            node.left.set_red_node()
        if is_red_node(node.right):
            node.right.set_black_node()
        else:
            node.right.set_red_node()
        return node

    def put(self, value):
        self.root = self._insert(self.root, value)
        self.root.set_black_node()

    def _insert(self, node, value):
        if node is None:
            return Node(value=value, height=1)

        if value < node.value:
            node.left = self._insert(node.left, value=value)
        elif value > node.value:
            node.right = self._insert(node.right, value=value)
        else:
            node.value = value
        node = self.balance(node)
        return node

    def balance(self, node):
        # 默认左旋，左黑，右红，node左旋
        if not is_red_node(node.left) and is_red_node(node.right):
            node = self.left_rotation(node)
        # 连续左节点， 右旋
        if is_red_node(node.left) and is_red_node(node.left.left):
            node = self.right_rotation(node)
        # 左右都红，则该节点和左右节点染相反色
        if is_red_node(node.left) and is_red_node(node.right):
            node = self.flip_color(node)
        node.height = int(node.left.height if node.left is not None else 0) + int(
            node.right.height if node.right is not None else 0) + 1
        return node

    def get(self, node, item):
        if node is None:
            return None

        if item < node.value:
            return self.get(node.left, item)
        elif item > node.value:
            return self.get(node.right, item)
        else:
            return node

    def inOrderTraverse(self, node):
        if node.left:
            self.inOrderTraverse(node.left)
        print(node)
        if node.right:
            self.inOrderTraverse(node.right)

    def move_red_left(self, node):
        """
        :return: 2节点处理，若node节点右边的左子节点为红，染色（node及左右子节点）->进行右旋转(右节点)->左旋转-->
        染色（node及左右子节点），生成4节点
        若右边左子节点为黑， 染色（node及左右子节点），生成4节点
        """
        # node及左右节点重新染色
        node = self.flip_color(node)
        # 堂孙子节点是红色，可以生成4 节点
        if is_red_node(node.right.left):
            node = self.right_rotation(node.right)
            node = self.left_rotation(node)
            node = self.flip_color(node)
        return node

    def move_red_right(self, node):
        # 右边2节点处理
        node = self.flip_color(node)
        if is_red_node(node.left.left):
            node = self.right_rotation(node)
            node = self.flip_color(node)
        return node

    def get_delete_min(self, node):
        if node.left is None:
            return None
        # 无 3-4 节点
        if not is_red_node(node.left) and not is_red_node(node.left.left):
            node = self.move_red_left(node)
        node.left = self.get_delete_min(node.left)
        return self.balance(node)

    def right_min_node(self, node):
        if node.left is None:
            return node
        else:
            return self.right_min_node(node.left)

    def _delete(self, node, value):

        if value < node.value:
            if not is_red_node(node.left) and not is_red_node(node.left.left):
                node = self.left_rotation(node)
            node.left = self._delete(node.left, value)
        else:
            if is_red_node(node.left):
                node = self.right_rotation(node)
            if value == node.value and node.right is None:
                return None
            if not is_red_node(node.right) and not is_red_node(node.right.left):
                node = self.move_red_right(node)

            if value == node.value:
                min_node = self.right_min_node(node.right)
                node.value = min_node.value
                node.right = self.get_delete_min(node.right)
            else:
                node.right = self._delete(node.right, value)

        return self.balance(node)

    def delete(self, value):
        self.root = self._delete(self.root, value)
        self.root.set_black_node()


rb = RBTree()
rb.put(20)
rb.put(30)
rb.put(10)
rb.put(40)
rb.put(15)
rb.delete(20)
print("=========")
print(rb.root)
print(rb.root.left)
print(rb.root.left.left)
print(rb.root.right)
print("==========")
rb.inOrderTraverse(rb.root)
