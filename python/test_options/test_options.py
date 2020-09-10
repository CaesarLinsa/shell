
from python.options import define, options, parse_config_file

define("port", default=8888, type=int)

define("host", default='1.23.1.23', type=str, group="hostlist")

# parse_config_file('./test.conf')

print(options.port)
print(options.hostlist.host)
