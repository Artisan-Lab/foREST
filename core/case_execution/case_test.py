import random
import time

import redis
import requests
from rest_framework.utils import json
from module.Coverage_get_tool import GetCoverage
from module.notify import notify
from module.response_parse import response_parse
from module.make_url import make_url
from module.save_success_case import save_success_case
from module.get_success_case import get_success_case

fuzz_pool = redis.StrictRedis(host='127.0.0.1', port=6379, db=7, decode_responses=True)

'''
fuzz(optional, matr, tag, api_info, fuzz_test_times, cov_url, Authorization)
'''

def fuzz(optional, matr, tag, api_info, fuzz_test_times, cov_url, Authorization, operation_mode):

    ini_coverage_rate_executed_code = 1000
    if operation_mode == 0:
        ini_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
        print(ini_coverage_rate_executed_code)
        if not ini_coverage_rate_executed_code:
            chongqi = requests.get('http://10.177.74.168:5000/restart')
            if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                print('重启成功~~~~')
            else:
                notify()

    headers = {}
    data = {}
    pa_locations = []
    pa_names = []
    value_fuzzs = []
    id = api_info.api_id
    url = api_info.path
    method = api_info.http_method
    # list: fuzz_cases = ["{'name': 'dss2', 'id': '16540'}", "{'name': 'dss1', 'id': '16540'}"]
    if not optional:
        fuzz_cases = fuzz_pool.sscan(str(id))[1]
    else:
        fuzz_cases = fuzz_pool.sscan(str(id) + 'optional')[1]
        # 从必选参数fuzz成功的case中取case加入到optional的fuzz case中
        fuzz_success_data = get_success_case().get_fuzz_success(matr, tag, method)
        if fuzz_success_data != None:
            fuzz_success_dat = json.loads(fuzz_success_data)
            require_param = fuzz_success_dat.keys()
            require_location = []
            require_val = []
            for i in range(len(require_param) - 1):
                require_location.append(int(float(list(fuzz_success_dat[list(require_param)[i]])[-1])))
                require_val.append(''.join(list(fuzz_success_dat[list(require_param)[i]])[:-1]))
            url, headers, data = make_url().make(url, require_location, list(require_param), require_val, headers, data)
        else:
            no_optional_fuzz_cases = eval(random.choice(fuzz_pool.sscan(str(id))[1]))
            for q in no_optional_fuzz_cases.keys():
                pa_names.append(q)
                pa_locations.append(int(list(no_optional_fuzz_cases[q])[-1]))
                value = ''.join(list(no_optional_fuzz_cases[q])[:-1])
                value_fuzzs.append(value)
            url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            pa_locations.clear()
            pa_names.clear()
            value_fuzzs.clear()

    for i in range(len(fuzz_cases)):
        if i + 1 == fuzz_test_times:
            break
        fuzz_case = fuzz_cases[i]
        # dict: fuzz_case = {'name': 'dss2', 'id': '16540'}
        fuzz_case = eval(fuzz_case)
        for q in fuzz_case.keys():
            pa_names.append(q)
            pa_locations.append(int(list(fuzz_case[q])[-1]))
            value = ''.join(list(fuzz_case[q])[:-1])
            value_fuzzs.append(value)
        if Authorization != None:
            headers.update({"Authorization": Authorization})
        else:
            headers = {}
        urll, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
        if method == 'post':
            response = requests.post(url=urll, headers=headers, data=data)
        if method == 'put':
            response = requests.put(url=urll, headers=headers, data=data)
        if method == 'patch':
            response = requests.patch(url=urll, headers=headers, data=data)
        if method == 'get':
            response = requests.get(url=urll, headers=headers, data=data)
        if method == 'delete':
            response = requests.delete(url=urll, headers=headers, data=data)

        if response != None:
            try:
                response_json = response.json()
                response_parse().json_txt(matr, tag, response_json)
                # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                if ini_coverage_rate_executed_code == 1000:
                    pass
                else:
                    time.sleep(2)
                    now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                    if not now_coverage_rate_executed_code:
                        chongqi = requests.get('http://10.177.74.168:5000/restart')
                        if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                            print('重启成功~~~~')
                        else:
                            notify()
                    '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                    if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                        # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                        fuzz_success_json_data = json.dumps(fuzz_case)
                        save_success_case().save_fuzz_success(matr, tag, fuzz_success_json_data, method)
            except ValueError:
                print("NOT JSON")
        else:
            pass
        try:
            print(response.json())
        except ValueError:
            print("NOT JSON")


