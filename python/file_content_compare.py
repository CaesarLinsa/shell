#_-_coding:utf-8_-_
import argparse
#
# compare 无序的文件内容中差异及并集
#

def read_file(filepath):
    with open(filepath) as f:
        return f.readlines()

def diff(filepart,fileall):
    return [ content for content in \
             filepart if content in fileall ]


def union(filepart, fileall):
    for line in filepart:
        if line not in fileall:
            fileall.append(line)
    return fileall

def println(mylist):
    for li in mylist:
        print(li),

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-diff','--diff',\
                 help="compare part not in all lines"\
                 ,action="store_true")
    parser.add_argument("-union","--union",\
                 help="union the content beetwen part and all",\
                 action="store_true")
    parser.add_argument("-s","--source",help="source file",
                 action="store",type=str)
    parser.add_argument("-t","--target",help="source file",
                 action="store",type=str)
    args = parser.parse_args()
    if args.diff:
        println(diff(read_file(args.source),read_file(args.target)))
    if args.union:
        println(union(read_file(args.source),read_file(args.target)))

if __name__ == "__main__":
    main()
