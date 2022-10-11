import json
import yaml
from typing import Union
import jsonref
from entity.api_info import APIInfo
from module.parser.dependency import SemanticTree, SetKeyValueDependency
from .swagger_parser import SwaggerParser
from .open_api_parser import OpenAPIParser
import re

pattern = re.compile(r'{.*}')


def match_identifier(identifier_1, identifier_2):
    method_1, path_1 = identifier_1.split()
    method_2, path_2 = identifier_2.split()
    if method_1.lower() != method_2.lower():
        return False
    path_1_list = path_1.split("/")[::-1]
    path_2_list = path_2.split("/")[::-1]
    if len(path_1_list) != len(path_2_list):
        return False
    for i in range(len(path_2_list)):
        if path_1_list[i] == path_2_list[i] or \
                (re.search(pattern, path_1_list[i]) and re.search(pattern, path_2_list[i])):
            continue
        else:
            return False
    else:
        return True


class APIListParser(object):
    __instance = None

    @staticmethod
    def Instance():
        return APIListParser.__instance

    def __init__(self):
        if APIListParser.__instance:
            return
        self._api_list = None
        self._root = None
        self._len = 0
        APIListParser.__instance = self

    def parsing_api_file(self, path):
        """

        @param path: api file absolute path
        @type path: str
        """
        # Parsing the reference in the document

        with open(path, encoding='utf-8') as stream:
            if path.endswith(".yaml"):
                yaml_data = yaml.safe_load(stream)
                json_data = jsonref.loads(json.dumps(yaml_data))
            elif path.endswith(".json"):
                stream = json.load(stream)
                SwaggerParser.resolve_circular_references(stream)
                json_data = jsonref.loads(json.dumps(stream))
            else:
                raise Exception("Error API file format")

        # Use different parsing schemes for different document versions
        if json_data.get('swagger'):
            swagger_parser = SwaggerParser(json_data)
            self._api_list = swagger_parser.swagger_parser()
        else:
            open_api_parser = OpenAPIParser(json_data)
            self._api_list = open_api_parser.openAPI_parser()
        self._len = len(self._api_list)


    def find_api_by_identifier(self, api_identifier) -> Union[APIInfo, None]:
        for api_info in self._api_list:  # type: APIInfo
            if match_identifier(api_info.identifier, api_identifier):
                return api_info
        else:
            return None

    @property
    def len(self) -> int:
        return self._len

    def foREST_dependency_analysis(self):
        semantic_tree = SemanticTree(self._api_list)
        self._root = semantic_tree.root
        key_value_parser = SetKeyValueDependency(self._api_list)
        key_value_parser.get_dependency()
        return key_value_parser.not_reference_field
    
    @property
    def api_list(self) -> [APIInfo]:
        return self._api_list

    @property
    def root(self):
        return self._root


def api_list_parser() -> APIListParser:
    return APIListParser.Instance()
