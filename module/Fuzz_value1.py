import random
import requests
import redis
from rest_framework.utils import json
from module.graph2 import get_dep_info
from module.parse import parse
import os.path
import sys
import numpy as np

# sys.setrecursionlimit(100000)

# # 获取依赖测试graph
# my_path = os.path.abspath(os.path.dirname(__file__))
# api_info_list = parse(1.0)
# matrix, weight_info_list = get_dep_info(api_info_list)
# graph = matrix.tolist()
# print(graph)
# print(len(graph))
graph = []
api_info_list = []
# total = 0

######   创建visited，用来停止遍历，即一旦遇到visited，即刻退出递归 #0代表没被访问   #######


##################      创建Stack用于代替递归操作，改用循环实现遍历    ##################

# 采用栈顶尾端实现（即list的尾端为栈顶），push/pop的复杂度为1

class Stack:
    # 初始化栈为空列表
    def __init__(self):
        self.items = []
    # 判断栈是否为空，返回布尔值
    def isEmpty(self):
        return self.items == []
    # 压栈
    def push(self,item):
        self.items.append(item)
    # 出栈
    def pop(self):
        return self.items.pop()
    # 返回栈顶元素
    def peek(self):
        return self.items[len(self.items)-1]
    # 返回栈的大小
    def size(self):
        return len(self.items)

###########################      连接redis-pool      ##############################

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# req = redis.StrictRedis(connection_pool=pool)
resp = redis.StrictRedis(connection_pool=pool)

post = redis.StrictRedis(connection_pool=pool)
post.lpush('api_id_p', '')
delete = redis.StrictRedis(connection_pool=pool)
delete.lpush('api_id_d', '')

fuzz_success = redis.StrictRedis(connection_pool=pool)

#################################     模糊处理    ##################################
def fuzz(type):
    if 'integer' == type:
        # sys.maxsize整数最大值9223372036854775807， 整数最小值为-sys.maxsize-1 -9223372036854775808
        # sys.float_info.max float最大值为2.2250738585072014e-308 ,sys.float_info.min float最大值为1.7976931348623157e+308
        list_integer = [1,2,0,3,-45,-51,-82,
                        sys.maxsize,-sys.maxsize-1,sys.float_info.max,sys.float_info.min]

        return random.choice(list_integer)
    elif 'string' == type:
        # 我就随便写写，我也不知道写啥。。。
        list_string = ['3171261@qq.com','CommonLisp','Concrete5','John Doe',
                       'https://gitlab.example.com/api/v4/templates/gitignores/Ruby',
                       '# This file is a template, and might need editing',
                       '!@@#$$%%%^^^',
                       '(^&%GBH#T$G"""""""""""DFHBD"BDGVDFVWEF$$53346542@##@$#@%$##',
                       '2012-10-22T14:13:35Z',
                       'PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/groups/:id/access_requests',
                       '/uploads/-/system/appearance/logo/1/logo.png',
                       '#e75e40','#ffffff','logo=@/path/to/logo.png','5832fc6e14300a0d962240a8144466eef4ee93ef0d218477e55f11cf12fc3737'
                       'ee1dd64b6adc89cf7e2c23099301ccc2c61b441064e9324d963c46902a85ec34',
                       '127.0.0.1','hello@flightjs.com']

        return random.choice(list_string)

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

################################    测试    ########################################

# 记录拓扑排序顺序
topology_order = []
# 记录出度为0的点
out_degree_zero = []
# 设计出度为0的点
end = []


