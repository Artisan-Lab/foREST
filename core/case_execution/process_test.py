import json
import random
import time

import requests

from module.Coverage_get_tool import GetCoverage
from module.get_success_case import get_success_case
from module.make_url import make_url
from module.notify import notify
from module.response_parse import response_parse
from module.save_success_case import save_success_case


def test(operation_mode, cov_url, restart, each_process_exc_case_num, nums, params_pool, fuzz_pool, api_info,
         success_pool, Authorization, username, password):
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

    cases = []

    if nums == 0:
        for i in range(each_process_exc_case_num):
            if fuzz_pool.sscan(str(id)) < each_process_exc_case_num:
                for j in list(fuzz_pool.smembers(str(id))):
                    cases.append(j)
                    fuzz_pool.srem(str(id), j)
                break
            else:
                cases.append(fuzz_pool.sscan(str(id))[1][i])
                fuzz_pool.srem(str(id), fuzz_pool.sscan(str(id))[1][i])
    else:
        for i in range(each_process_exc_case_num):
            if fuzz_pool.sscan(str(id) + 'optional') < each_process_exc_case_num:
                for j in list(fuzz_pool.smembers(str(id) + 'optional')):
                    cases.append(j)
                    fuzz_pool.srem(str(id) + 'optional', j)
                break
            else:
                cases.append(fuzz_pool.sscan(str(id) + 'optional')[1][i])
                fuzz_pool.srem(str(id) + 'optional', fuzz_pool.sscan(str(id) + 'optional')[1][i])

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
        for fuzz_case in cases:
            fuzz_case = eval(fuzz_case)
            for q in fuzz_case.keys():
                pa_names.append(q)
                pa_locations.append(int(list(fuzz_case[q])[-1]))
                value = ''.join(list(fuzz_case[q])[:-1])
                value_fuzzs.append(value)
            if Authorization != None:
                headers.update({"Authorization": Authorization})
                headers.update({'username', username})
                headers.update({'password', password})
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
                headers.update({'username', username})
                headers.update({'password', password})
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


