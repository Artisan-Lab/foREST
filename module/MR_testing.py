import requests
import os.path
from prance import ResolvingParser
import json
import parse
import random
from datetime import timedelta, datetime
from random import randrange


def random_date(start, end):
    # 随机生成start与end之间的日期 format：ISO 8601
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_str(slen=10):
    # 随机生成字符串，默认长度为10
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    return ''.join(sa)


def fuzz_parameter(field_info):
    if field_info.enum:
        return field_info.field_name + '=' + str(random.choice(field_info.enum))
    elif field_info.format:
        if field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
            return field_info.field_name + '=' + \
                   str(random_date(
                       datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(microsecond=0)).isoformat())
    else:
        if field_info.field_type == 'boolean':
            return field_info.field_name + '=' + random.choice(['true', 'false'])
        elif field_info.field_type == 'string':
            return field_info.field_name + '=' + random_str()
        elif field_info.field_type == 'integer':
            return field_info.field_name + '=' + str(random.randint(0, 50))
    pass


def add_token(url):
    # 加上token 因为暂时不考虑token的问题 所以在第一步就加上token
    # if '?' in url:
    #     url = url + '&private_token=n19y6WJgSgjyDuFSHMx9'
    #     # ehWyDYxYMRcFLKCRryeK root token
    # else:
    url = url + '?private_token=n19y6WJgSgjyDuFSHMx9'
    return url


def get_responses(url, req_parameter, responses_list, default_count):
    # 获取一个响应列表 其中 列表第一项为源输出（不加参数的输出）
    parameter = fuzz_parameter(req_parameter)
    url1 = url + '&' + parameter
    request_response = requests.get(url1)
    response_status = request_response.status_code
    if 300 > response_status >= 200 and default_count < 10:
        if not json.loads(request_response.text):
            responses_list = get_responses(url, req_parameter, responses_list, default_count + 1)
        else:
            responses_list.append(json.loads(requests.get(url1).text))
    elif 500 > response_status >= 300 and default_count < 10:
        responses_list = get_responses(url, req_parameter, responses_list, default_count + 1)
    elif 500 == response_status:
        print('find bug in %s' % url1)
    return responses_list


def MR_texting(response_text, response_text1, response_text2, MR_matric):
    # MR_matric 的 含义分别为 subset  equality equivalence disjoint complete diffirence
    response_text3 = response_text1 + response_text2
    if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) or \
            all([response_text1[i] in response_text for i in range(0, len(response_text1))])):
        # judge subset
        MR_matric[0] = MR_matric[0] + 1
    if response_text == response_text1:
        MR_matric[1] = MR_matric[1] + 1
    if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) and
            all([response_text1[i] in response_text for i in range(0,len(response_text1))])) and \
            response_text1 != response_text:
        MR_matric[2] = MR_matric[2] + 1
    if (all([response_text2[i] not in response_text1 for i in range(0,len(response_text2))]) and
            all([response_text1[i] not in response_text2 for i in range(0,len(response_text1))])):
        MR_matric[3] = MR_matric[3] + 1
    if (all([response_text[i] in response_text3 for i in range(0,len(response_text))]) and
            all([response_text3[i] in response_text for i in range(0,len(response_text3))])) and \
            response_text1 != response_text2:
        MR_matric[4] = MR_matric[4] + 1
    return MR_matric


def metamorphic(api_info,parameter_list):
    if api_info.http_method == 'get':
        MR_dic = {}
        url = add_token(api_info.path)
        if api_info.req_field_names:
            for req_paramerter in api_info.req_param:
                if req_paramerter.field_name in api_info.req_field_names:
                    parameter = str(parameter_list[req_paramerter.field_name])
                    if req_paramerter.location == 0:
                        url = url.replace('{'+req_paramerter.field_name+'}',parameter)
                    else:
                        url = url + '&' + parameter
        source_response = requests.get(url)
        if source_response.status_code > 300:
            print(url+'dependency default')
            return
        for req_paramerter in api_info.req_param:
            # 测API的每个参数
            MR_matric_count = [0, 0, 0, 0, 0, 0]
            # 前三个为源输出与加参数输出之间的关系 subset equality equivalence
            # 不同参数输出之间的关系 disjoint
            # 不同参数输出与源输出之间的关系 complete
            # 多次相同请求之间的关系difference
            MR_matric = [0, 0, 0, 0, 0, 0]
            # 记录测得的MR
            if req_paramerter.field_name in api_info.req_field_names:
                continue
            responses = [json.loads(requests.get(url).text)]
            for i in range(1,11):
                responses = get_responses(url, req_paramerter, responses, 0)
            if len(responses) < 10:
                print('lack %s' % req_paramerter.field_name)
                continue
            for i in range(1, 11):
                response_text = responses[0]
                response_text1 = random.choice(responses[1:11])
                response_text2 = random.choice(responses[1:11])
                for i in range(10):
                    if response_text1 == response_text2:
                        response_text2 = random.choice(responses[1:11])
                MR_matric_count = MR_texting(response_text, response_text1, response_text2, MR_matric_count)
            if MR_matric_count[0] == max(MR_matric_count): #and MR_matric_count[1] + MR_matric_count[2] <MR_matric_count[0]:
                MR_matric[0] = 1
            if MR_matric_count[1] == max(MR_matric_count):
                MR_matric[1] = 1
            if MR_matric_count[1] + MR_matric_count[2] == MR_matric_count[0] and MR_matric_count[1] != 0 and MR_matric_count[2] !=0:
                MR_matric[2] = 1
            if MR_matric_count[3] == max(MR_matric_count):
                MR_matric[3] = 1
            if MR_matric_count[4] == 10 and MR_matric_count[2] != 1:
                MR_matric[4] = 1
            MR_dic[str(req_paramerter.field_name)] = MR_matric
        print(str(MR_dic))


path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    metamorphic(api_info,{'user_id': 34})




# def mr_test_get(specification,url,method,token):
