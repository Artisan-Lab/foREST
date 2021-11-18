from dependency.open_api_parse.parser import Parser
from dependency.semantictree import CreateSemanticTree
import os
from tool.tools import Tool
from testing_render.testing import Test
import datetime


starttime = datetime.datetime.now()
open_api_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.\\openapi\\' + Tool.readconfig('api_file', 'file_path'))
open_api_parser = Parser(path=open_api_file_path)
open_api_list = open_api_parser.get_api_list
Tool.save_api_list(open_api_list)
semantic_tree = CreateSemanticTree(open_api_list)
semantic_tree.create_tree()
test_process = Test(semantic_tree.root, open_api_list, set_traverse_nums=2)
test_process.foREST_BFS()
end_time = datetime.datetime.now()
print('runtime ' + str(end_time-starttime))
