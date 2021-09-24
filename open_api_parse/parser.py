import json
import os
import yaml
import jsonref
from config.config import ReadConfig
from open_api_parse.swagger_parser import SwaggerParser
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), ReadConfig.readconfig('api_file', 'file_path'))


class Parser:

    def __init__(self, path):
        with open(path,encoding='utf-8') as stream:
            yaml_data = yaml.safe_load(stream)
        # 此处如果yaml文件有问题，会报错）
        self.json_data = jsonref.loads(json.dumps(yaml_data))
        if self.json_data.get('swagger'):
            self.version = 'swagger'
        else:
            self.version = 'openapi'


a = Parser(path)
b = SwaggerParser(a.json_data)
c = b.swagger_parser()
print(1)