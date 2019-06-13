# coding:utf-8

def line_use(lines):
    # sort the list of tuples, the tuple contains two elements
    # first is start point, second is end point
    sort_lines = sorted(lines, key=lambda tup: tup[0])
    for i, line in enumerate(sort_lines):
        if i == 0:
            continue
        # if second tuple first smaller than first tuple end
        # we combine the two tuple.egg.[(1,3),(2,4)] return
        # [(1,4)]
        if line[0] <= sort_lines[i-1][1]:
           sort_lines[i] = (sort_lines[i-1][0],line[1])
           sort_lines.pop(i-1)
           return line_use(sort_lines)
    return sort_lines

def line_spare(lines):
    sort_lines = sorted(lines, key=lambda tup:tup[0])
    for i, line in enumerate(sort_lines):
        if i == 0:
            continue
        # second tuple first bigger than first tuple end
        # we return the bettwens.egg [(1,3),(4,5)],return
        # [(3,4)]
        if line[0] >= sort_lines[i-1][1]:
            sort_lines[i] = (sort_lines[i-1][1], line[0])
            sort_lines.pop(i-1)
            return line_spare(sort_lines)
    return sort_lines


def main(lines):
lines_use = line_use(lines)
lines_free = line_spare(lines_use)