# 直接测试函数,(x,y)为graph中对应api节点
def test(x,api_info_list):
    api_info = api_info_list[x]
    url = api_info.path
    method = api_info.http_method
    data = ''
    # 用redis记录post和delete的id
    if method == 'post':
        for i in range(2):
            url = api_info.path
            data = []
            for field_info in api_info.req_param:
                if field_info.require:
                    flag = '0'
                    location = field_info.location

                    # 在资源池中寻找依赖字段的值
                    if resp.llen(str(field_info.field_name)) != 0:
                        listl = []
                        for i in range(resp.llen(str(field_info.field_name))): listl.append(i + 1)
                        index = random.choice(listl)
                        valu = resp.lindex(str(field_info.field_name),
                                           random.choice(str(index)))  # 从response的redis中根据name取对应value
                        value = str(valu, encoding="utf-8")
                        # 若需求字段对于格式有需求，可进行更改
                        if field_info.field_type == str:
                            continue
                        elif field_info.field_type == bytes:
                            pass

                    # 该节点对之前节点有依赖，并且所有依赖节点全部实现，但是仍有需求字段需人工实现
                    if resp.llen(str(field_info.field_name)) == 0:
                        value = fuzz(field_info.field_type)

                    # 这是针对本项目，本人的user_id是4，也可提前存到资源池中，这个不重要
                    if field_info.field_name == 'user_id':
                        value = 4

                    # 不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                    if location == 0:
                        url = url.replace('{' + field_info.field_name + '}', str(value))
                    elif location == 1:
                        # url追加key1=value1&key2=value2到url后,即查询字符串
                        if flag == 0:
                            flag = 1
                            url = url + "?" + str(field_info.field_name) + "=" + str(value)
                        else:
                            url = url + "&" + str(field_info.field_name) + "=" + str(value)
                    elif location == 2:
                        pass
                        # 操作
                    elif location == 3:
                        # 参数组成json字符串 ==> data
                        data.append(value)
                        pass
            post.lpush('api_id_p', api_info.api_id)

            if '?' in url:
                # 配置token
                url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            else:
                url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            # 请求API
            print("test " + str(api_info.api_id) + " " + method + " " + url)
            response = requests.post(url, data).text
            repon = str(response)
            if len(repon) > 0:
                reponses = json.loads(repon)
                json_txt(reponses)
            else:
                pass
            print(response)
    elif method == 'delete':
        for field_info in api_info.req_param:
            if field_info.require:
                flag = '0'
                location = field_info.location
                if resp.llen(str(field_info.field_name)) != 0:
                    listl = []
                    for i in range(resp.llen(str(field_info.field_name))): listl.append(i + 1)
                    index = random.choice(listl)
                    valu = resp.lindex(str(field_info.field_name),
                                       random.choice(str(index)))  # 从response的redis中根据name取对应value
                    value = str(valu, encoding="utf-8")
                else:
                    value = fuzz(field_info.field_type)
                if field_info.field_name == 'user_id':
                    value = 4

                # 不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    # 操作
                    pass
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data.append(value)
                    pass
        post.lrem('api_id_p', api_info.api_id, 0)

        if '?' in url:
            # 配置token
            url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        else:
            url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        # 请求API
        print("test " + str(api_info.api_id) + " " + method + " " + url)
        response = requests.delete(url).text
        repon = str(response)
        if len(repon) > 0:
            reponses = json.loads(repon)
            json_txt(reponses)
        else:
            pass
        print(response)
    else:
        for field_info in api_info.req_param:
            if field_info.require:
                flag = '0'
                location = field_info.location

                if resp.llen(str(field_info.field_name)) != 0:
                    listl = []
                    for i in range(resp.llen(str(field_info.field_name))): listl.append(i + 1)
                    index = random.choice(listl)
                    valu = resp.lindex(str(field_info.field_name),
                                       random.choice(str(index)))  # 从response的redis中根据name取对应value
                    if valu:
                        value = str(valu, encoding="utf-8")
                    # 若需求字段对于格式有需求，可进行更改
                    if field_info.field_type == str:
                        continue
                    elif field_info.field_type == bytes:
                        pass
                else :
                    value = fuzz(field_info.field_type)

                if field_info.field_name == 'user_id':
                    value = 4

                # 不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    # 操作
                    pass
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data.append(value)
                    pass

        if '?' in url:
            # 配置token
            url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        else:
            url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        # 请求API
        print("test " + str(api_info.api_id) + " " + method + " " + url)
        if method == 'get':
            response = requests.get(url, data).text
        elif method == 'put':
            response = requests.put(url).text
        elif method == 'patch':
            response = requests.put(url).text
        repon = str(response)
        if len(repon) > 0:
            reponses = json.loads(repon)
            json_txt(reponses)
        else:
            pass
        print(response)



