from open_api_parse.parser import Parser
import os
import sys
from utils.utils import Tool
from module.testing import Test
import datetime
from dependency.dependency import Dependency
from module.foREST_monitor import foRESTMonitor
from utils import foREST_setting
import argparse



if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--time_budget',
                            help='Testing run time in hours '
                                 f'(default {foREST_setting.TESTING_TIME} hours)',
                            type=float, default=foREST_setting.TESTING_TIME, required=False
                            )
    arg_parser.add_argument('--token',
                            help='User identification code'
                                 f'(default',
                            type=str, required=True
                            )
    arg_parser.add_argument('--api_document_path', help='The read path of the API documentation'
                            f'(default'
                            )

    foREST_monitor = foRESTMonitor()
    foREST_monitor.reset_start_time()
    foREST_monitor.set_time_budget(foREST_setting.TESTING_TIME)

    open_api_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.\\openapi\\' +
                                      foREST_setting.API_FILE_PATH)
    open_api_parser = Parser(path=open_api_file_path)
    open_api_list = open_api_parser.get_api_list
    semantic_tree_root = Dependency(open_api_list)
    test_process = Test(semantic_tree_root, open_api_list, foREST_monitor)
    test_process.foREST_tree_based_bfs()
    end_time = datetime.datetime.now()


