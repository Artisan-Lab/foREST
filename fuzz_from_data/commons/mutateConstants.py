import os

STRINGS_FOR_MUTATED = ['<sql>', '<script>', '</>', '<html>', 'or', '\/', '<php', '</>', '</script>', b'0x\ussssxxx']
INTEGERS_FOR_MUTATED = [2 ** 63 - 1, -2 ** 63 - 1]
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./mutateConstants.txt")
with open(path, 'r', encoding='UTF-8') as f:
    lines = f.readlines()
    for l in lines:
        STRINGS_FOR_MUTATED.append(l)
