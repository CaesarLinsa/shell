import configparser
from copy import copy
import collections


class Error(object):
    pass


def is_option_register(opts, opt):
    if opt in opts:
        return True
    return False


class _Option(object):
    UNSET = object()

    def __init__(self, name, default, type):
        if type is None:
            raise ValueError("type must not be none")
        self.name = name
        self.type = type
        self.default = default
        self._value = self.UNSET

    def value(self):
        return self.default if self._value is _Option.UNSET else self._value

    def set(self, value):
        self._value = value

    def convert(self, value):
        return self.type(value)


class OptGroup(object):

    def __init__(self, group_name=None):
        if group_name is None:
            group_name = 'DEFAULT'
        self.group_name = group_name
        self.opts = {}

    def register_opt(self, opt):
        if is_option_register(self.opts, opt):
            return False
        self.opts[opt.name] = opt
        return True


class GroupAttr(collections.Mapping):

    def __init__(self, opt_parse, opt_group):
        self.opt_parse = opt_parse
        self.opt_group = opt_group

    def __getattr__(self, name):
        return self.opt_parse._get(name, self.opt_group)

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __contains__(self, item):
        return item in self.opt_group.opts

    def __iter__(self):
        for key in self.opt_group.opts.keys():
            yield key

    def __len__(self):
        return len(self.opt_group.opts)


class OptionParse(object):

    def __init__(self):
        self.__dict__['_options'] = {}
        self.__dict__['_groups'] = {}

    def __getattr__(self, name):
        return self._get(name)

    def define(self, name, default, type, group_name):
        option = _Option(name, default, type)
        if group_name is None:
            self.register_opt(option, None)
        else:
            opt_group = self._get_group(group_name)
            if group_name not in self._groups:
                self.groups[group_name] = opt_group
            self.register_opt(option, opt_group)

    def register_group(self, group):
        if group.group_name in self._groups:
            return
        self._groups[group.group_name] = copy(group)

    def _get_group(self, group_or_name):
        group = group_or_name if isinstance(group_or_name, OptGroup) else None
        group_name = group.group_name if group else group_or_name

        if group_name not in self._groups:
            self.register_group(OptGroup(group_name))
        return self._groups[group_name]

    def register_opt(self, opt, group=None):
        if group is not None:
            group = self._get_group(group)
            return group.register_opt(opt)

        if is_option_register(self._options, opt):
            return False

        self._options[opt.name] = opt
        return True

    def _get(self, name, group=None):
        if group is None and name in self._groups:
            return GroupAttr(self, self._get_group(name))
        return self._get_opt_info(name, group).value()

    def _get_opt_info(self, opt_name, group=None):

        if group is None:
            opts = self._options
        else:
            group = self._get_group(group)
            opts = group.opts

        if opt_name not in opts:
            raise Error
        return opts[opt_name]

    def parse_config_file(self, path):
        config = ini2json(path)
        for section in config:
            if 'DEFAULT' == section:
                default_section = config.get('DEFAULT')
                for name in default_section:
                    if name in self._options:
                        option = self._options[name]
                        option.set(option.convert(default_section.get(name)))
            elif section in self._groups:
                section_data = config.get(section)
                group = self._groups[section]
                for k, v in section_data.items():
                    if k in group.opts:
                        option = group.opts[k]
                        option.set(option.convert(v))


options = OptionParse()


def define(name, default, type, group=None):
    return options.define(name, default, type, group)


def parse_config_file(path):
    return options.parse_config_file(path)


def ini2json(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    ini_json = {section: dict(config.items(section)) for section in config.sections()}
    if 'DEFAULT' in config:
        ini_json.update({'DEFAULT': dict(config['DEFAULT'])})
    return ini_json
