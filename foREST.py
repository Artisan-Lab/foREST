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
                                 f'(default {}',
                            type=str, required=True
                            )
    arg_parser.add_argument('--api_document_path', help='The read path of the API documentation'
                            f'(default {}'
                            )
    try:
        if len(sys.argv) <= 1:
            print(f'🍅 tomato {TESTING_TIME} minutes. Ctrl+C to exit')
            tomato(WORK_MINUTES, 'It is time to take a break')
            print(f'🛀 break {BREAK_MINUTES} minutes. Ctrl+C to exit')
            tomato(BREAK_MINUTES, 'It is time to work')

        elif sys.argv[1] == '-t':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
            print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to take a break')

        elif sys.argv[1] == '-b':
            minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
            print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
            tomato(minutes, 'It is time to work')

        elif sys.argv[1] == '-h':
            help()

        else:
            help()

    except KeyboardInterrupt:
        print('\n goodbye')
    except Exception as ex:
        print(ex)
        exit(1)

    foREST_monitor = foRESTMonitor()
    foREST_monitor.reset_start_time()
    foREST_monitor.set_time_budget(TESTING_TIME)

    open_api_file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.\\openapi\\' +
                                      Tool.read_config('api_file', 'file_path'))
    open_api_parser = Parser(path=open_api_file_path)
    open_api_list = open_api_parser.get_api_list
    semantic_tree_root = Dependency(open_api_list)
    test_process = Test(semantic_tree_root, open_api_list, foREST_monitor)
    test_process.foREST_tree_based_bfs()
    end_time = datetime.datetime.now()
    success_api_number = 0
    for i in test_process.success_pool:
        success_api_number += i
    print('API coverage(success/total): %d/%d' % (success_api_number, test_process.api_number))
    print('runtime %.3e' % foREST_monitor.running_time)
