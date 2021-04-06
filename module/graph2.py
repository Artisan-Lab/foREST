from module.parse import parse
import os
from prance import ResolvingParser
from operator import length_hint
import numpy as np

# def make():
#     path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/wordpress.yaml")
#     parser = ResolvingParser(path)
#     spec = parser.specification
#     servers = spec.get("servers")
#     url = servers.get('url')
#     return url


'''
静态分析：根据路径，匹配路径上相似程度，认为相似程度越高，依赖程度越高
count记录相似程度：
    0 代表不相关
    非0 代表request和response的parameter相同：
        1 代表仅参数相同
        2 代表除参数外，路径上有一个相同
        3 代表除参数外，路径上有两个相同
        ......
        我认为路径相同，依赖程度越高，但是也可根据description进行相似度的检测，3.0版本将加入description进行检测
req_url_path, resp_url_path 用于判断路径相似程度
req_object_dic, resp_object_dic 字典存储object类型数据
    object_list = {23:int,litianyu:string,888:int,str:string,68:int}
'''
def dependency_object2object(req_url_path, resp_url_path, req_object_dic, resp_object_dic):
    count = 0
    for req_key in req_object_dic.keys():
        if req_key in resp_object_dic.keys() and req_object_dic[req_key] == resp_object_dic[req_key]:
            count = 1
            # url = make()
            # req_path = req_url_path.replace(url, '')
            # resp_path = resp_url_path.replace(url, '')
            # req_li = req_path.split('/')
            # resp_li = resp_path.split('/')
            # for req in req_li:
            #     if req in resp_li:
            #         count += 1
            return count
        else:
            return count


def dependency_object2int(req_url_path, resp_url_path, req_object_dic, resp_name, resp_type):
    count = 0
    if resp_name in req_object_dic.keys() and resp_type == req_object_dic[resp_name]:
        count = 1
        return count
    else:
        return count


def dependency_int2int(req_url_path, resp_url_path, req_name, req_type, resp_name, resp_type):
    count = 0
    if req_name == resp_name and req_type == resp_type:
        count = 1
        return count
    else:
        return count


def denpendency_int2object(req_url_path, resp_url_path, req_field_name, req_array, resp_object_dic):
    count = 0
    if req_field_name in resp_object_dic.keys() and req_array == resp_object_dic[req_field_name]:
        count = 1
        return count
    else:
        return count


def adj(api_info_list):
    global index
    index = 0
    # base on request
    for req_api_list in api_info_list:
        if req_api_list.req_param != []:
            i = req_api_list.api_id
            for req_field_info in req_api_list.req_param:
                # 依赖字段必须
                if req_field_info.require == True:
                    '''
                    判断是否为object或者array这种复杂类型
                    分别用dependency_object2object
                         dependency_object2int
                         dependency_int2int
                         dependency_int2object
                    判断依赖
                    '''
                    if req_field_info.field_type == 'object':
                        option_object(req_field_info.object)
                        req_object_dic = object_dic
                        object_dic.clear()
                        for resp_api_list in api_info_list:
                            if resp_api_list.resp_param != []:
                                j = resp_api_list.api_id
                                for resp_field_info in resp_api_list.resp_param:
                                    if resp_field_info.field_type == 'object':
                                        option_object(resp_field_info.object)
                                        resp_object_dic = object_dic
                                        object_dic.clear()
                                        count = dependency_object2object(req_api_list.path, resp_api_list.path,
                                                                         req_object_dic, resp_object_dic)
                                    elif resp_field_info.field_type == 'array':
                                        if isinstance(resp_field_info.array, list):
                                            option_array(resp_field_info.array)
                                            resp_array_dic = array_dic
                                            array_dic.clear()
                                            count = dependency_object2object(req_api_list.path, resp_api_list.path,
                                                                         req_object_dic, resp_array_dic)
                                        else:
                                            count = dependency_object2int(req_api_list.path, resp_api_list.path,
                                                                         req_object_dic, resp_field_info.field_name, resp_field_info.field_type)
                                    if count:
                                        matrix[i][j] = index
                                        score[i][j] = count
                                        weight_info_list.append(req_field_info.field_name)
                                        index += 1

                    elif req_field_info.field_type == 'array':
                        if isinstance(req_field_info.array, list):
                            option_array(req_field_info.array)
                            req_array_dic = array_dic
                            array_dic.clear()
                            for resp_api_list in api_info_list:
                                if resp_api_list.resp_param != []:
                                    j = resp_api_list.api_id
                                    for resp_field_info in resp_api_list.resp_param:
                                        if resp_field_info.field_type == 'object':
                                            option_object(resp_field_info.object)
                                            resp_object_dic = object_dic
                                            object_dic.clear()
                                            count = dependency_object2object(req_api_list.path, resp_api_list.path,
                                                                             req_array_dic, resp_object_dic)
                                        elif resp_field_info.field_type == 'array':
                                            if isinstance(resp_field_info.array, list):
                                                option_array(resp_field_info.array)
                                                resp_array_dic = array_dic
                                                array_dic.clear()
                                                count = dependency_object2object(req_api_list.path, resp_api_list.path,
                                                                             req_array_dic, resp_array_dic)
                                            else:
                                                count = dependency_int2int(req_api_list.path, resp_api_list.path,
                                                                           req_field_info.field_name, req_field_info.array,
                                                                           resp_field_info.field_name, resp_field_info.array)
                                        else:
                                            count = dependency_object2int(req_api_list.path, resp_api_list.path,
                                                                          req_array_dic, resp_field_info.field_name, resp_field_info.field_type)
                                        if count:
                                            matrix[i][j] = index
                                            score[i][j] = count
                                            weight_info_list.append(req_field_info.field_name)
                                            index += 1

                        else:    # field_name,array
                            for resp_api_list in api_info_list:
                                if resp_api_list.resp_param != []:
                                    j = resp_api_list.api_id
                                    for resp_field_info in resp_api_list.resp_param:
                                        if resp_field_info.field_type == 'object':
                                            option_object(resp_field_info.object)
                                            resp_object_dic = object_dic
                                            object_dic.clear()
                                            count = denpendency_int2object(req_api_list.path, resp_api_list.path,
                                                                           req_field_info.field_name, req_field_info.array,
                                                                           resp_object_dic)
                                        elif resp_field_info.field_type == 'array':
                                            if isinstance(resp_field_info.array, list):
                                                option_array(resp_field_info.array)
                                                resp_array_dic = array_dic
                                                array_dic.clear()
                                                count = denpendency_int2object(req_api_list.path, resp_api_list.path,
                                                                               req_field_info.field_name, req_field_info.array,
                                                                               resp_array_dic)
                                            else:
                                                count = dependency_int2int(req_api_list.path, resp_api_list.path,
                                                                           req_field_info.field_name, req_field_info.array,
                                                                           resp_field_info.field_name, resp_field_info.array)
                                        else:
                                            count = dependency_int2int(req_api_list.path, resp_api_list.path,
                                                                       req_field_info.field_name, req_field_info.array,
                                                                       resp_field_info.field_name, resp_field_info.field_type)
                                        if count:
                                            matrix[i][j] = index
                                            score[i][j] = count
                                            weight_info_list.append(req_field_info.field_name)
                                            index += 1
                    else:
                        for resp_api_list in api_info_list:
                            if resp_api_list.resp_param != []:
                                j = resp_api_list.api_id
                                for resp_field_info in resp_api_list.resp_param:
                                    if resp_field_info.field_type == 'object':
                                        option_object(resp_field_info.object)
                                        resp_object_dic = object_dic
                                        object_dic.clear()
                                        count = denpendency_int2object(req_api_list.path, resp_api_list.path,
                                                                       req_field_info.field_name, req_field_info.field_type,
                                                                       resp_object_dic)
                                    elif resp_field_info.field_type == 'array':
                                        if isinstance(resp_field_info.array, list):
                                            option_array(resp_field_info.array)
                                            resp_array_dic = array_dic
                                            array_dic.clear()
                                            count = denpendency_int2object(req_api_list.path, resp_api_list.path,
                                                                           req_field_info.field_name, req_field_info.field_type,
                                                                           resp_array_dic)
                                        else:
                                            count = dependency_int2int(req_api_list.path, resp_api_list.path,
                                                                       req_field_info.field_name, req_field_info.field_type,
                                                                       resp_field_info.field_name, resp_field_info.array)
                                    else:
                                        count = dependency_int2int(req_api_list.path, resp_api_list.path,
                                                                   req_field_info.field_name, req_field_info.field_type,
                                                                   resp_field_info.field_name, resp_field_info.field_type)
                                    if count:
                                        matrix[i][j] = index
                                        score[i][j] = count
                                        weight_info_list.append(req_field_info.field_name)
                                        index += 1
                # 依赖字段非必须
                else:
                    pass


