import requests
import os.path
from prance import ResolvingParser
import json
import random
import parse


def add_token(url):
    if '?' in url:
        url = url + '&private_token=zKZFJN3EymWm5GMCaCwx'
    else:
        url = url + '?private_token=zKZFJN3EymWm5GMCaCwx'
    return url


def fuzz(field_info):
    if field_info.default:
        return field_info.field_name + '=' + field_info.default
    elif field_info.enum:
        return field_info.field_name + '=' + random.choice(field_info.enum)
    else:
        if field_info.field_type == 'boolean':
            return field_info.field_name + '=' + random.choice(['true', 'false'])
        elif field_info.field_type == 'string':
            return field_info.field_name + '=' + random.choice(['sample', '', ' ', 'fsdapo324,;,fl;sa'])
        elif field_info.field_type == 'integer':
            return field_info.field_name + '=' + random.choice(['0', '1', '-1'])
    pass


def MR_judge(test1_url, test2_url):
    request_respones = requests.get(test1_url)
    request_respones2 = requests.get(test2_url)
    respones_status2 = request_respones2.status_code
    respones_text = json.loads(request_respones.text)
    respones_text2 = json.loads(request_respones2.text)
    if 300 > respones_status2 >= 200:
        status = 'success'
    elif 500 > respones_status2 >=300:
        status = 'error'
        return 'format error'
    elif 500 == respones_status2:
        status = 'internal error'
        return 'find bug'
    MR = 'None'
    if all([respones_text2[i] in respones_text for i in range(0,len(respones_text2))]):
        # judge subset
        MR = 'Subset'
    if respones_text2 == respones_text:
        MR = 'Equality'
    if (all([respones_text2[i] in respones_text for i in range(0,len(respones_text2))]) and
            all([respones_text[i] in respones_text2 for i in range(0,len(respones_text))])):
        MR = 'Equivalence'
    if (all([respones_text2[i] not in respones_text for i in range(0,len(respones_text2))]) and
            all([respones_text2[i] not in respones_text for i in range(0,len(respones_text2))])):
        MR = 'Disjoint'
    return MR
    pass


def metamorphic(api_info):
    url = api_info.path
    if api_info.req_field_names:
        for req_paramerter in api_info.req_param:
            if req_paramerter.field_name in api_info.req_field_names:
                fuzz_parameter = fuzz(req_paramerter)
                if '?' in url:
                    url = url + '?' + fuzz_parameter
                else:
                    url = url + '&' + fuzz_parameter
    for req_paramerter in api_info.req_param:
        # 测API的每个参数
        if req_paramerter.field_name in api_info.req_field_names:
            continue
        url1 = add_token(url)
        fuzz_parameter = fuzz(req_paramerter)
        if '?' in url:
            url2 = add_token(url + '&' + fuzz_parameter)
        else:
            url2 = add_token(url + '?' + fuzz_parameter)

        MR = MR_judge(url1,url2)
        print(MR)



path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    metamorphic(api_info)




# def mr_test_get(specification,url,method,token):