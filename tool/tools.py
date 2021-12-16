import os
import json
import re
import configparser
import nltk


class Tool:

    @staticmethod
    def list_de_duplicate(list1):
        temp = []
        for item in list1:
            if not item in temp:
                temp.append(item)
        return temp

    @staticmethod
    def readconfig(title, key):
        conf = configparser.ConfigParser()
        root_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../FoREST_config.conf")
        conf.read(root_path)
        return conf.get(title, key)

    @staticmethod
    def save_api_list(open_api_list):
        pattern = re.compile(r'([a-z]*)', re.I)
        file_name = pattern.match(Tool.readconfig('api_file', 'file_path'))[0]
        cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
        path = os.path.join(os.path.dirname(cur_path), './log/api_list')
        if not os.path.exists(path):
            os.mkdir(path)  # 如果不存在这个logs文件夹，就自动创建一个
        jst = json.dumps(open_api_list, default=lambda o: o.__dict__, indent=4)
        if not os.path.isfile(path + '/' + file_name + '.json'):
            with open(path + '/' + file_name + '.json', 'w') as f:
                f.write(jst)

    @staticmethod
    def save_no_reference(no_reference_key):
        cur_path = os.path.dirname(os.path.realpath(__file__))  # log_path是存放日志的路径
        path = os.path.join(os.path.dirname(cur_path), './log/no_reference_key')
        file_name = 'no_reference_key'
        if not os.path.exists(path):
            os.mkdir(path)  # 如果不存在这个logs文件夹，就自动创建一个
        with open(path + '/' + file_name + '.json', 'w') as f:
            f.write(str(no_reference_key))


token = Tool.readconfig('service', 'token')
send_timeout = Tool.readconfig('request', 'send_timeout')
received_timeout = Tool.readconfig('request', 'received_timeout')
sno = nltk.stem.SnowballStemmer('english')