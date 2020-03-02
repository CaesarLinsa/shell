# -*-coding:utf-8 -*-


class HeapQueue(object):
    N = 0

    def __init__(self, num):
        self.pq = [''] * (num + 1)

    def is_empty(self):
        return self.N == 0

    def insert(self, v):
        self.N += 1
        self.pq[self.N] = v
        self.swim(self.N)

    def delMax(self):
        max = self.pq[1]
        self.pq[1] = self.pq[self.N]
        self.pq[self.N] = ''
        self.N -= 1
        self.sink(1)
        return max

    def swim(self, k):
        while k > 1 and self.pq[k] > self.pq[int(k / 2)]:
            self.pq[k], self.pq[int(k / 2)] = self.pq[int(k / 2)], self.pq[k]
            k = int(k / 2)

    def sink(self, k):
        while 2 * k <= self.N:
            j = 2 * k
            if j < self.N and self.pq[j] < self.pq[j + 1]: j += 1
            if not self.pq[j] > self.pq[k]: break
            self.pq[j], self.pq[k] = self.pq[k], self.pq[j]
            k = j


if __name__ == '__main__':
    q = HeapQueue(10)
    q.insert(10)
    q.insert(20)
    q.insert(5)
    q.insert(100)
    q.insert(36)
    q.insert(72)
    q.insert(45)
    q.insert(43)
    q.insert(40)
    q.insert(33)
    print(q.N)
    while q.N != 0:
        print(q.delMax(), end=" ")
