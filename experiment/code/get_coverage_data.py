import requests
import json
import time
import datetime
local_host = "http://192.168.112.168/api/v4/templates/get_coverage"



start_time = datetime.datetime.now()

def get_coverage():
    while True:
        response_dic = json.loads(requests.get(local_host).text)
        coverage_list = [datetime.datetime.now()-start_time, response_dic['covered'], response_dic['covered_line']]
        time.sleep(0.05)
        with open('../data/data', 'a') as f:
            f = f.write(str(coverage_list[0]) + ',' + str(coverage_list[1]) + ',' + str(coverage_list[2]) + '\n')


if __name__ == '__main__':
    get_coverage()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
