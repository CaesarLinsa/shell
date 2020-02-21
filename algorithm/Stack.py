class Stack(object):

    def __init__(self):
        self._items = []

    def top(self):
        return self._items[-1]

    def push(self, v):
        self._items.append(v)

    def pop(self):
        return self._items.pop()

    def len(self):
        return len(self._items)

    def is_empty(self):
        return not self._items


def convert(number, base):
    s = Stack()
    while number != 0:
        s.push(int(number % base))
        number = int(number / base)
    while not s.is_empty():
        print(s.pop(), end='')


if __name__ == '__main__':
    convert(10, 2)
