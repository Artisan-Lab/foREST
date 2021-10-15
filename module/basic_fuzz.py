import random
from datatime import timedelta, datetime
import json
import sys

random_integer = [1, 2, 0, 3, -45, -81, sys.maxsize, -sys.maxsize-1, sys.float_info.min]

def random_date(start, end):
    delta = end - start
    int_delta = (delta.day * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)



def random_str(slen=10):
    seed =  "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_=+-"
    list_string = ["string", "long string", "email:1@gmail.com"]
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    random_string = random.choice(list_string)
    return random.choice([''.join(sa), random_string])


class BasicFuzz:

    @staticmethod
    def fuzz_integer(field_info):
        integer_max = 100
        integer_min = 0
        if field_info.max:
            integer_max = field_info.max
        if field_info.min:
            integer_min = field_info.min
        fuzz_value = random.randint(integer_min, integer_max)
        return fuzz_value

    @staticmethod
    def fuzz_string(field_info, string_len=10):
        if field_info.format:
            if field_info.format == 'ISO 8601 YYYY-MM0DDTHH:MM:SSZ':
                fuzz_value = str(random_date(datetime(2019, 1, 1, 0, 0, 0).astimezone().replace(microsecond=0),
                                             datetime(2021, 12, 31, 23, 59, 59).astimezone().replace(microsecond=0).
                                             isoformat()))
            else:
                print('please add format %s' % field_info.format)
                field_info.format = None
                fuzz_value = random_str(string_len)
        else:
            fuzz_value = random_str(string_len)
        return fuzz_value

    @staticmethod
    def fuzz_boolean():
        return random.choice(['True', 'False'])

    @staticmethod
    def fuzz_value(field_info):
        if field_info.field_type == 'boolean':
            return BasicFuzz.fuzz_boolean()
        elif field_info.field_type == 'string':
            return BasicFuzz.fuzz_string(field_info)
        elif field_info.field_type == 'integer':
            return BasicFuzz.fuzz_integer(field_info)

    @staticmethod
    def fuzz_value_from_type(field_type):
        pass
