from ConfigParser import ConfigParser

class ConfigParse(object):

    def __init__(self, file):
        self.file = file
        self.conf = ConfigParser()

    def read_file(self):
        self.conf.read(self.file)
        return { section:dict(self.conf.items(section)) for section in self.conf.sections()}

    def write_file(self, di):
        section_data = self.read_file()
        section_remove = [ d for d in section_data.keys() if d not in di.keys()]
        section_add = [ s for s in di.keys() if s not in section_data.keys() ]
        for k in section_remove:
            self.conf.remove_section(k)
        for k in di.keys():
             if k in section_add:
                 self.conf.add_section(k)
             for option,value in di.get(k).items():
                 self.conf.set(k,option,value)

        section_have = [ k for k in section_data.keys() if k not in section_remove]
        for k in section_have:
            for option,value in section_data.get(k).items():
                if not di.get(k).get(option, None):
                    self.conf.remove_option(k, option)

        with open(self.file,'w') as f:
            self.conf.write(f)


