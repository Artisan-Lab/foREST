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


class FuzzAndJudgeUnit:
    parameter = None
    responses_status = None
    request_response = None
    req_field_names = None
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
        a = requests.get(self.new_url).text
        self.request_response = json.loads(a)
        response_status = requests.get(self.new_url).status_code
        if 300 > response_status >= 200:
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
            print(self.base_url + '  ' + self.field_info.field_name + 'may has problem')
            self.responses_status = 0
