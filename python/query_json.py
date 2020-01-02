import json
import sys
import operator


class InvalidQuery(Exception):
    pass


class Filter(object):
    binary_operators = {
        u"=": operator.eq,
        u"==": operator.eq,
        u"eq": operator.eq,

        u"<": operator.lt,
        u"lt": operator.lt,

        u">": operator.gt,
        u"gt": operator.gt,

        u"<=": operator.le,
        u"le": operator.le,

        u">=": operator.ge,
        u"ge": operator.ge,

        u"!=": operator.ne,
        u"ne": operator.ne
    }

    multiple_operators = {
        u"or": any,
        u"and": all
    }

    def __init__(self, tree):
        self._eval = self.build_evaluator(tree)

    def __call__(self, value):
        return self._eval(value)

    def build_evaluator(self, tree):
        try:
            operator, nodes = list(tree.items())[0]
        except Exception:
            raise InvalidQuery("Unable to parse tree %s" % tree)
        try:
            op = self.multiple_operators[operator]
        except KeyError:
            try:
                op = self.binary_operators[operator]
            except KeyError:
                raise InvalidQuery("Unknown operator %s" % operator)

            def value_compare(value):
                value_dict = {}
                for k in nodes.keys():
                    if k in value.keys():
                        value_dict[k] = value.get(k)
                return op(value_dict, nodes)
            return value_compare
        # Iterate over every item in the list of the value linked
        # to the logical operator, and compile it down to its own
        # evaluator.
        elements = [self.build_evaluator(node) for node in nodes]
        return lambda value: op((e(value) for e in elements))

class Json_Parse(object):
    def __init__(self, filename):
        self.f = open(filename, "r+")

    def read_line(self):
        line = self.f.readline()
        if line:
            return line, json.loads(line)
        return None, None


def print_help():
    print("Usage: python query_json.py \n"
          "              json-file \n"
          "              query_str")
    print("       json-file:json file path such as caesar.json")
    print("       query_str: query string such as \"{\"gt\":{\"age\":17}}\" or"
          " \"{\"or\":[{\"eq\":{\"age\":19}},{\"eq\":{\"name\":\"caesar\"}}]}\"")

if __name__ == '__main__':
    argvs = sys.argv
    if any(["--help" in argvs, "-h" in argvs,
           len(argvs) < 3]):
        print_help()
        exit(0)
    json_file_path = argvs[1]
    query_str = argvs[2]
    f = Filter(eval(query_str))
    jp = Json_Parse(json_file_path)
    while True:
        line, data = jp.read_line()
        if line:
            if f(data):
                print line,
        else:
            break
