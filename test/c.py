import random
import time
import requests
import redis
from rest_framework.utils import json
import sys
import numpy as np
from module.Coverage_get_tool import GetCoverage
from module.Combination import Combination

graph = []
api_info_list = []

###########################      连接redis-pool      ##############################

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# req = redis.StrictRedis(connection_pool=pool)
resp = redis.StrictRedis(connection_pool=pool)

post = redis.StrictRedis(connection_pool=pool)
post.lpush('api_id_p', '')
delete = redis.StrictRedis(connection_pool=pool)
delete.lpush('api_id_d', '')
fuzz_success = redis.StrictRedis(connection_pool=pool)
fuzz_success.lpush('success!!!success!!!success!!!', '')

#################################     模糊处理    ##################################
def fuzz(type):
    if 'integer' == type:
        # sys.maxsize整数最大值9223372036854775807， 整数最小值为-sys.maxsize-1 -9223372036854775808
        # sys.float_info.max float最大值为2.2250738585072014e-308 ,sys.float_info.min float最大值为1.7976931348623157e+308
        list_integer = [1, 2, 0, 3, -45, -51, -82,
                        sys.maxsize, -sys.maxsize - 1, sys.float_info.max, sys.float_info.min]

        return random.choice(list_integer)
    elif 'string' == type:
        # 我就随便写写，我也不知道写啥。。。
        list_string = ['3171261@qq.com', 'CommonLisp', 'Concrete5', 'John Doe',
                       'https://gitlab.example.com/api/v4/templates/gitignores/Ruby',
                       '# This file is a template, and might need editing',
                       '!@@#$$%%%^^^',
                       '(^&%GBH#T$G"""""""""""DFHBD"BDGVDFVWEF$$53346542@##@$#@%$##',
                       '2012-10-22T14:13:35Z',
                       'PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/groups/:id/access_requests',
                       '/uploads/-/system/appearance/logo/1/logo.png',
                       '#e75e40', '#ffffff', 'logo=@/path/to/logo.png',
                       '5832fc6e14300a0d962240a8144466eef4ee93ef0d218477e55f11cf12fc3737'
                       'ee1dd64b6adc89cf7e2c23099301ccc2c61b441064e9324d963c46902a85ec34',
                       '127.0.0.1', 'hello@flightjs.com']

        return random.choice(list_string)
    elif 'boolean' == type:
        list_boolean = ['False', 'True']
        return random.choice(list_boolean)

########################   遍历json文件所有的key以及对应的value  #######################

def json_txt(dic_json):
    if isinstance(dic_json, list):
        for dic in dic_json:
            if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic:
                    if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                        json_txt(dic[key])
                        resp.lpush(str(key), str(dic[key]))
                    else:
                        resp.lpush(str(key), str(dic[key]))
    else:
        if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
            for key in dic_json:
                if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                    json_txt(dic_json[key])
                    resp.lpush(str(key), str(dic_json[key]))
                else:
                    resp.lpush(str(key), str(dic_json[key]))

#############################   对应object类型和array类型    ########################

object_dic = {}
def option_object(objects):
    if objects:
        i = 1
        for obj in objects:
            if obj.type == 'array':
                if isinstance(obj, list):
                    i = i + 1
                    option_array(obj.object)
                else:
                    pass
            elif obj.type == 'object':
                i = i + 1
                option_object(obj.object)
            else:
                object_dic[obj.name] = obj.type + str(i)

array_dic = {}
def option_array(array):
    if array:
        i = 1
        for arr in array:
            if arr.type == 'array':
                if isinstance(arr, list):
                    i = i + 1
                    option_array(arr.object)
                else:
                    pass
            elif arr.type == 'object':
                i = i + 1
                option_object(arr.object)
            else:
                array_dic[arr.name] = arr.type + str(i)

################################    测试    ########################################

