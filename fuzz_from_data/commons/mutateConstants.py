STRINGS_FOR_MUTATED = ['<sql>', '<script>', '</>', '<html>', 'or', '\/', '<php', '</>', '</script>', b'0x\ussssxxx']
INTEGERS_FOR_MUTATED = [2 ** 63 - 1, -2 ** 63 - 1]
with open('/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/commons/mutateConstants.txt', 'r') as f:
    lines = f.readlines()
    for l in lines:
        STRINGS_FOR_MUTATED.append(l)
