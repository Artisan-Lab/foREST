import requests
import os.path
from prance import ResolvingParser
import json
import random
from random import randrange
import parse
from datetime import timedelta, datetime


def add_token(url):
    if '?' in url:
        url = url + '&private_token=zKZFJN3EymWm5GMCaCwx'
    else:
        url = url + '?private_token=zKZFJN3EymWm5GMCaCwx'
    return url


def random_str(slen=10):
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(slen):
      sa.append(random.choice(seed))
    return ''.join(sa)


def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)


def fuzz_paramerter(field_info):
    if field_info.enum:
        return field_info.field_name + '=' + str(random.choice(field_info.enum))
    elif field_info.format:
        if field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
            return field_info.field_name + '=' + \
                   str(random_date(datetime(2019,1,1,0,0,0).astimezone().replace(microsecond=0),
                    datetime(2021,12,31,23,59,59).astimezone().replace(microsecond=0)).isoformat())
    else:
        if field_info.field_type == 'boolean':
            return field_info.field_name + '=' + random.choice(['true', 'false'])
        elif field_info.field_type == 'string':
            return field_info.field_name + '=' + random_str(random.randint(0,10))
        elif field_info.field_type == 'integer':
            return field_info.field_name + '=' + str(random.randint(0,50))
    pass


def created_url(url, req_paramerter):
    fuzz_parameter = fuzz_paramerter(req_paramerter)
    url1 = url + '&' + fuzz_parameter
    return url1


def get_responses(url, req_paramerter, responses_list, default_count):
    url1 = created_url(url, req_paramerter)
    request_respones = requests.get(url1)
    respones_status = request_respones.status_code
    if 300 > respones_status >= 200 and default_count < 10:
        if json.loads(request_respones.text) == []:
            responses_list = get_responses(url, req_paramerter, responses_list, default_count + 1)
        else:
            responses_list.append(json.loads(requests.get(url1).text))
    elif 500 > respones_status >= 300 and default_count < 10:
        responses_list = get_responses(url, req_paramerter, responses_list, default_count + 1)
    elif 500 == respones_status:
        print('find bug in %s' % url1)
    return responses_list


def MR_texting(responses_list, MR_matric):
    #subset  equality equivalence disjoint complete diffirence
    response_text = responses_list[0]
    response_random = random.sample(responses_list[1:10],2)
    response_text1 = response_random[0]
    response_text2 = response_random[1]
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
    if (all([response_text[i] not in response_text1 for i in range(0,len(response_text))]) and
            all([response_text1[i] not in response_text for i in range(0,len(response_text1))])):
        MR_matric[3] = MR_matric[3] + 1
    return MR_matric


def metamorphic(api_info):
    url = add_token(api_info.path)
    if api_info.req_field_names:
        for req_paramerter in api_info.req_param:
            if req_paramerter.field_name in api_info.req_field_names:
                fuzz_parameter = fuzz_paramerter(req_paramerter)
                url = url + '&' + fuzz_parameter
    for req_paramerter in api_info.req_param:
        # 测API的每个参数
        MR_matric = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        if req_paramerter.field_name in api_info.req_field_names:
            continue
        responses = [json.loads(requests.get(url).text)]
        for i in range(1,11):
            responses = get_responses(url, req_paramerter, responses, 0)
        if len(responses) < 10:
            print('no enough %s' % req_paramerter.field_name)
            continue
        for i in range(1,11):
            MR_matric = MR_texting(responses, MR_matric)
        if MR_matric[0] == max(MR_matric) and MR_matric[1] + MR_matric[2] <MR_matric[0]:
            MRs = 'subset'
        if MR_matric[1] == max(MR_matric):
            MRs = 'equality or test case not use'
        if MR_matric[1] + MR_matric[2] == MR_matric[0] and MR_matric[1] != 0 and MR_matric[2] !=0:
            MRs = 'equivalence'
        print(req_paramerter.field_name + '   ' +MRs)


path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    metamorphic(api_info)




# def mr_test_get(specification,url,method,token):