from open_api_parse.parser import Parser
from common.dependency.semantictree import CreateSemanticTree
import os
from tool.tools import Tool

open_api_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.\\openapi\\' + Tool.readconfig('api_file', 'file_path'))

open_api_parser = Parser(path=open_api_file_path)
open_api_list = open_api_parser.get_api_list()
Tool.save_api_list(open_api_list)
semantic_tree = CreateSemanticTree(open_api_list)
semantic_tree.create_tree()
print(1)
