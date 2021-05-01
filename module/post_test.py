import ast
import random
import sys
import time

import redis
import requests
from rest_framework.utils import json
from module.Coverage_get_tool import GetCoverage
from module.Combination import Combination

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


# 组装url
def make(url, p_location, p_name, value_fuzz):
    flag = 0
    headers = {}
    data = {}
    for i in range(len(p_location)):
        '''
        不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
        path和query 用url直接请求
        header和body用request.post(url, headers=headers)或requests.post(url, data)
        '''
        if p_location == 0:
            url = url.replace('{' + p_name[i] + '}', str(value_fuzz[i]))
        elif p_location == 1:
            # url追加?key1=value1&key2=value2到url后,即查询字符串
            if flag == 0:
                flag = 1
                url = url + "?" + str(p_name[i]) + "=" + str(value_fuzz[i])
            else:
                url = url + "&" + str(p_name[i]) + "=" + str(value_fuzz[i])
        elif p_location == 2:
            headers[str(p_name[i])] = str(value_fuzz[i])
        elif p_location == 3:
            # 参数组成json字符串 ==> data
            data[str(p_name[i])] = str(value_fuzz[i])
    return url, headers, data

# 一个参数k次覆盖率不变，则结束fuzz
def one_fuzz_k_times(fuzz_success_data, k, parameter, api_id, cov_url, ini_coverage_rate_executed_code,lll):
    if isinstance(parameter,list):
        parameter = str(parameter).replace('[','').replace(']','')
        parameter = ast.literal_eval(parameter)
    for i in range(k):
        p_name = parameter.keys()
        p_type = parameter[p_name][:-1]
        p_location = parameter[p_name][-1]
        value_fuzz = fuzz(p_type)
        fuzz_success_data[str(p_name)] = str(value_fuzz) + str(p_location)
        url, headers, data = make(url, p_location, p_name, value_fuzz)
        print('fuzz  ' + str(api_id) + ' post ' + url)
        response = requests.post(url=url, headers=headers, data=data)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
            time.sleep(2)
            now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
            '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
            if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                if lll == 0:
                    save_post_fuzz_success(fuzz_success_json_data)
                elif lll == 1:
                    save_post_fuzz_optional_success(fuzz_success_json_data)
                fuzz_success_data.clear()
                one_fuzz_k_times(fuzz_success_data, k, parameter, api_id, cov_url, ini_coverage_rate_executed_code)
        else:
            pass
        print(response.json())

# 多个参数k次覆盖率不变，则结束fuzz
def mult_fuzz_k_times(fuzz_success_data, k,c,pa_location,pa_name,value_fuzz ,parameter, api_id, cov_url, ini_coverage_rate_executed_code,lll):
    if isinstance(parameter,list):
        parameter = str(parameter).replace('[','').replace(']','')
        parameter = ast.literal_eval(parameter)
    for i in range(k):
        for pa in c:
            pa_location.append(parameter[pa][-1])
            pa_name.append(pa)
            pa_type = parameter[pa][:-1]
            value_fuzz.append(fuzz(pa_type))
            fuzz_success_data[str(pa_name)] = str(value_fuzz) + str(pa_location)
        global url
        url, headers, data = make(url, pa_location, pa_name, value_fuzz)
        '''Redis存储post过的api_id'''
        post.lpush('api_id_p', api_id)
        # '''配置token'''
        # if '?' in url:
        #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        # else:
        #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        print('fuzz  ' + str(api_id) + ' post ' + url)
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
                if lll == 0:
                    save_post_fuzz_success(fuzz_success_json_data)
                elif lll == 1:
                    save_post_fuzz_optional_success(fuzz_success_json_data)
                fuzz_success_data.clear()
                mult_fuzz_k_times(fuzz_success_data, k,c,pa_location,pa_name,value_fuzz ,parameter, api_id, cov_url, ini_coverage_rate_executed_code)
        else:
            pass
        print(response.json())

