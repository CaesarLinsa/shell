#_-_coding:utf-8_-_
import argparse
#
# compare 无序的文件内容中差异及并集
#

def read_file(filepath):
    with open(filepath) as f:
        return [x.strip() for x in f.readlines()]

def diff(filepart,fileall):
    filepart = sorted(filepart)
    fileall = sorted(fileall)
    return [ content for content in \
             filepart if content not in fileall]

def show_diff_results(filepart,fileall):
    template = '{0:<50}\t|\t{1:<50}'
    lineno = max(len(filepart), len(fileall))
    diff_result = diff(filepart,fileall)
    for i in range(lineno):
        if i < min(len(filepart), len(fileall)):
            if filepart[i] in diff_result:
                print("\033[01;31m %s\033[0m" %template.format(filepart[i],fileall[i]))
            else:
                print("%s" %template.format(filepart[i],fileall[i]))
        else:
            if len(filepart) < len(fileall):
                print("%s" %template.format('',fileall[i]))
            else:
                print("%s" %template.format(filepart[i],''))

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
        show_diff_results(read_file(args.source),read_file(args.target))
    if args.union:
        println(union(read_file(args.source),read_file(args.target)))

if __name__ == "__main__":
    main()
