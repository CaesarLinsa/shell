try:
    from ConfigParser import RawConfigParser as ConfigParser
except Exception as e:
    from configparser import RawConfigParser as Configparser
import sys
import json


class ConfigParse(object):

    def __init__(self, file):
        self.file = file
        self.conf = ConfigParser()
    
    # read ini file to dict
    def read_file(self):
        self.conf.read(self.file)
        return {section: dict(self.conf.items(section))
                for section in self.conf.sections()}

    def ini2json(self):
        json_data = self.read_file()
        return json.dumps(json_data, indent=4, sort_keys=True)

    # write dict to ini file
    def write_file(self, di):
        dic = self._dic_to_ini_validate(di) 
        section_data = self.read_file()
        section_remove = [d for d in section_data.keys() if d not in dic.keys()]
        section_add = [s for s in dic.keys() if s not in section_data.keys()]
        for k in section_remove:
            self.conf.remove_section(k)
        # set option ,value to ini file according to the dict
        for k in di.keys():
            if k in section_add:
                self.conf.add_section(k)
            for option, value in di.get(k).items():
                self.conf.set(k, option, value)

        # remove the option that not in dict
        section_have = [k for k in section_data.keys() if k not in section_remove]
        for k in section_have:
            for option, value in section_data.get(k).items():
                if not dic.get(k).get(option, None):
                    self.conf.remove_option(k, option)

        with open(self.file, 'w') as f:
            self.conf.write(f)

    def _dic_to_ini_validate(self, dic):
        complex_types = [dict, list, tuple]
        if not isinstance(dic, dict):
            raise Exception("%s is not valid dict" % dic)
        for section, value in dic.items():
            if type(section) in complex_types:
                raise Exception("section %s must be str" % section)
            if not isinstance(value, dict):
                raise Exception("%s is not valid dict" % dic)
            for k, v in value.items():
                if type(k) in complex_types:
                    raise Exception("option %s must be str" % k)
                if type(v) in complex_types:
                    raise Exception("value %s must be str" % v)
                value[str(k)] = str(value.pop(k))
            dic[str(section)] = dic.pop(section)
        return dic
    
    # add or update option key and value
    def add_option_key_value(self, option, key, value):
        dic = self.read_file()
        options = dic.keys()
        if option in options:
            dic[option][key] = value
        else:    
            dic[option] = {key: value}
        self.write_file(dic)

    # del the key that in the option
    def del_option_key(self, option, key):
        dic = self.read_file()
        options = dic.keys()
        if option not in options:
            return
        else:
            if key not in dic[option].keys():
                return
            else:
                del dic[option][key]
        self.write_file(dic)
    
    # del option
    def del_option(self, option):
        dic = self.read_file()
        if option not in dic.keys():
            return
        else:
            del dic[option]
        self.write_file(dic)

    # get options
    def get_options(self):
        dic = self.read_file()
        return dic.keys()
    
    # get some option keys of ini file
    def get_option_keys(self, option):
        dic = self.read_file()
        if option not in dic.keys():
            return []
        return dic[option].keys()
   
    def get_option_key_value(self, option, key):
        dic = self.read_file()
        if option not in dic.keys():
            return 
        else:
            if key not in dic[option].keys():
                return
            else:
                return dic[option][key]


def print_help():
    func_list = [func for func in dir(ConfigParse) if not func.startswith("_")]
    print("Usage:\tpython\tConfigParse.py\t\n"
          "      \t      \tini-file \n"
          "      \t      \tfunction-name \n"
          "      \t      \tfunction-args")
    print("ini-file      \tinifile path such as caesar.ini")
    print("function-name \tthe function name in ConfigParse:%s" % ' '.join(func_list)) 
    print("function-args \tthe function args of function-name")


if __name__ == '__main__':
    argvs = sys.argv
    if any(["--help" in argvs, "-h" in argvs,
           len(argvs) < 3]):
        print_help()
        exit(0)
    file_path = argvs[1]
    function_name = argvs[2]
    cf = ConfigParse(file_path)
    if len(argvs) == 3:
        print(getattr(cf, function_name)())
    else:
        function_args = argvs[3:]
        print(getattr(cf, function_name)(*function_args))
