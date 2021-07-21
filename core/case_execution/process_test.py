import json
import os
import random
import time
from configparser import ConfigParser
from fnmatch import fnmatch

import redis
import requests
from core.case_execution.config import TestingConfig
from module.Coverage_get_tool import GetCoverage
from module.get_success_case import get_success_case
from module.make_url import make_url
from module.notify import notify
from module.object_handle import fuzz_object
from module.response_parse import response_parse
from module.save_success_case import save_success_case
from module.type_fuzz import fuzz
from log.get_logging import Log

testingConfig = TestingConfig()

config = ConfigParser()
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
config.read(path, encoding='UTF-8')


def restart_coverage_tool(now_coverage_rate_executed_code, restart_url):
    """
    restart coverage tool if coverage is down
    """
    if not now_coverage_rate_executed_code:
        response = requests.get(restart_url)
        if 'The coverage tool is not running The coverage tool is running ,PID is' in response:
            print('重启成功~~~~')
        else:
            notify()


def request_by_different_methods(method, url, headers, data):
    """
    request_by_different_methods
    """
    if method == 'post':
        response = requests.post(url=url, headers=headers, data=data)
    if method == 'put':
        response = requests.put(url=url, headers=headers, data=data)
    if method == 'patch':
        response = requests.patch(url=url, headers=headers, data=data)
    if method == 'get':
        response = requests.get(url=url, headers=headers, data=data)
    if method == 'delete':
        response = requests.delete(url=url, headers=headers, data=data)
    return response


def process_no_optional_fuzz_cases(no_optional_fuzz_cases, pa_names, pa_locations, value_fuzzs):
    """
    process_no_optional_fuzz_cases
    """
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
        if not isinstance(value, int) and not isinstance(value, bool) and value != None:
            print(1)
            try:
                value = json.loads(value)
            except:
                print("obj")
        value_fuzzs.append(value)
    return no_optional_fuzz_cases, pa_names, pa_locations, value_fuzzs


def set_auth(authorization, headers, username, password):
    """
    set_auth
    """
    if authorization:
        headers.update({"Authorization": authorization})
        headers.update({'username': username})
        headers.update({'password': password})


def do_request(url, pa_locations, pa_names, value_fuzzs, headers, data, method):
    """
    request by different parameters
    """
    url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
    response = request_by_different_methods(method, url, headers, data)
    return response


db_params = int(config.get('redis', 'db_params'))
db_success = int(config.get('redis', 'db_success'))
db_parallelism = int(config.get('redis', 'db_parallelism'))
db_fuzz_pool = int(config.get('redis', 'db_fuzz_pool'))
db_serial = int(config.get('redis', 'db_serial'))
db_o = int(config.get('redis', 'db_o'))
redis_host = config.get('redis', 'host')
redis_port = config.get('redis', 'port')
need_coverage = int(config.get('operation_mode', 'need_coverage'))
db_statistics = int(config.get('redis', 'db_statistics'))

params_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_params, decode_responses=True)
success_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_success, decode_responses=True)
fuzz_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_fuzz_pool, decode_responses=True)
flag = redis.StrictRedis(host=redis_host, port=redis_port, db=db_o, decode_responses=True)
statistics = redis.StrictRedis(host=redis_host, port=redis_port, db=db_statistics, decode_responses=True)


