# -*- coding: utf-8 -*-


def insert_sort(lst):
    """ 插入排序
    从第一个元素为当前元素开始，当其前面元素大于当前元素，则交换位置
    """
    for i in range(1, len(lst)):
        j = i
        while j > 0 and lst[j - 1] > lst[j]:
            lst[j - 1], lst[j] = lst[j], lst[j - 1]
            j -= 1


if __name__ == '__main__':
    lst = [4, 5, 2, 1, 11, 23, 20]
    insert_sort(lst)
    print(lst)
