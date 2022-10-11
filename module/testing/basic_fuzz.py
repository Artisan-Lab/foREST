import random, time
import string
import sys
import numpy as np
from allpairspy import AllPairs
from xeger import Xeger

X = Xeger()
random_integer = [1, 2, 0, 3, -45, -81, sys.maxsize, -sys.maxsize-1, sys.float_info.min]
random_letter = string.ascii_letters
start = '2018-01-01T00:00:00'
end = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())


def strTimeProp(start, end, prop, frmt):
    stime = time.mktime(time.strptime(start, frmt))
    etime = time.mktime(time.strptime(end, frmt))
    ptime = stime + prop * (etime - stime)
    return int(ptime)


def randomDate(start, end, frmt='%Y-%m-%dT%H:%M:%S'):
    return time.strftime(frmt, time.localtime(strTimeProp(start, end, random.random(), frmt)))

def random_str(slen=0):
    ans = []
    number = "0123456789"
    char = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    symbol_ = "#!@$%^&*()_=+-"
    list_string = ["string", "long_string", "email:1@gmail.com", "%e6%99%ba%e8%83%bd%e5", "&#x6797;", r"\u01\u6D\u01\u6E\u01\u6F", r"\u01\u6", "",None]
    if np.random.choice([1, 0], replace=True, p=[0.5, 0.5]):
        return random.choice(list_string)
    seed = [number, char, symbol_]
    for j in seed:
        slen = random.randint(0, 5)
        for i in range(slen):
            ans.append(random.choice(j))
    if np.random.choice([1, 0], replace=True, p=[0.5, 0.5]):
        random.shuffle(ans)
    return "".join(ans)

def str_replace(init_string, index, new_letter):
    new = []
    for s in init_string:
        new.append(s)
    new[index] = new_letter
    return ''.join(new)


class BasicFuzz:

    @staticmethod
    def fuzz_float(min_float=0, max_float=100):
        fuzz_value = round(random.uniform(min_float, max_float), random.randint(0,5))
        return fuzz_value

    @staticmethod
    def fuzz_integer(integer_max=100, integer_min=0):
        fuzz_value = random.randint(integer_min, integer_max)
        return fuzz_value

    @staticmethod
    def fuzz_mutation_parameter(value):
        if len(value) > 3:
            mutation_character_number = random.randint(1, int(len(value)/2))
        else:
            mutation_character_number = len(value)
        for _ in range(mutation_character_number):
            mutation_index = random.randint(0, len(value)-1)
            if value[mutation_index].isdigit():
                value = str_replace(value, mutation_index, str(random.randint(0, 9)))
            if value[mutation_index].isalpha():
                value = str_replace(value, mutation_index, random.choice(random_letter))
        return value

    @staticmethod
    def fuzz_string(string_len=0):
        fuzz_value = random_str(string_len)
        return fuzz_value

    @staticmethod
    def fuzz_boolean():
        return random.choice(['True', 'False'])

    @staticmethod
    def fuzz_dict():
        value = {}
        for i in range(random.randint(0,5)):
            value[BasicFuzz.fuzz_string()] = random.choice([BasicFuzz.fuzz_string(), BasicFuzz.fuzz_integer()])
        return value

    @staticmethod
    def fuzz_list():
        value = {}
        for i in range(random.randint(0,5)):
            value[BasicFuzz.fuzz_string()] = random.choice([BasicFuzz.fuzz_string(), BasicFuzz.fuzz_integer()])
        return value

    @staticmethod
    def fuzz_value_from_field(field_info):
        if field_info.enum and random.choice([0, 1]):
            return random.choice(field_info.enum)
        if field_info.format and random.choice([0,1]):
            if field_info.format == 'date-time':
                return randomDate(start,end)+X.xeger("^\.[0-9]{3}\+0000")
        if field_info.pattern and random.choice([0,1]):
            try:
                return X.xeger(field_info.pattern)
            except:
                pass
        if random.choice([0,0,0,1]):
            return random.choice([BasicFuzz.fuzz_string(),
                                  BasicFuzz.fuzz_integer(),
                                  BasicFuzz.fuzz_float(),
                                  BasicFuzz.fuzz_boolean(),
                                  BasicFuzz.fuzz_list(),
                                  BasicFuzz.fuzz_dict()])
        if field_info.field_type == 'bool':
            return BasicFuzz.fuzz_boolean()
        elif field_info.field_type == 'str':
            return BasicFuzz.fuzz_string()
        elif field_info.field_type == 'int':
            return BasicFuzz.fuzz_integer()
        elif field_info.field_type == 'number':
            return BasicFuzz.fuzz_float()

