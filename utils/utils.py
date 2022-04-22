import os
import json
import random
import re



class Tool:

    @staticmethod
    def list_de_duplicate(list1):
        temp = []
        for item in list1:
            if not item in temp:
                temp.append(item)
        return temp

    @staticmethod
    def read_json_file(file_path):
        with open(file_path, 'r') as json_file:
            load_dict = json.load(json_file)
        return load_dict

    @staticmethod
    def save_api_list(open_api_list):
        pattern = re.compile(r'([a-z]*)', re.I)
        file_name = pattern.match(Tool.read_config('api_file', 'file_path'))[0]
        cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
        path = os.path.join(os.path.dirname(cur_path), './log/api_list')
        if not os.path.exists(path):
            os.mkdir(path)  # 如果不存在这个logs文件夹，就自动创建一个
        jst = json.dumps(open_api_list, default=lambda o: o.__dict__, indent=4)
        if not os.path.isfile(path + '/' + file_name + '.json'):
            with open(path + '/' + file_name + '.json', 'w') as f:
                f.write(jst)

    # @staticmethod
    # def save_resource_pool(resource_pool):
    #     pattern = re.compile(r'([a-z]*)', re.I)
    #     file_name = pattern.match(Tool.read_config('api_file', 'file_path'))[0]
    #     cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
    #     path = os.path.join(os.path.dirname(cur_path), './log/resource')
    #     if not os.path.exists(path):
    #         os.mkdir(path)  # 如果不存在这个logs文件夹，就自动创建一个
    #     jst = json.dumps(resource_pool, default=lambda o: o.__dict__, indent=4)
    #     if not os.path.isfile(path + '/' + file_name + '.json'):
    #         with open(path + '/' + file_name + '.json', 'w') as f:
    #             f.write(jst)

    @staticmethod
    def save_no_reference(no_reference_key):
        cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
        path = os.path.join(os.path.dirname(cur_path), './log/no_reference_key')
        file_name = 'no_reference_key'
        if not os.path.exists(path):
            os.mkdir(path)  # 如果不存在这个logs文件夹，就自动创建一个
        with open(path + '/' + file_name + '.json', 'w') as f:
            f.write(str(no_reference_key))

    @staticmethod
    def random_dic(dicts):
        dict_key_ls = list(dicts.keys())
        random.shuffle(dict_key_ls)
        new_dic = {}
        for key in dict_key_ls:
            new_dic[key] = dicts.get(key)
        return new_dic


ANNOTATION_TABLE = Tool.read_json_file('./annotation_table.json')
EXTERNAL_KEY_DICT = Tool.read_json_file('./external_key.json')