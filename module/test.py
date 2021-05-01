import random
import redis
import sys
import numpy as np

from module.delete_test import delete_fuzz_test, delete_fuzz_test_optional
from module.get_test import get_fuzz_test, get_fuzz_test_optional
from module.patch_test import patch_fuzz_test, patch_fuzz_test_optional
from module.post_test import post_fuzz_test,post_fuzz_test_optional
from module.put_test import put_fuzz_test, put_fuzz_test_optional

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

# fuzz处理graph（x）位置的api
def fuzzgraph(x, api_info_list, cov_url):
    api_info = api_info_list[x]
    method = api_info.http_method
    if method == 'post':
        k = 5
        post_fuzz_test(k,api_info,cov_url)
        post_fuzz_test_optional(k, api_info, cov_url)
    elif method == 'delete':
        k = 5
        delete_fuzz_test(k, api_info, cov_url)
        delete_fuzz_test_optional(k, api_info, cov_url)
    elif method == 'get':
        k = 5
        get_fuzz_test(k, api_info, cov_url)
        get_fuzz_test_optional(k, api_info, cov_url)
    elif method == 'put':
        k = 5
        put_fuzz_test(k, api_info, cov_url)
        put_fuzz_test_optional(k, api_info, cov_url)
    else:
        k = 5
        patch_fuzz_test(k, api_info, cov_url)
        patch_fuzz_test_optional(k, api_info, cov_url)
    print(str(api_info.api_id) + '全部参数所有fuzz完成')


def topology_visit(g, n, api_info_list, visited, end, cov_url):
    # 第一个开始节点api是没有依赖的，其中需要的参数可通过fuzz来获取（也可人工赋值）
    visited[n] = 1
    fuzzgraph(n, api_info_list, cov_url)
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
                fuzzgraph(k, api_info_list,cov_url)
                visited[k] = 1
                g[k] = end
                n = k


def traversal(grap, api_info_lis, cov_url):
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
        topology_visit(graph, k, api_info_list, visited, end, cov_url)

    return visited