def test(operation_mode, cov_url, restart_url, nums, api_info, Authorization, username, password, cases):
    global data
    ini_coverage_rate_executed_code = 1000
    request_log = Log('request.log')
    post_failed_log = Log('post_failed.log')
    post_success_log = Log('post_success.log')
    get_success_log = Log('get_success.log')
    get_failed_log = Log('post_failed.log')
    statistics.setnx('success_request_number', 0)
    statistics.setnx('total_request_number', 0)
    statistics.setnx('failed_request_number', 0)
    statistics.setnx('status_code_5xx_num', 0)
    statistics.setnx('status_code_4xx_num', 0)
    statistics.setnx('status_code_2xx_num', 0)
    total_request_number = int(statistics.get('total_request_number'))
    success_request_number = int(statistics.get('success_request_number'))
    failed_request_number = int(statistics.get('failed_request_number'))
    status_code_5xx_num = int(statistics.get('status_code_5xx_num'))
    status_code_4xx_num = int(statistics.get('status_code_4xx_num'))
    status_code_2xx_num = int(statistics.get('status_code_2xx_num'))

    if operation_mode == 0:
        if need_coverage == 1:
            ini_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
            print(ini_coverage_rate_executed_code)
            restart_coverage_tool(ini_coverage_rate_executed_code, restart_url)
            if need_coverage == 1:
                ini_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                print(ini_coverage_rate_executed_code)
                if not ini_coverage_rate_executed_code:
                    chongqi = requests.get(restart_url)
                    if 'The coverage tool is not running The coverage tool is running ,PID is' in chongqi:
                        print('重启成功~~~~')
                    else:
                        notify()
    headers = {}
    data = {}
    for request_param in api_info.req_param:
        if request_param.location == 3 and request_param.field_type == "array":
            data = []
    pa_locations = []
    pa_names = []
    value_fuzzs = []
    id = api_info.api_id
    url = api_info.path
    method = api_info.http_method

    if nums != 0:
        # 从必选参数fuzz成功的case中取case加入到optional的fuzz case中
        fuzz_success_data = get_success_case().get_fuzz_success(testingConfig.success_pool, method)
        if fuzz_success_data is not None:
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
                        if testingConfig.params_pool.llen(str(field_info.field_name)) != 0:
                            length = testingConfig.params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = testingConfig.params_pool.lindex(str(field_info.field_name), index)
                        else:
                            value = fuzz(field_info.field_type)
                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
                    elif field_info.field_type == 'object' and field_info.object is not None:
                        if testingConfig.params_pool.llen(str(field_info.field_name)) != 0:
                            length = testingConfig.params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = testingConfig.params_pool.lindex(str(field_info.field_name), index)
                        else:
                            dic = fuzz_object().object_handle(field_info.object)
                            value = json.dumps(dic)
                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
                    else:
                        if testingConfig.params_pool.llen(str(field_info.field_name)) != 0:
                            length = testingConfig.params_pool.llen(str(field_info.field_name))
                            index = random.randint(0, length)
                            value = testingConfig.params_pool.lindex(str(field_info.field_name), index)
                        else:
                            if field_info.array == 'string' or field_info.array == 'integer' \
                                    or field_info.array == 'boolean':
                                value = []
                                value.append(fuzz(field_info.array))
                            else:
                                value = [{"name": "linjiaxian", "type": "human", "age": 18}, {"id": 100, "cloud_id": 2}]
                        no_optional_fuzz_cases[str(field_info.field_name)] = str(value) + str(field_info.location)
            no_optional_fuzz_cases, pa_names, pa_locations, value_fuzzs = process_no_optional_fuzz_cases(
                no_optional_fuzz_cases,
                pa_names,
                pa_locations,
                value_fuzzs)
            for q in no_optional_fuzz_cases.keys():
                pa_names.append(q)
                pa_locations.append(int(list(no_optional_fuzz_cases[q])[-1]))
                value = ''.join(list(no_optional_fuzz_cases[q])[:-1])
                try:
                    value = eval(value)
                except:
                    pass
                if not isinstance(value, int) and not isinstance(value, bool) and value is not None:
                    try:
                        value = json.loads(value)
                    except:
                        pass
                value_fuzzs.append(value)
            url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            pa_locations.clear()
            pa_names.clear()
            value_fuzzs.clear()
        # print("组装完成！！！！！！！！！！！！！！！！！！")
    fuzz__cases = []

    if nums == 0:
        if len(cases) != 0:
            for fuzz_case in cases:
                url = api_info.path
                fuzz_case = eval(fuzz_case)
                # print(fuzz_case)
                for q in fuzz_case.keys():
                    pa_names.append(q)
                    pa_locations.append(int(list(fuzz_case[q])[-1]))
                    value = ''.join(list(fuzz_case[q])[:-1])
                    try:
                        value = eval(value)
                    except:
                        pass
                    if not isinstance(value, int) and not isinstance(value, bool) and value != None:
                        try:
                            value = json.loads(value)
                        except:
                            pass
                    value_fuzzs.append(value)
                if Authorization:
                    headers.update({"Authorization": Authorization})
                    # headers.update({'username': username})
                    # headers.update({'password': password})
                url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
                pa_locations.clear()
                pa_names.clear()
                value_fuzzs.clear()
                # request_log.info(
                #     f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'")
                try:
                    if method == 'post':
                        response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'put':
                        response = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'patch':
                        response = requests.patch(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'get':
                        response = requests.get(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'delete':
                        response = requests.delete(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                except:
                    request_log.warning(
                        f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                    response = None
                total_request_number = total_request_number + 1
                statistics.set("total_request_number", total_request_number)
                if response is not None:
                    try:
                        response_json = response.json()
                        response_parse().json_txt(params_pool, response_json)
                        # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                        if ini_coverage_rate_executed_code == 1000:
                            pass
                        else:
                            time.sleep(2)
                            if need_coverage == 1:
                                now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                                restart_coverage_tool(now_coverage_rate_executed_code, restart_url)
                                '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                                if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                                    fuzz_case.update({'api_id': str(id)})
                                    fuzz_success_json_data = json.dumps(fuzz_case)
                                    save_success_case().save_fuzz_success(testingConfig.success_pool,
                                                                          fuzz_success_json_data, method)
                    except ValueError:
                        print("NOT JSON")
                    try:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                        )
                    except:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response}\n\n'
                        )
                    if response.status_code is not None:
                        if fnmatch(str(response.status_code), "5*"):
                            request_log.error(
                                f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                            status_code_5xx_num += 1
                            statistics.set('status_code_5xx_num', status_code_5xx_num)
                        elif fnmatch(str(response.status_code), "4*"):
                            status_code_4xx_num += 1
                            statistics.set('status_code_4xx_num', status_code_4xx_num)
                        elif fnmatch(str(response.status_code), "2*"):
                            status_code_2xx_num += 1
                            statistics.set('status_code_2xx_num', status_code_2xx_num)
                            flag = 0
                            try:
                                response.json()
                            except:
                                flag = 1
                                print(response)
                            if flag == 0:
                                if 'status' in response.json():
                                    if response.json()["status"] == "SUCCESS":
                                        success_request_number += 1
                                        statistics.set('success_request_number', success_request_number)
                                        statistics.sadd(str(method.upper()) + "_SUCCESS", str(id))
                                        if method == 'post':
                                            post_success_log.info(
                                                f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                                f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                            )
                                    elif response.json()["status"] == "FAILED":
                                        failed_request_number += 1
                                        statistics.set('failed_request_number', failed_request_number)
                                        statistics.sadd(str(method.upper()) + "_FAILED", str(id))
                                        if method == 'post':
                                            post_failed_log.info(
                                                f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                                f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                            )
                    data.clear()
                    headers.clear()
        else:
            if Authorization:
                headers.update({"Authorization": Authorization})
                # headers.update({'username': username})
                # headers.update({'password': password})
            url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            # request_log.info(
            #     f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'")
            try:
                if method == 'post':
                    response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'put':
                    response = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'patch':
                    response = requests.patch(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'get':
                    response = requests.get(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'delete':
                    response = requests.delete(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
            except:
                request_log.warning(
                    f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                response = None
            total_request_number = total_request_number + 1
            statistics.set("total_request_number", total_request_number)
            if response is not None:
                try:
                    response_json = response.json()
                    response_parse().json_txt(testingConfig.params_pool, response_json)
                    # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                    if ini_coverage_rate_executed_code == 1000:
                        pass
                    else:
                        time.sleep(2)
                        if need_coverage == 1:
                            now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                            restart_coverage_tool(now_coverage_rate_executed_code, restart_url)
                except ValueError:
                    print("NOT JSON")
                    try:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                        )
                    except:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response}\n\n'
                        )
                if response.status_code is not None:
                    if fnmatch(str(response.status_code), "5*"):
                        request_log.error(
                            f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                        status_code_5xx_num += 1
                        statistics.set('status_code_5xx_num', status_code_5xx_num)
                    elif fnmatch(str(response.status_code), "4*"):
                        status_code_4xx_num += 1
                        statistics.set('status_code_4xx_num', status_code_4xx_num)
                    elif fnmatch(str(response.status_code), "2*"):
                        status_code_2xx_num += 1
                        statistics.set('status_code_2xx_num', status_code_2xx_num)
                        flag = 0
                        try:
                            response.json()
                        except:
                            flag = 1
                            print(response)
                        if flag == 0:
                            if 'status' in response.json():
                                if response.json()["status"] == "SUCCESS":
                                    success_request_number += 1
                                    statistics.set('success_request_number', success_request_number)
                                    statistics.sadd(str(method.upper()) + "_SUCCESS", str(id))
                                    if method == 'post':
                                        post_success_log.info(
                                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                        )
                                elif response.json()["status"] == "FAILED":
                                    failed_request_number += 1
                                    statistics.set('failed_request_number', failed_request_number)
                                    statistics.sadd(str(method.upper()) + "_FAILED", str(id))
                                    if method == 'post':
                                        post_failed_log.info(
                                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                        )
            data.clear()
            headers.clear()
    else:
        if len(cases) != 0:
            # print("有参数")
            for fuzz_case in cases:
                if len(eval(fuzz_case)) == nums:
                    fuzz__cases.append(fuzz_case)
            for fuzz_case in fuzz__cases:
                fuzz_case = eval(fuzz_case)
                url = api_info.path
                for q in fuzz_case.keys():
                    pa_names.append(q)
                    pa_locations.append(int(list(fuzz_case[q])[-1]))
                    value = ''.join(list(fuzz_case[q])[:-1])
                    try:
                        value = eval(value)
                    except:
                        print("str")
                    if not isinstance(value, int) and not isinstance(value, bool) and value != None:
                        try:
                            value = json.loads(value)
                        except:
                            print("obj")
                    value_fuzzs.append(value)
                if Authorization:
                    headers.update({"Authorization": Authorization})
                    # headers.update({'username': username})
                    # headers.update({'password': password})
                url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
                # request_log.info(
                #     f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'")
                try:
                    if method == 'post':
                        response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'put':
                        response = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'patch':
                        response = requests.patch(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'get':
                        response = requests.get(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                    if method == 'delete':
                        response = requests.delete(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                except:
                    request_log.warning(
                        f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                    response = None
                total_request_number = total_request_number + 1
                statistics.set("total_request_number", total_request_number)
                if response is not None:
                    try:
                        response_json = response.json()
                        response_parse().json_txt(params_pool, response_json)
                        # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                        if ini_coverage_rate_executed_code == 1000:
                            pass
                        else:
                            time.sleep(2)
                            if need_coverage == 1:
                                now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                                restart_coverage_tool(now_coverage_rate_executed_code, restart_url)
                                '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
                                if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                                    fuzz_case.update({'api_id': str(id)})

                                    fuzz_success_json_data = json.dumps(fuzz_case)
                                    save_success_case().save_fuzz_optional_success(testingConfig.success_pool,
                                                                                   fuzz_success_json_data,
                                                                                   method)
                    except ValueError:
                        print("NOT JSON")
                    try:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                        )
                    except:
                        request_log.info(
                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                            f'Received: \'HTTP/1.1 {response.status_code} response : {response}\n\n'
                        )
                    if response.status_code is not None:
                        if fnmatch(str(response.status_code), "5*"):
                            request_log.error(
                                f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                            status_code_5xx_num += 1
                            statistics.set('status_code_5xx_num', status_code_5xx_num)
                        elif fnmatch(str(response.status_code), "4*"):
                            status_code_4xx_num += 1
                            statistics.set('status_code_4xx_num', status_code_4xx_num)
                        elif fnmatch(str(response.status_code), "2*"):
                            status_code_2xx_num += 1
                            statistics.set('status_code_2xx_num', status_code_2xx_num)
                            flag = 0
                            try:
                                response.json()
                            except:
                                flag = 1
                                print(response)
                            if flag == 0:
                                if 'status' in response.json():
                                    if response.json()["status"] == "SUCCESS":
                                        success_request_number += 1
                                        statistics.set('success_request_number', success_request_number)
                                        statistics.sadd(str(method.upper()) + "_SUCCESS", str(id))
                                        if method == 'post':
                                            post_success_log.info(
                                                f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                                f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                            )
                                    elif response.json()["status"] == "FAILED":
                                        failed_request_number += 1
                                        statistics.set('failed_request_number', failed_request_number)
                                        statistics.sadd(str(method.upper()) + "_FAILED", str(id))
                                        if method == 'post':
                                            post_failed_log.info(
                                                f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                                f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                            )
            data.clear()
            headers.clear()
        else:
            # print("无参数！！！！！！！！！！！！！！")
            if Authorization:
                headers.update({"Authorization": Authorization})
                # headers.update({'username': username})
                # headers.update({'password': password})
            else:
                pass
            url, headers, data = make_url().make(url, pa_locations, pa_names, value_fuzzs, headers, data)
            # request_log.info(
            #     f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'")
            try:
                if method == 'post':
                    response = requests.post(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'put':
                    response = requests.put(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'patch':
                    response = requests.patch(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'get':
                    response = requests.get(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
                if method == 'delete':
                    response = requests.delete(url=url, headers=headers, data=json.dumps(data), timeout=(300, 300))
            except:
                request_log.warning(
                    f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'")
                response = None
            total_request_number = total_request_number + 1
            statistics.set("total_request_number", total_request_number)
            if response is not None:
                try:
                    response_json = response.json()
                    response_parse().json_txt(testingConfig.params_pool, response_json)
                    # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                    if ini_coverage_rate_executed_code == 1000:
                        pass
                    else:
                        time.sleep(2)
                        if need_coverage == 1:
                            now_coverage_rate_executed_code = GetCoverage().getCoverage_rate_executed_code(cov_url)
                            restart_coverage_tool(now_coverage_rate_executed_code, restart_url)
                except ValueError:
                    print("NOT JSON")
                try:
                    request_log.info(
                        f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                        f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                    )
                except:
                    request_log.info(
                        f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                        f'Received: \'HTTP/1.1 {response.status_code} response : {response}\n\n'
                    )
                if response.status_code is not None:
                    if fnmatch(str(response.status_code), "5*"):
                        request_log.error(
                            f"Sending: \'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data}\'\n")
                        status_code_5xx_num += 1
                        statistics.set('status_code_5xx_num', status_code_5xx_num)
                    elif fnmatch(str(response.status_code), "4*"):
                        status_code_4xx_num += 1
                        statistics.set('status_code_4xx_num', status_code_4xx_num)
                    elif fnmatch(str(response.status_code), "2*"):
                        status_code_2xx_num += 1
                        statistics.set('status_code_2xx_num', status_code_2xx_num)
                        flag = 0
                        try:
                            response.json()
                        except:
                            flag = 1
                            print(response)
                        if flag == 0:
                            if 'status' in response.json():
                                if response.json()["status"] == "SUCCESS":
                                    success_request_number += 1
                                    statistics.set('success_request_number', success_request_number)
                                    statistics.sadd(str(method.upper()) + "_SUCCESS", str(id))
                                    if method == 'post':
                                        post_success_log.info(
                                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                        )
                                elif response.json()["status"] == "FAILED":
                                    failed_request_number += 1
                                    statistics.set('failed_request_number', failed_request_number)
                                    statistics.sadd(str(method.upper()) + "_FAILED", str(id))
                                    if method == 'post':
                                        post_failed_log.info(
                                            f'{method.upper()} {api_info.path} {url} API_id:{id} header:{headers}  data:{data} \n'
                                            f'Received: \'HTTP/1.1 {response.status_code} response : {response.json()}\n\n'
                                        )
            data.clear()
            headers.clear()