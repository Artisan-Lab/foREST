import requests
import random
from datetime import datetime
import json
from metamorphic.fuzz_and_judge import random_str
from metamorphic.fuzz_and_judge import random_date
import

fuzz_times = 10


class Fuzz:
    # 基本Fuzz模块
    fuzz_value = None
    request_response = None
    default = None
    format = None
    type = None
    enum = None
    key = None
    base_url = None
    new_url = None
    location = None
    responses_status = 0
    response = None

    def __init__(self):
        pass

    def set_enum(self, enum):
        self.enum = enum

    def get_enum(self):
        # 返回参数的枚举值
        return self.enum

    def set_default(self, default):
        self.default = default

    def get_default(self):
        # 返回参数默认值
        return str(self.default)

    def set_format(self, parameter_format):
        self.format = parameter_format

    def get_format(self):
        # 返回参数格式
        return str(self.format)

    def set_type(self, parameter_type):
        self.type = parameter_type

    def get_type(self):
        # 返回参数类型
        return str(self.type)

    def set_key(self, key):
        self.key = key

    def get_key(self):
        # 返回参数名
        return str(self.key)

    def fuzz_by_format(self):
        # 基于参数的格式进行fuzz
        parameter_format = self.get_format()
        if parameter_format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
            self.fuzz_value = str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                              datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(
                                                  microsecond=0)).isoformat())

    def fuzz_by_enum(self):
        # 基于枚举进行fuzz
        self.fuzz_value = str(random.choice(self.enum))

    def fuzz_string(self):
        # 随机字符串
        self.fuzz_value = random_str()

    def fuzz_boolean(self):
        # 随机布尔值
        self.fuzz_value = random.choice(['True', 'false'])

    def fuzz_integer(self):
        # 随机整数
        self.fuzz_value = str(random.randint(0, 50))

    def set_fuzz_value(self, value):
        self.fuzz_value = value

    def get_fuzz_value(self):
        # 返回fuzz后的值
        return self.fuzz_value

    def set_location(self, location):
        self.location = location

    def compose_url(self):
        # 编写url
        if self.location == 0:
            self.new_url = self.base_url.replace('{' + self.key+ '}', self.fuzz_value)
        elif self.location == 1:
            self.new_url = self.base_url + '&' + self.key + '=' + self.fuzz_value

    def get_new_url(self):
        # 返回全新的url
        return self.new_url

    def is_effect(self):
        # 判断url是否有效
        response_status = requests.get(self.new_url).status_code
        if 300 > response_status >= 200:
            self.request_response = json.loads(requests.get(self.new_url).text)
            if self.request_response:
                self.responses_status = 1
            else:
                self.responses_status = 0
        elif 500 > response_status >= 300:
            self.responses_status = 0
        elif 500 == response_status:
            print('\033[31m find bug in %s' % self.new_url)
            self.responses_status = 0

    def get_response(self):
        return self.request_response

    def get_response_status(self):
        # 返回响应的状态
        return self.responses_status


class ResponseInfo:

    def __init__(self ,key ,value ,response):
        self.key = key
        self.value = value
        self.response = response


class GetSingleParameterResponses:

    def __init__(self, field_info, times, base_url):
        self.field_info = field_info
        self.times = times
        self.base_url = base_url
        self.new_url = base_url
        self.enum_responses = []
        self.default_responses = []
        self.responses = []

    def get_all_responses(self):
        fuzz_unit = Fuzz()
        fuzz_unit.set_location(self.field_info.location)
        parameter_name = self.field_info.field_name
        enums = self.field_info.enum
        default = self.field_info.default
        parameter_format = self.field_info.format
        parameter_type = self.field_info.field_type
        if enums:
            for enum in enums:
                fuzz_unit.set_key(parameter_name)
                fuzz_unit.set_fuzz_value(enum)
                fuzz_unit.compose_url()
                fuzz_unit.is_effect()
                if fuzz_unit.get_response_status():
                    self.enum_responses.append(ResponseInfo(parameter_name ,enum ,fuzz_unit.get_response()))
                else:
                    print('%s enum value error' %fuzz_unit.get_new_url())
        if default:
            fuzz_unit.set_key(parameter_name)
            fuzz_unit.set_fuzz_value(default)
            fuzz_unit.compose_url()
            fuzz_unit.is_effect()
            if fuzz_unit.get_response_status():
                self.default_responses.append(ResponseInfo(parameter_name, default, fuzz_unit.get_response()))
            else:
                print('%s default value error' % fuzz_unit.get_new_url())
        if parameter_type:
            if parameter_format:
                fuzz_unit.set_key(parameter_name)
                fuzz_unit.set_format(parameter_format)
                for i in range(fuzz_times):
                    fuzz_unit.fuzz_by_format()
                    fuzz_unit.compose_url()
                    fuzz_unit.is_effect()
                    if fuzz_unit.get_response_status():
                        self.responses.append(
                            ResponseInfo(parameter_name, fuzz_unit.get_fuzz_value(), fuzz_unit.get_response()))
            else:
                fuzz_unit.set_key(parameter_name)
                fuzz_unit.set_type(parameter_type)
                if parameter_type == 'string':
                    for i in range(fuzz_times):
                        fuzz_unit.fuzz_string()
                        fuzz_unit.compose_url()
                        fuzz_unit.is_effect()
                        if fuzz_unit.get_response_status():
                            self.responses.append(
                                ResponseInfo(parameter_name, fuzz_unit.get_fuzz_value(), fuzz_unit.get_response()))
                elif parameter_type == 'integer':
                    for i in range(fuzz_times):
                        fuzz_unit.fuzz_integer()
                        fuzz_unit.compose_url()
                        fuzz_unit.is_effect()
                        if fuzz_unit.get_response_status():
                            self.responses.append(
                                ResponseInfo(parameter_name, fuzz_unit.get_fuzz_value(), fuzz_unit.get_response()))
                elif parameter_type == 'boolean':
                    fuzz_unit.set_fuzz_value('True')
                    fuzz_unit.compose_url()
                    fuzz_unit.is_effect()
                    if fuzz_unit.get_response_status():
                        self.responses.append(
                            ResponseInfo(parameter_name, 'True', fuzz_unit.get_response()))
                    else:
                        print('%s fuzz boolean error' % fuzz_unit.get_new_url())
                    fuzz_unit.set_fuzz_value('False')
                    fuzz_unit.compose_url()
                    fuzz_unit.is_effect()
                    if fuzz_unit.get_response_status():
                        self.responses.append(
                            ResponseInfo(parameter_name, 'False', fuzz_unit.get_response()))
                    else:
                        print('%s fuzz boolean error' % fuzz_unit.get_new_url())

    def get_responses(self):
        return self.responses

    def get_default_responses(self):
        return self.default_responses

    def get_enum_response(self):
        return self.enum_responses


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/openapi.yaml")
    api_list = parse.get_api_info(1, path)
    print(1)
#

if __name__ == '__main__':
    main()