'''
type(object) = List  type(array) = List
object_info(self,name,type)   array(self,type)
应该返回整合好的依赖字段
example: object(int,sting,array) => chenyang(26,'chenyang',[88,'str',68])
         object_list = {23:int,litianyu:string,888:int,str:string,68:int}
'''
object_dic = {}
def option_object(objects):
    if objects:
        for obj in objects:
            if obj.type == 'array':
                if isinstance(obj, list):
                    option_array(obj.object)
                else:
                    pass
            elif obj.type == 'object':
                option_object(obj.object)
            else:
                object_dic[obj.name] = obj.type

array_dic = {}
def option_array(array):
    if array:
        for arr in array:
            if arr.type == 'array':
                if isinstance(arr, list):
                    option_array(arr.object)
                else:
                    pass
            elif arr.type == 'object':
                option_object(arr.object)
            else:
                array_dic[arr.name] = arr.type


'''
不同字段名称相同字典,存储格式：{"0":["id + group_id + parameters"]}代表api0中的parameters中的id的真实含义为group_id
直接改api_list，从矩阵上改太繁琐
dic = { 647: ["id + group_id + parameters", "id + group_id + responses"] }
'''
dictionary = {}
def update_api_list(dic,api_info_list):
    for api_info in api_info_list:
        if api_info.api_id in dic.keys():
            rename_list = dic[api_info.api_id]
            for rel in rename_list:
                rell = rel.split('+')
                if rell[2] == 'parameters':
                    for req in api_info.req_param:
                        if rell[0] == req.field_name:
                            req.field_name = rell[1]
                else:
                    for resp in api_info.resp_param:
                        if rell[0] == resp.field_name:
                            resp.field_name = rell[1]
    return api_info_list


'''
api的information，以list保存 , num为api的number 
dir1,2分别为特殊的api存储，表示字段相同含义不同，字段不同含义相同
'''
def get_dep_info(api_info_list):
    update_api_info_list = update_api_list(dictionary,api_info_list)
    global num
    num = length_hint(api_info_list)
    num = num + 1
    # 定义邻接矩阵matri
    global  matrix
    matrix = np.zeros([num, num], dtype=int)
    m = np.ones([num, num], dtype=int)
    matrix -= m
    # 存储相似程度分数
    global score
    score = np.zeros([num, num], dtype=int)
    # 定义一个list，命名weight_info_list，其中index从0~n，填入matrix，其中list[index]=[].append(id,name...)存储请求字段
    global weight_info_list
    weight_info_list = []
    adj(update_api_info_list)
    # print(matrix)
    # print(weight_info_list)
    return matrix, weight_info_list
