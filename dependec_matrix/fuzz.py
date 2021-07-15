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

    def __init__(self):
        pass

    @staticmethod
    def array_handle(array):
        array_list = []
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
    def object_handle(field_list):
        object_list = {}
        if field_list:
            for field_info in field_list:
                value = FuzzAndJudgeUnit.fuzz_value(field_info)
                object_list[field_info.field_name] = value
        return object_list

    @staticmethod
    def fuzz_value(field_info):
        if field_info.enum:
            fuzz_value = str(random.choice(field_info.enum))
        elif field_info.format:
            if field_info.format == 'ISO 8601 YYYY-MM-DDTHH:MM:SSZ':
                fuzz_value = str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                                 datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(
                                                     microsecond=0)).isoformat())
            else:
                print('please Add format %s' % field_info.format)
                field_info.format = None
                fuzz_value = FuzzAndJudgeUnit.fuzz_value(field_info)
        else:
            if field_info.field_type == 'boolean':
                fuzz_value = random.choice(['true', 'false'])
            elif field_info.field_type == 'string':
                fuzz_value = random_str()
            elif field_info.field_type == 'integer':
                fuzz_value = random.choice([1, 2, 0, 3, -45, -51, -82,
                        sys.maxsize, -sys.maxsize - 1, sys.float_info.max, sys.float_info.min])
            elif field_info.field_type == 'object':
                fuzz_value = FuzzAndJudgeUnit.object_handle(field_info.object)
            elif field_info.field_type == 'array':
                fuzz_value = FuzzAndJudgeUnit.array_handle(field_info.array)
            else:
                fuzz_value = None
        return fuzz_value

