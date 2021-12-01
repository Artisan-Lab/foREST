import json
import yaml
import jsonref
from open_api_parse.swagger_parser import SwaggerParser
from open_api_parse.open_api_parser import OpenAPIParser


class Parser:

    def __init__(self, path):
        with open(path, encoding='utf-8') as stream:
            yaml_data = yaml.safe_load(stream)
        # 此处如果yaml文件有问题，会报错）
        self.json_data = jsonref.loads(json.dumps(yaml_data))
        self.api_list = []
        if self.json_data.get('swagger'):
            self.version = 'swagger'
            swagger_parser = SwaggerParser(self.json_data)
            self.api_list = swagger_parser.swagger_parser()
        else:
            self.version = 'openapi'
            open_api_parser = OpenAPIParser(self.json_data)
            self.api_list = open_api_parser.openAPI_parser()

    @property
    def get_api_list(self):
        return self.api_list

