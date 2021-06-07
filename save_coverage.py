import os
import time
from configparser import ConfigParser

import requests
from bs4 import BeautifulSoup

def getCoverage_rate_executed_code(url, selector):
    try:
        strhtml = requests.get(url)
    except ConnectionError:
        return None
    soup = BeautifulSoup(strhtml.text, 'lxml')
    try:
        coverage_rate_executed_code = \
            str(soup.select(selector)).split('>')[1].split('<')[0]
    except:
        coverage_rate_executed_code = '0.00%'

    return coverage_rate_executed_code

while True:
    config = ConfigParser()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./restfultest_config.ini")
    config.read(path, encoding='UTF-8')
    cov_url = config.get('coverage_config', 'cov_url')
    selector = config.get('coverage_config', 'coverage_rate_executed_code_selector')
    t = time.localtime()
    cur_time = '%d:%d:%d' % (t.tm_hour, t.tm_min, t.tm_sec)
    coverage_rate = getCoverage_rate_executed_code(cov_url, selector)
    # print(cur_time, coverage_rate)
    with open('./COVERAGE_RATE.txt', 'a+') as f:  # with自动关闭文件
        f.write('%s %s \n' % (cur_time, coverage_rate))
    time.sleep(5)


