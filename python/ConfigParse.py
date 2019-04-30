from ConfigParser import ConfigParser

class ConfigParse(object):

    def __init__(self, file):
        self.file = file
        self.conf = ConfigParser()
    
    # read ini file to dict
    def read_file(self):
        self.conf.read(self.file)
        return { section:dict(self.conf.items(section)) for section in self.conf.sections()}

    # write dict to ini file
    def write_file(self, di):
        dic = self._dic_to_ini_validate(di) 
        section_data = self.read_file()
        section_remove = [ d for d in section_data.keys() if d not in dic.keys()]
        section_add = [ s for s in dic.keys() if s not in section_data.keys() ]
        for k in section_remove:
            self.conf.remove_section(k)
        # set option ,value to ini file according to the dict
        for k in di.keys():
             if k in section_add:
                 self.conf.add_section(k)
             for option,value in di.get(k).items():
                 self.conf.set(k,option,value)

        # remove the option that not in dict
        section_have = [ k for k in section_data.keys() if k not in section_remove]
        for k in section_have:
            for option,value in section_data.get(k).items():
                if not dic.get(k).get(option, None):
                    self.conf.remove_option(k, option)

        with open(self.file,'w') as f:
            self.conf.write(f)

    def _dic_to_ini_validate(self, dic):
        complex_types = [dict, list, tuple]
        if not isinstance(dic, dict):
            raise Exception("%s is not valid dict" %dic)
        for section, value in dic.items():
            if type(section) in complex_types:
                raise Exception("section %s must be str" %section)
            if not isinstance(value, dict):
                raise Exception("%s is not valid dict" %dic)
            for k,v in value.items():
                if type(k) in complex_types:
                    raise Exception("option %s must be str" %k)
                if type(v) in complex_types:
                    raise Exception("value %s must be str" %v)
                value[str(k)]=str(value.pop(k))
            dic[str(section)] = dic.pop(section)
        return dic

