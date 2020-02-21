# -*-coding: utf-8 -*-


def binary_search(lst, ls_v):
    # 递归进行2分查找 O(lgn)
    mid = len(lst) >> 1
    if ls_v > lst[mid]:
        # 当列表长度为0时，且不能与预期值时
        if mid == 0: return -1
        return binary_search(lst[mid:], ls_v)
    elif ls_v < lst[mid]:
        if mid == 0: return -1
        return binary_search(lst[:mid], ls_v)
    else:
        return mid


def binary_2search(lst, ls_V):
    lo = 0
    hi = len(lst)
    # 当lo和hi相邻时，终止，没有找到
    while hi - lo > 1:
        mid = (lo + hi) >> 1
        if lst[mid] > ls_V:
            hi = mid
        elif lst[mid] < ls_V:
            lo = mid
        else:
            return mid
    return -1


if __name__ == '__main__':
    lst = [1, 3, 5, 9, 21]
    print(binary_search(lst, 3))
