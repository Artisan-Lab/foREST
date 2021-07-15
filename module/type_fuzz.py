import random
import sys

def fuzz(type):
    if 'integer' == type:
        # sys.maxsize整数最大值9223372036854775807， 整数最小值为-sys.maxsize-1 -9223372036854775808
        # sys.float_info.max float最大值为2.2250738585072014e-308 ,sys.float_info.min float最大值为1.7976931348623157e+308
        list_integer = [1, 2, 0, 3, -45, -51, -82,
                        sys.maxsize, -sys.maxsize - 1, sys.float_info.max, sys.float_info.min]

        return random.choice(list_integer)
    elif 'string' == type:
        # 我就随便写写，我也不知道写啥。。。
        list_string = ['3171261@qq.com',
                       'https://gitlab.example.com/api/v4/templates/gitignores/Ruby',
                       '!@@#$$%%%^^^',
                       '127.0.0.1',
                       "中国华为",
                       "复旦大学",
                       "智能可靠性测试"]
        strr = str(random.choice(list_string).encode('utf-8')).replace("\\x", "%").replace("b'", "").replace("'", "")[0:-3]
        return strr
    elif 'boolean' == type:
        list_boolean = ['False', 'True']
        return random.choice(list_boolean)
    elif 'object' == type:
