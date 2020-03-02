# -*- coding:utf-8 -*-


def select_sort(lst):
    """ 选择排序
    每次选择剩下元素中最小元素与首元素交换位置
    时间复杂度O(n²)
    """
    for i, e in enumerate(lst):
        minindex = lst.index(min(lst[i:])) # 剩下元素的最小值索引
        lst[i], lst[minindex] = lst[minindex], lst[i] # 最小值与首元素交换位置


if __name__ == '__main__':
    lst = [4, 5, 2, 1, 11, 23, 20]
    select_sort(lst)
    print(lst)
