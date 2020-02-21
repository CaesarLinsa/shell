# -*-coding:utf-8 -*-
def lcs(str_li1, str_li2):
    # 最长公共子序列： 求两字符串中最长相同部分，可以用来实现diff功能
    # 递归实现：
    # 1.若两个列表，任一为空则，最长子序列为""
    # 2.若两个列表，末尾字符相同，则最长子序列为 列表去除末尾字符后的lcs结果 + 末尾字符
    # 3. 若末尾字符不同，则为第一个列表去除最后字符与第二个列表或者第二个列表去除末尾与第一个列表lcs
    # 中最长的列表
    if not str_li1 or not str_li2:
        return ""
    else:
        if str_li1[-1] == str_li2[-1]:
            return lcs(str_li1[:-1], str_li2[:-1]) + str_li1[-1]
        else:
            left = lcs(str_li1[:-1], str_li2)
            right = lcs(str_li1, str_li2[:-1])
            if len(right) > len(left):
                return right
            else:
                return left


def short_lcs(li1, li2):
    # 使用遍历，当元素相同时，记录元素
    # 初始化一个 i+1 j+1的数组
    # 如果i+1，j+1位置元素相等，则此位置在i，j位置基础 +1
    # 否则，获取左右和上方中最大的值
    c_li = list()
    c = [[0 for _ in range(len(li1) + 1)] for _ in range(len(li2) + 1)]
    for i, lv1 in enumerate(li2):
        for j, lv2 in enumerate(li1):
            if lv1 == lv2:
                c[i + 1][j + 1] = c[i][j] + 1
                if not c_li or c_li[-1] != li2[i]:
                    c_li.append(li2[i])
            else:
                c[i + 1][j + 1] = max(c[i][j + 1], c[i + 1][j])
    return c_li


if __name__ == '__main__':
    c = short_lcs(list("advantage"), list("didactical"))
    print(c)
