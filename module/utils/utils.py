import os
import json
import random


def get_value_from_external(annotation_table, api_path, api_method, field_name, location):
    if api_path in annotation_table:
        if api_method in annotation_table[api_path]:
            for external_key in annotation_table[api_path][api_method]:
                if external_key[field_name] == field_name and external_key[location] == location:
                    return external_key['value']
    return None


def get_key_from_annotation_key_table(annotation_key_table, api_path, api_method, field_name, location):
    if api_path in annotation_key_table:
        if api_method in annotation_key_table[api_path]:
            for external_key in annotation_key_table[api_path][api_method]:
                if external_key['field_name'] == field_name and external_key['location'] == location:
                    return external_key['real_field_name']
    return None


def is_path_variable(_str):
    if _str[0] == '{' and _str[-1] == '}' and len(_str)>2:
        return _str[1:-2]
    else:
        return False


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as json_file:
            load_dict = json.load(json_file)
        return load_dict
    except:
        return None


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


def find_field_in_dic(dic, field_name, field_type):
    if isinstance(dic, dict):
        for key in dic:
            if key == field_name and type(dic[key]).__name__ == field_type:
                value = dic[key]
                return value
            else:
                value = find_field_in_dic(dic[key], field_name, field_type)
                if value:
                    return value
    elif isinstance(dic, list):
        if (dic is not None) and (len(dic) > 0) and isinstance(dic[0], dict):
            for sub_dic in dic:
                value = find_field_in_dic(sub_dic, field_name, field_type)
                if value:
                    return value
    return None