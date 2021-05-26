import os

from module.Coverage_get_tool import GetCoverage
from configparser import ConfigParser

config = ConfigParser()
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
config.read(path)

cov_url = config.get('coverage_config', 'cov_url')

a = GetCoverage().getCoverage_rate_executed_code(cov_url)
print(a)
b = ''.join(list(a)[:-1])
print(b)
print(type(b))
c = float(b)
print(c)