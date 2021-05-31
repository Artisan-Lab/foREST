import requests
import random
from datetime import timedelta, datetime
import json


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
    return ''.join(sa)


class Fuzz:
    fuzz_value = None
    request_response = None

    def __init__(self, field_info, base_url):
        self.field_info = field_info
        self.default = field_info.default
        self.format = field_info.format
        self.type = field_info.field_type
        self.enum = field_info.enum
        self.parameter_name = field_info.field_name
        self.base_url = base_url
        self.new_url = base_url
        self.location = field_info.location
        self.responses_status = 0

    def get_enum(self):
        return self.enum

    def get_default(self):
        return str(self.default)

    def get_format(self):
        return str(self.format)

    def get_type(self):
        return str(self.type)

    def get_key(self):
        return str(self.parameter_name)

    def fuzz_by_format(self):
        parameter_format = self.get_format()
        if parameter_format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
            self.fuzz_value = str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                              datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(
                                                  microsecond=0)).isoformat())

    def fuzz_by_enum(self):
        self.fuzz_value = str(random.choice(self.enum))

    def fuzz_by_string(self):
        self.fuzz_value = random_str()

    def fuzz_by_boolean(self):
        self.fuzz_value = random.choice(['True', 'false'])

    def fuzz_by_integer(self):
        self.fuzz_value = str(random.randint(0, 50))

    def get_fuzz_value(self):
        return self.fuzz_value

    def compose_url(self):
        if self.location == 0:
            self.new_url = self.base_url.replace('{' + self.parameter_name+ '}', self.fuzz_value)
        elif self.location == 1:
            self.new_url = self.base_url + '&' + self.parameter_name + '=' + self.fuzz_value

    def get_new_url(self):
        return self.new_url

    def is_effect(self):
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
            print('\033[31m find bug in %s' % self.new_url)
            self.responses_status = 0

    def get_response_status(self):
        return self.responses_status



class FuzzAndJudgeUnit:
    parameter = None
    responses_status = None
    request_response = None
    new_url = None

    def __init__(self, field_info, base_url):
        self.field_info = field_info
        self.base_url = base_url

    def fuzz_and_add_parameter(self):
        if self.field_info.enum:
            self.parameter = self.field_info.field_name + '=' + str(random.choice(self.field_info.enum))
        elif self.field_info.format:
            if self.field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
                self.parameter = self.field_info.field_name + '=' + \
                                 str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                                 datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(
                                                     microsecond=0)).isoformat())
        else:
            if self.field_info.field_type == 'boolean':
                self.parameter = self.field_info.field_name + '=' + random.choice(['true', 'false'])
            elif self.field_info.field_type == 'string':
                self.parameter = self.field_info.field_name + '=' + random_str()
            elif self.field_info.field_type == 'integer':
                self.parameter = self.field_info.field_name + '=' + str(random.randint(0, 50))
        if self.field_info.location == 0:
            self.new_url = self.base_url.replace('{' + self.field_info.field_name + '}', self.parameter)
        elif self.field_info.location == 1:
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