# -*-coding: utf-8 -*-


class Node(object):

    def __init__(self, value, left=None, right=None, parent=None):
        self.left = left
        self.value = value
        self.right = right
        self.parent = parent

    def __repr__(self):
        return "Node({})".format(self.value)


class BinaryTree(object):

    def __init__(self, lst):
        self.root_node = Node(lst[0])
        self.root_node.parent = None
        for v in lst[1:]:
            self.insert(self.root_node, v)

    def get(self, value, node):
        if node is None:
            # 递归查询，如果查询到节点到叶子节点，还没查出结果
            # 则为False
            return False, None
        if node.value == value:
            # 查到节点时，返回节点和其父节点
            return True, node
        elif value < node.value:
            return self.get(value, node.left)
        else:
            return self.get(value, node.right)

    def insert(self, node, value):
        if node is None:
            node = self.root_node
        if value > node.value:
            if node.right is None:
                new_node = Node(value)
                node.right = new_node
                new_node.parent = node
            else:
                self.insert(node.right, value)
        elif value < node.value:
            if node.left is None:
                new_node = Node(value)
                node.left = new_node
                new_node.parent = node
            else:
                self.insert(node.left, value)

    def delete(self, node, value):
        """
        删除的节点N存在以下3情况：
        1. 叶子节点：直接删除N，父节点指向N节点为None
        2. 存在一个子节点：将N父节点指针，指向N的子节点
        3. 存在两个子节点：找到右子树的最小节点M，删除M节点，将M节点值赋给N
        :param node: 自此节点往下搜索，需要删除的节点
        :param value: 需要删除的值为value的节点
        """
        flag, node = self.get(value, node)
        if not flag:
            print("node值为%s不存在" % value)
            raise KeyError("not find value error")
        if node.left is None and node.right is None:
            if node.parent is None:
                self.root_node = None
            elif node.value < node.parent.value:
                node.parent.left = None
            else:
                node.parent.right = None
        elif node.left is None:
            if node.parent is None:
                self.root_node = node.right
            elif node.value < node.parent.value:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
        elif node.right is None:
            if node.parent is None:
                self.root_node = node.left
            elif node.value < node.parent.value:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
        else:
            right_min_node = self.find_right_min(node.right)
            self.delete(node.right, right_min_node.value)
            node.value = right_min_node.value

    def find_right_min(self, node):
        while True:
            left_node = node.left
            if left_node is None:
                return node
            node = left_node

    def inOrderTraverse(self, node):
        if node is not None:
            self.inOrderTraverse(node.left)
            print(node.value)
            self.inOrderTraverse(node.right)


if __name__ == '__main__':
    lst = [5, 7, 3, 6, 1, 4, 3, 6, 9]
    tree = BinaryTree(lst)
    tree.inOrderTraverse(tree.root_node)
    flag, node = tree.get(1, tree.root_node)
    print(flag, node)
    tree.delete(tree.root_node, 5)
    tree.inOrderTraverse(tree.root_node)
