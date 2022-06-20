import os
import json
import random
import re
from foREST_setting import foRESTSettings


def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        load_dict = json.load(json_file)
    return load_dict


def list_de_duplicate(list1):
    temp = []
    for item in list1:
        if not item in temp:
            temp.append(item)
    return temp


def random_dic(dicts):
    dict_key_ls = list(dicts.keys())
    random.shuffle(dict_key_ls)
    new_dic = {}
    for key in dict_key_ls:
        new_dic[key] = dicts.get(key)
    return new_dic
