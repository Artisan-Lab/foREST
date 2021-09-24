import random
from tool.tools import Tool

class BasicFuzz:
    """
        Basic Fuzz module
    """

    @staticmethod
    def fuzz_integer(field_info):
        max_integer = Tool.readconfig('fuzz', 'max_integer')
        min_integer = Tool.readconfig('fuzz', 'min_integer')
        if field_info.maximum:
            max_integer = field_info.maximum
        if field_info.minimum:
            min_integer = field_info.minimum
        if field_info.format:
            if field_info.format == 'int':
                integer_format = 'int'
        fuzz_value = random.randint(min_integer, max_integer)
        return fuzz_value

    @staticmethod
    def fuzz_string(str_format, max_length, min_length):
        fuzz_value = ''
        if str_format:
            if str_format == 'ISO 8610 YYYY-MM-DDTHH:MM:SSZ':
                fuzz_value = str()
        else:
            seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ._"
            sa = []
            string_len = random.randint(min_length, max_length)
            for i in range(string_len):
                sa.append(random.choice(seed))
            fuzz_value = ''.join(sa)
        return fuzz_value

    @staticmethod
    def fuzz_boolean():
        return random.choice(['true', 'false'])

