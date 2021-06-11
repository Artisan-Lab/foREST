import json
import os
import random
import time
from configparser import ConfigParser

import redis
import requests

from module.Coverage_get_tool import GetCoverage
from module.get_success_case import get_success_case
from module.make_url import make_url
from module.notify import notify
from module.response_parse import response_parse
from module.save_success_case import save_success_case

config = ConfigParser()
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
config.read(path, encoding='UTF-8')
db_success = int(config.get('redis', 'db_success'))
db_params = int(config.get('redis', 'db_params'))
db_serial = int(config.get('redis', 'db_serial'))
db_parallelism = int(config.get('redis', 'db_parallelism'))
db_fuzz_pool = int(config.get('redis', 'db_fuzz_pool'))
db_o = int(config.get('redis', 'db_o'))
redis_host = config.get('redis', 'host')
redis_port = config.get('redis', 'port')

params_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_params, decode_responses=True)
success_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_success, decode_responses=True)
fuzz_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_fuzz_pool, decode_responses=True)
flag = redis.StrictRedis(host=redis_host, port=redis_port, db=db_o, decode_responses=True)

def test(operation_mode, cov_url, restart, nums, api_info, Authorization, username, password, cases):
    ini_coverage_rate_executed_code = 1000
    if operation_mode == 0:
        ini_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
        print(ini_coverage_rate_executed_code)
        if not ini_coverage_rate_executed_code:
            chongqi = requests.get(restart)
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

    print(cases)

    if nums != 0:
        # 从必选参数fuzz成功的case中取case加入到optional的fuzz case中
        fuzz_success_data = get_success_case().get_fuzz_success(success_pool, method)
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
    fuzz__cases = []

    if nums == 0:
        if len(cases) != 0:
            for fuzz_case in cases:
                fuzz_case = eval(fuzz_case)
                for q in fuzz_case.keys():
                    pa_names.append(q)
                    pa_locations.append(int(list(fuzz_case[q])[-1]))
                    value = ''.join(list(fuzz_case[q])[:-1])
                    value_fuzzs.append(value)
                if Authorization != None:
                    headers.update({"Authorization": Authorization})
                    headers.update({'username': username})
                    headers.update({'password': password})
                else:
                    pass
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
                        response_parse().json_txt(params_pool, response_json)
                        # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                        if ini_coverage_rate_executed_code == 1000:
                            pass
                        else:
                            time.sleep(2)
                            now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                            if not now_coverage_rate_executed_code:
                                chongqi = requests.get(restart)
                                if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                                    print('重启成功~~~~')
                                else:
                                    notify()
                            '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                            if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                                fuzz_case.update({'api_id': str(id)})
                                fuzz_success_json_data = json.dumps(fuzz_case)
                                save_success_case().save_fuzz_success(success_pool, fuzz_success_json_data, method)
                    except ValueError:
                        print("NOT JSON")
                else:
                    pass
                try:
                    print(response.json())
                except ValueError:
                    print("NOT JSON")
        else:
            if Authorization != None:
                headers.update({"Authorization": Authorization})
                headers.update({'username': username})
                headers.update({'password': password})
            else:
                pass
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
                    response_parse().json_txt(params_pool, response_json)
                    # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                    if ini_coverage_rate_executed_code == 1000:
                        pass
                    else:
                        time.sleep(2)
                        now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                        if not now_coverage_rate_executed_code:
                            chongqi = requests.get(restart)
                            if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                                print('重启成功~~~~')
                            else:
                                notify()
                except ValueError:
                    print("NOT JSON")
            else:
                pass
            try:
                print(response.json())
            except ValueError:
                print("NOT JSON")

    else:
        for fuzz_case in cases:
            if len(eval(fuzz_case)) == nums:
                fuzz__cases.append(fuzz_case)
        for fuzz_case in fuzz__cases:
            fuzz_case = eval(fuzz_case)
            for q in fuzz_case.keys():
                pa_names.append(q)
                pa_locations.append(int(list(fuzz_case[q])[-1]))
                value = ''.join(list(fuzz_case[q])[:-1])
                value_fuzzs.append(value)
            if Authorization != None:
                headers.update({"Authorization": Authorization})
                headers.update({'username': username})
                headers.update({'password': password})
            else:
                pass
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
                    response_parse().json_txt(params_pool, response_json)
                    # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                    if ini_coverage_rate_executed_code == 1000:
                        pass
                    else:
                        time.sleep(2)
                        now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                        if not now_coverage_rate_executed_code:
                            chongqi = requests.get(restart)
                            if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                                print('重启成功~~~~')
                            else:
                                notify()
                        '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                        if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                            # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                            fuzz_case.update({'api_id': str(id)})

                            fuzz_success_json_data = json.dumps(fuzz_case)
                            save_success_case().save_fuzz_optional_success(success_pool, fuzz_success_json_data,method)
                except ValueError:
                    print("NOT JSON")
            else:
                pass
            try:
                print(response.json())
            except ValueError:
                print("NOT JSON")
        fuzz__cases.clear()

