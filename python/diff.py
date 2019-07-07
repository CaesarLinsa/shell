#!/usr/bin/env python2

"""Simple diff based on LCS solution"""

import sys

def lcslen(x, y):
    """Build a matrix of LCS length.

    This matrix will be used later to backtrack the real LCS.
    """

    # This is our matrix comprised of list of lists.
    # We allocate extra row and column with zeroes for the base case of empty
    # sequence. Extra row and column is appended to the end and exploit
    # Python's ability of negative indices: x[-1] is the last elem.
    c = [[0 for _ in range(len(y) + 1)] for _ in range(len(x) + 1)]
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            if xi == yj:
                c[i][j] = 1 + c[i-1][j-1]
            else:
                c[i][j] = max(c[i][j-1], c[i-1][j])
    return c

def print_diff(c, x, y, i, j):
    """Print the diff using LCS length matrix by backtracking it"""
    if i < 0 and j < 0:
        return ""
    elif i < 0:
        print_diff(c, x, y, i, j-1)
        sys.stdout.write("- " + y[j])
    elif j < 0:
        print_diff(c, x, y, i-1, j)
        sys.stdout.write("+ " + x[i])
    elif x[i] == y[j]:
        print_diff(c, x, y, i-1, j-1)
        sys.stdout.write("  " + x[i])
    elif c[i][j-1] >= c[i-1][j]:
        print_diff(c, x, y, i, j-1)
        sys.stdout.write("- " + y[j])
    elif c[i][j-1] < c[i-1][j]:
        print_diff(c, x, y, i-1, j)
        sys.stdout.write("+ " + x[i])

def diff(x, y):
    c = lcslen(x, y)
    return print_diff(c, x, y, len(x)-1, len(y)-1)

def usage():
    sys.stdout.write("Usage: {} <file1> <file2>".format(sys.argv[0]))

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    with open(sys.argv[1], 'r') as f1, open(sys.argv[2], 'r') as f2:
        diff(f1.readlines(), f2.readlines())

if __name__ == '__main__':
    main()
