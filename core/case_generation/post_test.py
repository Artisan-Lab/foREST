import random
import sys
import time
import ast

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
def make(url, p_location, p_name, value_fuzz, headers, data):
    flag = 0
    for i in range(len(p_location)):
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
def one_fuzz_k_times(fuzz_success_data, k, parameter,url , api_id, cov_url, ini_coverage_rate_executed_code,lll):
    for i in range(k):
        for i in parameter.keys():
            p_name = str(i)
            print(p_name)
            p_type = ''.join(list(parameter[p_name])[:-1])
            p_location = []
            p_location.append(int(list(parameter[p_name])[-1]))
            value_fuzz = fuzz(p_type)
            fuzz_success_data[str(p_name)] = str(value_fuzz) + str(p_location)
            # '''配置token'''
            # if '?' in url:
            #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            # else:
            #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            headers = {}
            data = {}
            urll, headers, data = make(url, p_location, p_name, value_fuzz,headers, data)
            print('fuzz  ' + str(api_id) + ' post ' + urll)
            response = requests.post(url=urll, headers=headers, data=data)
            if response != None:
                response_json = response.json()
                json_txt(response_json)
                # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到redis中
                time.sleep(2)
                now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
                if not now_coverage_rate_executed_code:
                    pass
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
def mult_fuzz_k_times(fuzz_success_data, k, d, url, headers, data, api_id, cov_url, ini_coverage_rate_executed_code,lll):
    for i in range(k):
        h = headers
        da = data
        pa_location = []
        pa_name = []
        value_fuzz = []
        for pa in d.keys():
            pa_location.append(int(list(d[pa])[-1]))
            pa_name.append(pa)
            pa_type = ''.join(list(d[pa])[:-1])
            value_fuzz.append(fuzz(pa_type))
            fuzz_success_data[str(pa_name)] = str(value_fuzz) + str(pa_location)
        url, header, dat = make(url, pa_location, pa_name, value_fuzz, h, da)
        # '''配置token'''
        # if '?' in url:
        #     url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        # else:
        #     url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        print('fuzz  ' + str(api_id) + ' post ' + url)
        response = requests.post(url=url, headers=header, data=dat)
        if response != None:
            response_json = response.json()
            json_txt(response_json)
            # 如果fuzz成功(即覆盖率发生改变)，将测试用例保存到MySQL数据库中
            time.sleep(2)
            now_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
            if now_coverage_rate_executed_code:
                pass
            '''fuzz_success_data[str(field_info.field_name)] = str(val) + str(location)'''
            if now_coverage_rate_executed_code != ini_coverage_rate_executed_code:
                # 先将字典json.dumps()序列化存储到redis，然后再json.loads()反序列化为字典
                fuzz_success_json_data = json.dumps(fuzz_success_data)
                if lll == 0:
                    save_post_fuzz_success(fuzz_success_json_data)
                elif lll == 1:
                    save_post_fuzz_optional_success(fuzz_success_json_data)
                fuzz_success_data.clear()
                mult_fuzz_k_times(fuzz_success_data, k, d, url, h, da, api_id, cov_url, ini_coverage_rate_executed_code,lll)
            else:
                pass
        else:
            pass
        print(response.json())
        print(i)

def post_fuzz_test(k, api_info, cov_url):
    print("必选参数")
    lll = 0
    print(api_info)
    print(api_info.api_id)
    print(api_info.path)
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    if not ini_coverage_rate_executed_code:
        pass
    global url
    url = api_info.path
    api_id = api_info.api_id
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id
    parameter = {}
    parameters = []
    for field_info in api_info.req_param:
        if field_info.require:
            parameter[str(field_info.field_name)] = str(field_info.field_type) + str(field_info.location)
            parameters.append(parameter)
    length = len(parameter)
    print(parameters)
    if length == 0:
        response = requests.post(url)
        print(response.json())
    elif length == 1:
        one_fuzz_k_times(fuzz_success_data, k, parameter, url, api_id, cov_url, ini_coverage_rate_executed_code,lll)
    else:
        a = Combination.get_combine(Combination, parameter)
        j = {}
        for i in parameters:
            j.update(i)
        for b in a:
            c = list(b)
            d = {}
            for n in c:
                d.update(n)         # 把b里面的内容转到d，d是字典
            g = {}
            for m in j.keys():
                if m not in d.keys():
                    g[m] = j[m]

            pa_location = []
            pa_name = []
            value_fuzz = []
            for q in g.keys():
                pa_name.append(q)
                pa_location.append(int(list(g[q])[-1]))
                pa_type = ''.join(list(g[q])[:-1])
                value_fuzz.append(fuzz(pa_type))
            urll, headers, data = make(url, pa_location, pa_name, value_fuzz,{},{})    # 不变参数构造完成url
            mult_fuzz_k_times(fuzz_success_data, k, d, urll, headers, data, api_id, cov_url,
                              ini_coverage_rate_executed_code,lll)