def get_optional_param(api_info):
    optional = []
    for field_info in api_info.req_param:
        if not field_info.require:
            if field_info.field_type == 'string' or field_info.field_type == 'integer' or field_info.field_type == 'boolean':
                location = field_info.location
                a = {}
                a[field_info.field_name + str(location)] = field_info.field_type
                optional.append(a)
                a.clear()
            elif field_info.field_type == 'object':
                option_object(field_info.object)
                object = object_dic
                object_dic.clear()
                optional.append(object)
            elif field_info.field_type == 'array':
                option_array(field_info.array)
                arr = array_dic
                array_dic.clear()
                optional.append(arr)
    return optional

def post_fuzz_test(api_info,ini_coverage_rate_executed_code,cov_url):
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
        '''Redis存储post过的api_id'''
        post.lpush('api_id_p', api_info.api_id)
        # '''配置token'''
        # if '?' in url:
        #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        # else:
        #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        print('fuzz  ' + str(api_info.api_id) + ' post ' + url)
        response = requests.post(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到MySQL数据库中
            time.sleep(2)
            now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
            '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
            if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

def post_fuzz_test_optional(api_info,ini_coverage_rate_executed_code):
    optional = get_optional_param(api_info)
    end_list = Combination.get_combine(Combination, optional)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    for optional_param in end_list:
        optional_param = list(optional_param)
        for param in optional_param:
            a = param.keys()
            location = a[-1]
            para_name = a[:-1]
            if location == 0:
                url = url.replace('{' + para_name + '}', str(param.values()))
            elif location == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(para_name) + "=" + str(param.values())
                else:
                    url = url + "&" + str(para_name) + "=" + str(param.values())
            elif location == 2:
                headers[str(para_name)] = str(param.values())
            elif location == 3:
                # 参数组成json字符串 ==> data
                data[str(para_name)] = str(param.values())
            fuzz_success_data[str(para_name)] = str(param.values()) + str(location)
        print('fuzz  ' + str(api_info.api_id) + ' post ' + url)
        response = requests.post(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功，将测试用例保存到MySQL数据库中
            if response.status_code == '200':
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

def delete_fuzz_test(api_info,ini_coverage_rate_executed_code):
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            post.lrem('api_id_p', api_info.api_id, 0)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"

            print('fuzz  ' + str(api_info.api_id) + ' delete ' + url)
            response = requests.delete(url=url, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功，将测试用例保存到MySQL数据库中
                if response.status_code == '200':
                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                    fuzz_success_json_data = json.dumps(fuzz_success_data)
                    fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                    fuzz_success_data.clear()
            else:
                pass
            print(response.json())

def delete_fuzz_test_optional(api_info,ini_coverage_rate_executed_code):
    optional = get_optional_param(api_info)
    end_list = Combination.get_combine(Combination, optional)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    for optional_param in end_list:
        list(optional_param)
        for param in optional_param:
            a = param.keys()
            location = a[-1]
            para_name = a[:-1]
            if location == 0:
                url = url.replace('{' + para_name + '}', str(param.values()))
            elif location == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(para_name) + "=" + str(param.values())
                else:
                    url = url + "&" + str(para_name) + "=" + str(param.values())
            elif location == 2:
                headers[str(para_name)] = str(param.values())
            elif location == 3:
                # 参数组成json字符串 ==> data
                data[str(para_name)] = str(param.values())
            fuzz_success_data[str(para_name)] = str(param.values()) + str(location)
        print('fuzz  ' + str(api_info.api_id) + ' delete ' + url)
        response = requests.delete(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功，将测试用例保存到MySQL数据库中
            if response.status_code == '200':
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

def get_fuzz_test(api_info,ini_coverage_rate_executed_code):
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            print('fuzz  ' + str(api_info.api_id) + ' get ' + url)
            response = requests.get(url=url, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功，将测试用例保存到MySQL数据库中
                if response.status_code == '200':
                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                    fuzz_success_json_data = json.dumps(fuzz_success_data)
                    fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                    fuzz_success_data.clear()
            else:
                pass
            print(response.json())

def get_fuzz_test_optional(api_info,ini_coverage_rate_executed_code):
    optional = get_optional_param(api_info)
    end_list = Combination.get_combine(Combination, optional)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    for optional_param in end_list:
        list(optional_param)
        for param in optional_param:
            a = param.keys()
            location = a[-1]
            para_name = a[:-1]
            if location == 0:
                url = url.replace('{' + para_name + '}', str(param.values()))
            elif location == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(para_name) + "=" + str(param.values())
                else:
                    url = url + "&" + str(para_name) + "=" + str(param.values())
            elif location == 2:
                headers[str(para_name)] = str(param.values())
            elif location == 3:
                # 参数组成json字符串 ==> data
                data[str(para_name)] = str(param.values())
            fuzz_success_data[str(para_name)] = str(param.values()) + str(location)
        print('fuzz  ' + str(api_info.api_id) + ' get ' + url)
        response = requests.get(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功，将测试用例保存到MySQL数据库中
            if response.status_code == '200':
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

def put_fuzz_test(api_info,ini_coverage_rate_executed_code):
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            print('fuzz  ' + str(api_info.api_id) + ' put ' + url)
            response = requests.put(url=url, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功，将测试用例保存到MySQL数据库中
                if response.status_code == '200':
                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                    fuzz_success_json_data = json.dumps(fuzz_success_data)
                    fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                    fuzz_success_data.clear()
            else:
                pass
            print(response.json())

def put_fuzz_test_optional(api_info,ini_coverage_rate_executed_code):
    optional = get_optional_param(api_info)
    end_list = Combination.get_combine(Combination, optional)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    for optional_param in end_list:
        list(optional_param)
        for param in optional_param:
            a = param.keys()
            location = a[-1]
            para_name = a[:-1]
            if location == 0:
                url = url.replace('{' + para_name + '}', str(param.values()))
            elif location == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(para_name) + "=" + str(param.values())
                else:
                    url = url + "&" + str(para_name) + "=" + str(param.values())
            elif location == 2:
                headers[str(para_name)] = str(param.values())
            elif location == 3:
                # 参数组成json字符串 ==> data
                data[str(para_name)] = str(param.values())
            fuzz_success_data[str(para_name)] = str(param.values()) + str(location)
        print('fuzz  ' + str(api_info.api_id) + ' put ' + url)
        response = requests.put(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功，将测试用例保存到MySQL数据库中
            if response.status_code == '200':
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

def patch_fuzz_test(api_info,ini_coverage_rate_executed_code):
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            print('fuzz  ' + str(api_info.api_id) + ' patch ' + url)
            response = requests.patch(url=url, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功，将测试用例保存到MySQL数据库中
                if response.status_code == '200':
                    # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                    fuzz_success_json_data = json.dumps(fuzz_success_data)
                    fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                    fuzz_success_data.clear()
            else:
                pass
            print(response.json())

def patch_fuzz_test_optional(api_info):
    optional = get_optional_param(api_info)
    end_list = Combination.get_combine(Combination, optional)
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    for field_info in api_info.req_param:
        if field_info.require:
            flag = 0
            location = field_info.location
            field_type = field_info.field_type
            if field_type == 'string' or field_type == 'integer' or field_type == 'boolean':
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(val))
                elif location == 1:
                    # url追加?key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(val)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(val)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(val)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(val)
                fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)
            elif field_type == 'object':
                option_object(field_info.object)
                object = {}
                for para_name in object_dic.keys():
                    value_fuzz = fuzz(object_dic[para_name])
                    object[para_name] = value_fuzz
                if location == 2:
                    headers['object'] = object
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['object'] = object
                object_data = json.dumps(object)
                fuzz_success_data['object'] = object_data + str(location)
            else:
                option_array(field_info.array)
                array = {}
                for para_name in array_dic.keys():
                    value_fuzz = fuzz(array_dic[para_name])
                    array[para_name] = value_fuzz
                if location == 2:
                    headers['array'] = array
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data['array'] = array
                array_data = json.dumps(array)
                fuzz_success_data['array'] = array_data + str(location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
    for optional_param in end_list:
        list(optional_param)
        for param in optional_param:
            a = param.keys()
            location = a[-1]
            para_name = a[:-1]
            if location == 0:
                url = url.replace('{' + para_name + '}', str(param.values()))
            elif location == 1:
                # url追加?key1=value1&key2=value2到url后,即查询字符串
                if flag == 0:
                    flag = 1
                    url = url + "?" + str(para_name) + "=" + str(param.values())
                else:
                    url = url + "&" + str(para_name) + "=" + str(param.values())
            elif location == 2:
                headers[str(para_name)] = str(param.values())
            elif location == 3:
                # 参数组成json字符串 ==> data
                data[str(para_name)] = str(param.values())
            fuzz_success_data[str(para_name)] = str(param.values()) + str(location)
        print('fuzz  ' + str(api_info.api_id) + ' patch ' + url)
        response = requests.patch(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功，将测试用例保存到MySQL数据库中
            if response.status_code == '200':
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                fuzz_success.lpush('success!!!success!!!success!!!', fuzz_success_json_data)
                fuzz_success_data.clear()
        else:
            pass
        print(response.json())

# fuzz处理graph（x）位置的api
def fuzzgraph(x, api_info_list, cov_url):
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    api_info = api_info_list[x]
    method = api_info.http_method
    if method == 'post':
        now_reids_fuzz_success_length = fuzz_success.llen()
        post_fuzz_test(api_info,ini_coverage_rate_executed_code,cov_url)
        after_reids_fuzz_success_length = fuzz_success.llen()
        if now_reids_fuzz_success_length != after_reids_fuzz_success_length:
            print('fuzz成功改变了代码覆盖率')
            fuzz_success_json_data = json.loads(fuzz_success.lindex('success!!!success!!!success!!!', 0))  # 字典

        else:
            pass
        post_fuzz_test_optional(api_info,ini_coverage_rate_executed_code)
    elif method == 'delete':
        delete_fuzz_test(api_info,ini_coverage_rate_executed_code)
        delete_fuzz_test_optional(api_info,ini_coverage_rate_executed_code)
    elif method == 'get':
        get_fuzz_test(api_info,ini_coverage_rate_executed_code)
        get_fuzz_test_optional(api_info,ini_coverage_rate_executed_code)
    elif method == 'put':
        put_fuzz_test(api_info,ini_coverage_rate_executed_code)
        put_fuzz_test_optional(api_info,ini_coverage_rate_executed_code)
    else:
        patch_fuzz_test(api_info,ini_coverage_rate_executed_code)
        patch_fuzz_test_optional(api_info,ini_coverage_rate_executed_code)







def topology_visit(g, n, api_info_list, visited, end,queu):
    # 第一个开始节点api是没有依赖的，其中需要的参数可通过fuzz来获取（也可人工赋值）
    visited[n] = 1
    fuzzgraph(n, api_info_list, queu)
    while visited[n] == 1:
        # 创建遍历的存储队列
        dep_list = []
        for i in range(len(g)):
            if g[i][n] != -1:
                dep_list.append(i)
        if len(dep_list) == 0:
            break
        '''略过正常测试用例'''
        if len(dep_list) != 0:  # 说明queue里面所有api都无法test,并且资源池中也没有资源
            k = random.choice(dep_list)
            if visited[k] == 0:
                for a in dep_list:
                    g[a][n] = -1
                dep_list.clear()
                fuzzgraph(k, api_info_list,queu)
                visited[k] = 1
                g[k] = end
                n = k


def traversal(grap, api_info_lis, queu):
    graph = grap
    api_info_list = api_info_lis
    # 创建visited，用来停止遍历，即一旦遇到visited，即刻退出递归 #0代表没被访问
    visited = np.zeros(len(graph)).astype(dtype=int).tolist()
    # print(visited)
    # 记录拓扑排序顺序
    # topology_order = []
    # 记录出度为0的点
    out_degree_zero = []
    # 设计出度为0的点
    end = []
    for i in range(len(graph)):
        end.append(-1)
    # 收集出度为0的点的集合,即无依赖节点的集合
    for j in range(len(graph)):
        if graph[j] == end:
            out_degree_zero.append(j)
    # print(out_degree_zero)

    for m in range(len(out_degree_zero)):
        k = random.choice(out_degree_zero)
        out_degree_zero.remove(k)
        print(k)
        print(end)
        topology_visit(graph, k, api_info_list, visited, end, queu)

    return visited



