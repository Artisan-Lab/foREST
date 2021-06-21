import json
import os
import random
import time
from configparser import ConfigParser

import redis
import requests

from core.case_generation.generate import case_generation
from module.Coverage_get_tool import GetCoverage
from module.get_success_case import get_success_case
from module.make_url import make_url
from module.notify import notify
from module.object_handle import fuzz_object
from module.response_parse import response_parse
from module.save_success_case import save_success_case
from module.type_fuzz import fuzz

config = ConfigParser()
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
config.read(path, encoding='UTF-8')

db_params = int(config.get('redis', 'db_params'))
db_success = int(config.get('redis', 'db_success'))
db_parallelism = int(config.get('redis', 'db_parallelism'))
db_fuzz_pool = int(config.get('redis', 'db_fuzz_pool'))
db_serial = int(config.get('redis', 'db_serial'))
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
            no_optional_fuzz_cases = {}
            for field_info in api_info.req_param:
                if field_info.require:
                    if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                            or field_info.field_type == 'boolean':
                        if params_pool.llen(str(field_info.field_name)) != 0:
                            length = params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = params_pool.lindex(str(field_info.field_name), index)
                        else:
                            value = fuzz(field_info.field_type)
                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
                    elif field_info.field_type == 'object' and field_info.object != None:
                        if params_pool.llen(str(field_info.field_name)) != 0:
                            length = params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = params_pool.lindex(str(field_info.field_name), index)
                        else:
                            dic = fuzz_object.object_handle(field_info.object)
                            value = json.dumps(dic)
                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
                    else:
                        if params_pool.llen(str(field_info.field_name)) != 0:
                            length = params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = params_pool.lindex(str(field_info.field_name), index)
                        else:
                            value = []
                            value.append(fuzz(field_info.array))

                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
            for q in no_optional_fuzz_cases.keys():
                pa_names.append(q)
                pa_locations.append(int(list(no_optional_fuzz_cases[q])[-1]))
                value = ''.join(list(no_optional_fuzz_cases[q])[:-1])
                print(value)
                print(type(value))
                try:
                    value = eval(value)
                except:
                    print("str")
                print(value)
                print(type(value))
                if not isinstance(value, int) and not isinstance(value, bool)and value != None:
                    print(1)
                    try:
                        value = json.loads(value)
                    except:
                        print("obj")
                value_fuzzs.append(value)
            url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            pa_locations.clear()
            pa_names.clear()
            value_fuzzs.clear()
        print("组装完成！！！！！！！！！！！！！！！！！！")
    fuzz__cases = []

    if nums == 0:
        if len(cases) != 0:
            for fuzz_case in cases:
                fuzz_case = eval(fuzz_case)
                for q in fuzz_case.keys():
                    pa_names.append(q)
                    pa_locations.append(int(list(fuzz_case[q])[-1]))
                    value = ''.join(list(fuzz_case[q])[:-1])
                    print(value)
                    print(type(value))
                    try:
                        value = eval(value)
                    except:
                        print("str")
                    print(value)
                    print(type(value))
                    if not isinstance(value, int) and not isinstance(value, bool)and value != None:
                        try:
                            value = json.loads(value)
                        except:
                            print("obj")
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
        if len(cases) != 0:
            print("有参数")
            for fuzz_case in cases:
                if len(eval(fuzz_case)) == nums:
                    fuzz__cases.append(fuzz_case)
            print(f"params//aaa////{cases}//aaa////{fuzz__cases}")
            for fuzz_case in fuzz__cases:
                fuzz_case = eval(fuzz_case)
                for q in fuzz_case.keys():
                    pa_names.append(q)
                    pa_locations.append(int(list(fuzz_case[q])[-1]))
                    value = ''.join(list(fuzz_case[q])[:-1])
                    print(value)
                    print(type(value))
                    try:
                        value = eval(value)
                    except:
                        print("str")
                    print(value)
                    print(type(value))
                    if not isinstance(value, int) and not isinstance(value, bool) and value != None:
                        print(1)
                        try:
                            value = json.loads(value)
                        except:
                            print("obj")
                    value_fuzzs.append(value)
                if Authorization != None:
                    headers.update({"Authorization": Authorization})
                    headers.update({'username': username})
                    headers.update({'password': password})
                else:
                    pass
                print(f"url//0/{url}/// pa_locations///1//{pa_locations}///"
                      f"////pa_names/////{pa_names}//// value_fuzzs//////{value_fuzzs}///headers///4//{headers}//data//{data}")
                urll, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
                print(f"url是{urll}////id///{id}method/////{method}////header///{headers}/////data////{data}")
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
        else:
            print("无参数！！！！！！！！！！！！！！")
            if Authorization != None:
                headers.update({"Authorization": Authorization})
                headers.update({'username': username})
                headers.update({'password': password})
            else:
                pass
            urll, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            print(f"url是{urll}id///{id}method/////{method}")
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

