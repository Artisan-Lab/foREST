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
                       # '(^&%GBH#T$G"""""""""""DFHBD"BDGVDFVWEF$$53346542@##@$#@%$##',
                       # '2012-10-22T14:13:35Z',
                       # '/uploads/-/system/appearance/logo/1/logo.png',
                       # '#e75e40',
                       # '5832fc6e14300a0d962240a8144466eef4ee93ef0d218477e55f11cf12fc3737'
                       # 'ee1dd64b6adc89cf7e2c23099301ccc2c61b441064e9324d963c46902a85ec34',
                       '127.0.0.1']

        return random.choice(list_string)
    elif 'boolean' == type:
        list_boolean = ['False', 'True']
        return random.choice(list_boolean)