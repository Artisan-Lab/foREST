import json
import yaml
import jsonref
from entity.api_info import api_info
from module.parser.open_api_parse.swagger_parser import SwaggerParser
from module.parser.open_api_parse.open_api_parser import OpenAPIParser


class APIList:
    __instance = None

    def __init__(self):
        if self.__instance:
            return
        self._api_list = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __getitem__(self, item):
        """

        @param item: api id
        @type item: int
        @return: api info
        @rtype: api_info
        """
        if isinstance(item, int) and 0 <= item < len(self._api_list):
            return self._api_list[item]
        else:
            raise Exception("API id index error")

    def parsing_api_file(self, path):
        """

        @param path: api file absolute path
        @type path: str
        """
        with open(path, encoding='utf-8') as stream:
            yaml_data = yaml.safe_load(stream)

        # Parsing the reference in the document
        json_data = jsonref.loads(json.dumps(yaml_data))

        # Use different parsing schemes for different document versions
        if json_data.get('swagger'):
            swagger_parser = SwaggerParser(json_data)
            self._api_list = swagger_parser.swagger_parser()
        else:
            open_api_parser = OpenAPIParser(json_data)
            self._api_list = open_api_parser.openAPI_parser()



