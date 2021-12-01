from open_api_parse.parser import Parser
import os
from tool.tools import Tool
from testing_render.testing import Test
import datetime
from dependency.dependency import Dependency


start_time = datetime.datetime.now()
open_api_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.\\openapi\\' +
                                  Tool.readconfig('api_file', 'file_path'))
open_api_parser = Parser(path=open_api_file_path)
open_api_list = open_api_parser.get_api_list
semantic_tree_root = Dependency(open_api_list)
test_process = Test(semantic_tree_root, open_api_list, set_traverse_nums=2)
test_process.foREST_BFS()
end_time = datetime.datetime.now()
success_api_number = 0
for i in test_process.success_pool:
    success_api_number += i
print('API coverage(success/total): %d/%d' %(success_api_number, test_process.api_number))
print('runtime ' + str(end_time - start_time))
