import requests
import random
from datetime import timedelta, datetime
import json
import sys


def random_date(start, end):
    # 随机生成start与end之间的日期 format：ISO 8601
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)


def random_str(slen=10):
    # 随机生成字符串，默认长度为10
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    list_string = ['3171261@qq.com',
                   'https://gitlab.example.com/api/v4/templates/gitignores/Ruby',
                   '!@@#$$%%%^^^',
                   '127.0.0.1',
                   "中国华为",
                   "复旦大学",
                   "智能可靠性测试"]
    strr = str(random.choice(list_string).encode('utf-8')).replace("\\x", "%").replace("b'", "").replace("'", "")[0:-3]
    return random.choice([''.join(sa), strr])


class FuzzAndJudgeUnit:
    parameter = None
    responses_status = None
    request_response = None
    new_url = None

    def __init__(self, field_info, base_url):
        self.field_info = field_info
        self.base_url = base_url

    @staticmethod
    def array_handle(array):
        array_list = []
        value = None
        if isinstance(array, str):
            if array == 'integer':
                fuzz_value = random.choice([1, 2, 0, 3, -45, -51, -82,
                                            sys.maxsize, -sys.maxsize - 1, sys.float_info.max, sys.float_info.min])
            elif array == 'boolean':
                fuzz_value = random.choice(['true', 'false'])
            elif array == 'string':
                fuzz_value = random_str()
            else:
                fuzz_value = None
                print('can not fuzz array %s' % array)
        elif isinstance(array, list):
            fuzz_value = FuzzAndJudgeUnit.object_handle(array)
        else:
            print('can not fuzz array %s' % array)
            fuzz_value = None
        array_list.append(fuzz_value)
        return array_list

    @staticmethod
    def object_handle(objects):
        object_list = {}
        for object_ in objects:
            value = FuzzAndJudgeUnit.fuzz_value(object_)
            object_list[object_.name] = value
        return object_list

    @staticmethod
    def fuzz_value(field_info):
        if field_info.enum:
            fuzz_value = field_info.field_name + '=' + str(random.choice(field_info.enum))
        elif field_info.format:
            if field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
                fuzz_value = field_info.field_name + '=' + \
                                 str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                                 datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(
                                                     microsecond=0)).isoformat())
            else:
                print('please Add format %s' % field_info.format())
                field_info.format = None
                fuzz_value = FuzzAndJudgeUnit.fuzz_value(field_info)
        else:
            if field_info.field_type == 'boolean':
                fuzz_value = field_info.field_name + '=' + random.choice(['true', 'false'])
            elif field_info.field_type == 'string':
                fuzz_value = random_str()
            elif field_info.field_type == 'integer':
                fuzz_value = random.choice([1, 2, 0, 3, -45, -51, -82,
                        sys.maxsize, -sys.maxsize - 1, sys.float_info.max, sys.float_info.min])
            elif field_info.field_type == 'object':
                fuzz_value = FuzzAndJudgeUnit.object_handle(field_info.object)
            elif field_info.field_typ == 'array':
                fuzz_value = FuzzAndJudgeUnit.array_handle(field_info.array)
            else:
                fuzz_value = None
        return fuzz_value

    def fuzz_and_add_parameter(self):
        if self.field_info.enum:
            self.parameter = self.field_info.field_name + '=' + str(random.choice(self.field_info.enum))
        elif self.field_info.format:
            if self.field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
                self.parameter = self.field_info.field_name + '=' + \
                     str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                     datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(microsecond=0)).isoformat())
        else:
            if self.field_info.field_type == 'boolean':
                self.parameter = self.field_info.field_name + '=' + random.choice(['true', 'false'])
            elif self.field_info.field_type == 'string':
                self.parameter = self.field_info.field_name + '=' + random_str()
            elif self.field_info.field_type == 'integer':
                self.parameter = self.field_info.field_name + '=' + str(random.randint(0, 50))
        if self.field_info.location == 0:
            self.new_url = self.base_url.replace('{' + self.field_info.field_name + '}', self.parameter)
        else:
            self.new_url = self.base_url + '&' + self.parameter
        pass

    def judge_effective(self):
        response_status = requests.get(self.new_url).status_code
        if 300 > response_status >= 200:
            self.request_response = json.loads(requests.get(self.new_url).text)
            if not self.request_response:
                self.responses_status = 0
            else:
                self.responses_status = 1
        elif 500 > response_status >= 300:
            self.responses_status = 0
        elif 500 == response_status:
            print('find bug in %s' % self.base_url)
            self.responses_status = 0
        return self.responses_status
        pass

    def add_token(self):
        # 加上token 因为暂时不考虑token的问题 所以在第一步就加上token
        # if '?' in url:
        #     url = url + '&private_token=n19y6WJgSgjyDuFSHMx9'
        #     # ehWyDYxYMRcFLKCRryeK root token
        # else:
        self.base_url = self.base_url + '?private_token=n19y6WJgSgjyDuFSHMx9'

    def exec(self):
        for i in range(1, 10):
            self.fuzz_and_add_parameter()
            if self.judge_effective():
                self.request_response = json.loads(requests.get(self.new_url).text)
                self.responses_status = 1
                break
        if not self.judge_effective():
            print('fuzz %s %s fail' % (self.base_url, self.field_info.field_name))
            self.responses_status = 0