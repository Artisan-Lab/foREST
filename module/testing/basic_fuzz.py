import random
import string
from datetime import timedelta
import sys

random_integer = [1, 2, 0, 3, -45, -81, sys.maxsize, -sys.maxsize-1, sys.float_info.min]
random_letter = string.ascii_letters


def random_str(slen=10):
    seed = "0123456789abcdefghijklmnopqrstuvwxyz"  #!@#$%^&*()_=+-
    list_string = ["string", "long_string", "email:1@gmail.com"]
    sa = []
    for i in range(slen):
        sa.append(random.choice(seed))
    random_string = random.choice(list_string)
    return random.choice([''.join(sa), random_string])


def str_replace(init_string, index, new_letter):
    new = []
    for s in init_string:
        new.append(s)
    new[index] = new_letter
    return ''.join(new)


class BasicFuzz:

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
    def fuzz_string(string_len=10):
        fuzz_value = random_str(string_len)
        return fuzz_value

    @staticmethod
    def fuzz_boolean():
        return random.choice(['True', 'False'])

    @staticmethod
    def fuzz_value_from_field(field_info):
        if field_info.enum:
            return random.choice(field_info.enum)
        if field_info.field_type == 'bool':
            return BasicFuzz.fuzz_boolean()
        elif field_info.field_type == 'str':
            return BasicFuzz.fuzz_string()
        elif field_info.field_type == 'int':
            return BasicFuzz.fuzz_integer()

    @staticmethod
    def fuzz_value_from_type(field_type):
        pass
