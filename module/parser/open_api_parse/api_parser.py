import json
import yaml
import jsonref
from entity.api_info import APIInfo
from module.parser.open_api_parse.keyvaluedependency import SemanticTree, SetKeyValueDependency
from module.parser.open_api_parse.swagger_parser import SwaggerParser
from module.parser.open_api_parse.open_api_parser import OpenAPIParser


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
        self._len = len(self._api_list)

    def load_depend_info(self, depend_info):
        pass



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