# fuzz处理graph（x）位置的api
def fuzzgraph(x, api_info_list):
    api_info = api_info_list[x]
    url = api_info.path
    method = api_info.http_method
    data = ''
    # 用redis记录post和delete的id
    if method == 'post':
        for i in range(2):
            url = api_info.path
            val = 0
            headers = {}
            data = []
            for field_info in api_info.req_param:
                # if field_info.require:
                flag = '0'
                location = field_info.location
                field_type = field_info.field_type
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
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(value)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data.append(value)
                    pass
            '''Redis存储post过的api_id'''
            post.lpush('api_id_p', api_info.api_id)
            '''配置token'''
            if '?' in url:
                url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            else:
                url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
            '''
            请求API
            根据header中Content-Tpye对应data类型：
            常见的媒体格式类型：
            text/html ： HTML格式
            text/plain ：纯文本格式
            text/xml ： XML格式
            image/gif ：gif图片格式
            image/jpeg ：jpg图片格式
            image/png：png图片格式

            application/xml： XML数据格式
            application/json： JSON数据格式
            application/octet-stream ： 二进制流数据（如常见的文件下载）
            application/x-www-form-urlencoded ： <form encType=””>中默认的encType，form表单数据被编码为key/value格式发送到服务器（表单默认的提交数据的格式）
            
            multipart/form-data ： 需要在表单中进行文件上传时，就需要使用该格式
            '''
            print("fuzz " + str(api_info.api_id) + " " + method + " " + url)
            if len(headers) != 0:
                if headers.__contains__('Content-Type'):
                    if headers['Content-Type'] == 'application/json':
                        datas = json.dumps(data)
                    elif headers['Content-Type'] == 'application/x-www-form-urlencoded':
                        datas = data
                    elif headers['Content-Type'] == 'multipart/form-data':
                        '''
                        files = {"file": open("C:/Users/Administrator/Desktop/test.txt", "rb")}
                        r = requests.post("http://httpbin.org/post", files=files)
                        '''
                        pass
                else:
                    pass
            response = requests.post(url, headers = headers, data = datas).text
            repon = str(response)
            if len(repon) > 0:
                reponses = json.loads(repon)
                json_txt(reponses)
                if isinstance(reponses, dict):
                    # 如果fuzz成功，将fuzz内容保存到fuzz_success连接池中
                    if reponses.keys() != 'error' and reponses.keys() != 'message':
                        fuzz_success.lpush(str(field_info.field_name), str(val))
            else:
                pass
            print(response)
    elif method == 'delete':
        val = 0
        for field_info in api_info.req_param:
            if field_info.require:
                flag = '0'
                location = field_info.location
                field_type = field_info.field_type
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                # 不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    # 操作
                    pass
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data = [].append(value)
                    pass
        post.lrem('api_id_p', api_info.api_id, 0)

        if '?' in url:
            # 配置token
            url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        else:
            url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        # 请求API
        print("fuzz " + str(api_info.api_id) + " " + method + " " + url)
        response = requests.delete(url).text
        repon = str(response)
        if len(repon) > 0:
            reponses = json.loads(repon)
            json_txt(reponses)
            if isinstance(reponses, dict):
                # 如果fuzz成功，将fuzz内容保存到fuzz_success连接池中
                if reponses.keys() != 'error' and reponses.keys() != 'message':
                    fuzz_success.lpush(str(field_info.field_name), str(val))
        else:
            pass
        print(response)
    else:
        # fuzz_list用于临时存储fuzz成功的案例
        fuzz_list = []
        for field_info in api_info.req_param:
            if field_info.require:
                flag = '0'
                location = field_info.location
                field_type = field_info.field_type
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz

                # 临时存储fuzz成功的dic
                fuzz_dic = {}
                fuzz_dic[field_info.field_name] = [value]
                fuzz_list.append(fuzz_dic)

                # 不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    # 操作
                    pass
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data = [].append(value)
                    pass

        if '?' in url:
            # 配置token
            url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
        else:
            url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"
        # 请求API
        print("fuzz " + str(api_info.api_id) + " " + method + " " + url)
        if method == 'get':
            response = requests.get(url, data).text
        elif method == 'put':
            response = requests.put(url).text
        elif method == 'patch':
            response = requests.put(url).text
        repon = str(response)
        if len(repon) > 0:
            reponses = json.loads(repon)
            json_txt(reponses)
            if isinstance(reponses, dict):
                # 如果fuzz成功，将fuzz内容保存到fuzz_success连接池中
                if reponses.keys() == 'error' and reponses.keys() == 'message':
                    pass
                else:
                    for fuzz_dic in fuzz_list:
                        if fuzz_dic.keys():
                            fname = str(fuzz_dic.keys())
                            fvalue = fuzz_dic.get(fname)
                            fuzz_success.lpush(fname, str(fvalue))
        else:
            pass
        print(response)



def topology_visit(g, n, api_info_list, visited):
    # 第一个开始节点api是没有依赖的，其中需要的参数可通过fuzz来获取（也可人工赋值）
    visited[n] = 1
    fuzzgraph(n,api_info_list)
    while visited[n] == 1:
        # 创建遍历的存储队列
        queue = []
        for i in range(len(g)):
            if g[i][n] != -1:
                queue.append(i)
        if len(queue) == 0:
            break
        for j in queue:
            g[j][n] = -1
            if g[j] == end and visited[j] == 0:
                # i = queue.index(j)
                # i = i+1
                # for k in range(i,len(queue)):   # 将可测试的api节点后面所有已存储在queue里面的节点在对应graph上的值变为-1
                #     z = queue[k]
                #     g[z][n] = -1
                for a in queue:
                    g[a][n] = -1                 # 表示queue里所有api对n节点api的依赖全部实现，故改为-1，表示对此无依赖
                test(j,api_info_list)
                queue.clear()
                visited[j] = 1
                n = j

        if len(queue) != 0:                     # 说明queue里面所有api都无法test,并且资源池中也没有资源
            k = random.choice(queue)
            for a in queue:
                g[a][n] = -1
            queue.clear()
            if visited[k] == 0:
                fuzzgraph(k,api_info_list)
                visited[k] = 1
                g[k] = end
            n = k


def traversal(grap, api_info_lis):
    graph = grap
    api_info_list = api_info_lis
    end = []
    # 创建visited，用来停止遍历，即一旦遇到visited，即刻退出递归 #0代表没被访问
    visited = np.zeros(len(graph)).astype(dtype=int).tolist()
    print(visited)
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
        topology_visit(graph, k, api_info_list, visited)

    # for i in range(len(graph)):
    #     if g_list[i] == -1:
    #         global total
    #         total = total+1
    # print(total)

    return visited

# # 测试程序
# traversal(graph)


