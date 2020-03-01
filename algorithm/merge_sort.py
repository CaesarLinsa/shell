# -*- coding:utf-8 -*-


def merge_sort(arr):
    global aux
    aux = [''] * len(arr)
    __sort(arr, 0, len(arr)-1)

def __sort(arr, lo, hi):
    mid = lo + (hi - lo)/2
    if lo >= hi : return
    __sort(arr, lo, mid) # 左边部分排序
    __sort(arr, mid + 1, hi) #右边部分排序
    __merge(arr, lo, mid, hi) # 左右两边合并

def __merge(arr, lo, mid, hi):
    i = lo
    j = mid + 1
    for k in range(lo, hi + 1):
        aux[k] = arr[k]
    for k in range(lo, hi + 1):
        if i > mid: # 左边用尽(取右边元素)
            arr[k] = aux[j]
            j += 1
        elif j > hi: # 右边用尽(取左边元素)
            arr[k] = aux[i]
            i += 1
        elif aux[i] < aux[j]: # 左边小于右边(取左边元素)
            arr[k] = aux[i]
            i += 1
        else: # 右边小于左边(取右边元素)
            arr[k] = aux[j]
            j += 1

if __name__ == '__main__':
    li = [8, 4, 3, 7,11, 23,15, 1]
    merge_sort(li)
    print(li)