def post_fuzz_test(k, api_info, cov_url):
    lll = 0
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    global url
    url = api_info.path
    api_id = api_info.api_id
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    parameter = {}
    for field_info in api_info.req_param:
        if field_info.require:
            parameter[field_info.field_name] = field_info.field_type + str(field_info.location)
    length = len(parameter)
    if length == 1:
        one_fuzz_k_times(fuzz_success_data, k, parameter, api_id, cov_url, ini_coverage_rate_executed_code,lll)
    else:
        a = Combination.get_combine(Combination, parameter.keys())
        for b in a:
            c = list(b)  # c是要改变的参数list
            d = set(parameter.keys())
            e = set(c)
            f = d ^ e
            g = list(f)  # g是不改变的参数list
            pa_location = []
            pa_name = []
            value_fuzz = []
            for pa in g:  # 不变参数确定，反复改变可变参数
                pa_location.append(parameter[pa][-1])
                pa_name.append(pa)
                pa_type = parameter[pa][:-1]
                value_fuzz.append(fuzz(pa_type))
            url, headers, data = make(url, pa_location, pa_name, value_fuzz)    # 不变参数构造完成url
            mult_fuzz_k_times(fuzz_success_data, k, c, pa_location, pa_name, value_fuzz, parameter, api_id, cov_url,
                              ini_coverage_rate_executed_code,lll)

def post_fuzz_test_optional(k, api_info, cov_url):
    lll = 1
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    api_id = api_info.api_id
    global url
    url = api_info.path
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    fuzz_success_json_data = fuzz_success.lindex('post_success!!!!!!',-1)
    fuzz_success_dat = json.loads(str(fuzz_success_json_data))
    if fuzz_success_dat['id'] == api_id:
        require_param = fuzz_success_dat.keys()
        for i in range(len(require_param)):
            i = i + 1  # 因为第一个参数存储了id
            require_location = fuzz_success_dat[require_param[i]][-1]
            require_val = fuzz_success_dat[require_param[i]][:-1]
            url, headers, data, fuzz_success_data = make(url,require_location,require_param[i],require_val)
    optional_parameter = {}
    for field_info in api_info.req_param:
        if not field_info.require:
            optional_parameter[field_info.field_name] = field_info.field_type + str(field_info.location)
    end_list = Combination.get_combine(Combination, optional_parameter)
    for optional_param in end_list:
        optional_param = list(optional_param)
        if optional_param == None:
            pass
        else:
            length = len(optional_param)
            if length == 1:
                one_fuzz_k_times(fuzz_success_data, k, optional_param, api_id, cov_url, ini_coverage_rate_executed_code,lll)
            else:
                a = Combination.get_combine(Combination, optional_param.keys())
                for b in a:
                    cc = list(b)  # c是要改变的参数list
                    c = []
                    for ccc in cc:
                        c.append(ccc.keys())
                    d = []
                    for dd in a:
                        d.append(dd.keys())
                    d = set(d)
                    e = set(c)
                    f = d ^ e
                    g = list(f)  # g是不改变的参数list
                    pa_location = []
                    pa_name = []
                    value_fuzz = []
                    for pa in g:  # 不变参数确定，反复改变可变参数
                        pa_location.append(optional_param[pa][-1])
                        pa_name.append(pa)
                        pa_type = optional_param[pa][:-1]
                        value_fuzz.append(fuzz(pa_type))
                    url, headers, data = make(url, pa_location, pa_name, value_fuzz)  # 不变参数构造完成url
                    mult_fuzz_k_times(fuzz_success_data, k, c, pa_location, pa_name, value_fuzz, optional_param, api_id, cov_url,
                                      ini_coverage_rate_executed_code,lll)

def save_post_fuzz_success(fuzz_success_json_data):
    fuzz_success.lpush('post_success!!!!!!', fuzz_success_json_data)

def save_post_fuzz_optional_success(fuzz_success_json_data):
    fuzz_success.lpush('post_optional_success!!!!!!', fuzz_success_json_data)