def post_fuzz_test_optional(k, api_info, cov_url):
    print("可选参数")
    lll = 1
    ini_coverage_rate_executed_code = GetCoverage.getCoverage_rate_executed_code(cov_url)
    if not ini_coverage_rate_executed_code:
        pass
    api_id = api_info.api_id
    global url
    url = api_info.path
    headers = {}
    data = {}
    # 存储fuzz成功的测试用例
    fuzz_success_data = {}
    fuzz_success_data['id'] = api_info.api_id

    # 将必选参数已经fuzz成功的测试用例加入到可选参数的url构造中
    fuzz_success_json_data = fuzz_success.lindex('post_success!!!!!!',-1)
    if fuzz_success_json_data != None:
        fuzz_success_dat = json.loads(fuzz_success_json_data)
        if fuzz_success_dat['id'] == api_id:
            require_param = fuzz_success_dat.keys()
            for i in range(len(require_param)):
                i = i + 1  # 因为第一个参数存储了id
                require_location = fuzz_success_dat[require_param[i]][-1]
                require_val = fuzz_success_dat[require_param[i]][:-1]
                url, headers, data = make(url,require_location,require_param[i],require_val,{},{})
    else:
        for field_info in api_info.req_param:
            if field_info.require:
                flag = 0
                location = field_info.location
                field_type = field_info.field_type
                value_fuzz = fuzz(field_type)
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value_fuzz))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value_fuzz)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value_fuzz)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(value_fuzz)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data[str(field_info.field_name)] = str(value_fuzz)
                    pass

    static_url = url

    optional_parameter = {}
    optional_parameters = []
    for field_info in api_info.req_param:
        if not field_info.require:
            print(field_info.field_name)
            optional_parameter[str(field_info.field_name)] = str(field_info.field_type) + str(field_info.location)
            optional_parameters.append(optional_parameter)
    end_list = Combination.get_combine(Combination, optional_parameters)    #  可选参数的组合
    j = {}
    for optional_param in end_list:                  #  对可选参数 j 里面进行部分改变部分不变处理
        optional_param = list(optional_param)
        for i in optional_param:
            j.update(i)
        if j == None:
            pass
        else:
            length = len(j)
            if length == 1:
                one_fuzz_k_times(fuzz_success_data, k, j, url, api_id, cov_url, ini_coverage_rate_executed_code,lll)
                print('success')
            else:
                a = Combination.get_combine(Combination, optional_param)     # 获取 可选参数 j 里面是否多次变化list 的组合
                w = {}
                for b in a:
                    b = list(b)

                    print(b)

                    for e in b:
                        w.update(e)                  #  w是要改变的参数合集dic

                    g = {}
                    for l in j.keys():
                        if l not in w.keys():
                            g[l] = j[l]              #  g是不变的参数合集dic
                    pa_location = []
                    pa_name = []
                    value_fuzz = []
                    for q in g.keys():
                        pa_name.append(q)
                        pa_location.append(int(list(g[q])[-1]))
                        pa_type = ''.join(list(g[q])[:-1])
                        value_fuzz.append(fuzz(pa_type))
                    p = {}
                    o = {}
                    urll, headers, data = make(static_url, pa_location, pa_name, value_fuzz,p,o)  # 不变参数构造完成url
                    print('不变参数构造完成url')
                    mult_fuzz_k_times(fuzz_success_data, k, w, urll, headers, data, api_id, cov_url,
                                      ini_coverage_rate_executed_code,lll)
                    w.clear()
                    g.clear()
        j.clear()

def save_post_fuzz_success(fuzz_success_json_data):
    fuzz_success.lpush('post_success!!!!!!', fuzz_success_json_data)

def save_post_fuzz_optional_success(fuzz_success_json_data):
    fuzz_success.lpush('post_optional_success!!!!!!', fuzz_success_json_data)

