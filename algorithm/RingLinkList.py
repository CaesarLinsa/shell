# -*- conding:uft-8 -*-


class Node(object):
    def __init__(self, value):
        self.value = value
        self.next = None


class RingLinkList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return None == self.head

    def append(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = node
            self.head.next = node
        else:
            cur = self.head
            while cur.next != self.head:
                pre = cur
                cur = cur.next
            cur.next = node
            node.next = self.head

    def head_append(self, value):
        node = Node(value)
        if self.is_empty():
            self.head = node
            self.head.next = node
        else:
            cur = self.head
            node.next = cur
            self.head = node
            while cur.next != self.head:
                cur = cur.next
            cur.next = node

    def traversal(self):
        if self.is_empty():
            pass
        else:
            cur = self.head
            while cur.next != self.head:
                print(cur.value)
                cur = cur.next
            print(cur.value)

    def __len__(self):
        if self.is_empty():
            return 0
        else:
            cur = self.head
            size = 1
            while cur.next != self.head:
                size += 1
                cur = cur.next
            return size


if __name__ == '__main__':
    # 约瑟夫问题
    r = RingLinkList()
    n = 32
    m = 3
    for i in range(1, n):
        r.append(i)
    cur = r.head
    # 当只剩下一个节点时退出循环
    while cur.next != cur:
        for i in range(m - 1):
            pre = cur
            cur = cur.next
        print(cur.value)
        # 删除m倍数节点
        pre.next = cur.next
        # 从下个节点重新开始
        cur = pre.next
    print(cur.value)
