import json
import sys

from foREST_setting import foRESTSetting, foRESTSettings
import argparse
# import datetime
# import os
from module.parser.open_api_parse.api_parser import APIList
from module.foREST_monitor.clock_monitor import TimeMonitor
from module.foREST_monitor.foREST_monitor import foRESTMonitor
# from module.open_api_parse.parser import Parser
# from module.testing.testing import Test
# from module.dependency.dependency import Dependency


if __name__ == "__main__":
    # command-line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--foREST_mode',
                            help='pure testing or data based testing'
                                 f'(default pure testing)',
                            type=str, default="pure testing", required=False)
    arg_parser.add_argument('--time_budget',
                            help='Testing run time in hours '
                                 f'(default 1 hours)',
                            type=float, default=1, required=False)
    arg_parser.add_argument('--token',
                            help='User identification code'
                                 f'(default',
                            type=str, required=False)
    arg_parser.add_argument('--api_file_path',
                            help='The read path of the API documentation',
                            type=str, required=True)
    arg_parser.add_argument('--settings_file',
                            help='Custom user settings file path',
                            type=str, default='', required=False)
    arg_parser.add_argument('--target_ip',
                            help='service under testing ip',
                            type=str)
    args = arg_parser.parse_args()

    # convert the command-line arguments to a dict
    args_dict = vars(args)

    # combine settings from settings file to the command-line arguments
    if args.settings_file:
        try:
            setting_file = json.load(open(args.settings_file))
            args_dict.update(setting_file)
        except Exception as error:
            print(f"\n Argument Error::\n\t{error!s}")
            sys.exit(-1)

    # configure foREST setting and start monitor
    foREST_settings = foRESTSetting(args_dict)
    foREST_monitor = foRESTMonitor()
    foREST_monitor.create_time_monitor(foREST_settings.time_budget)

    # parsing API file
    api_list = APIList()
    api_list.parsing_api_file(foREST_settings.api_file_path)


    semantic_tree_root = Dependency(open_api_list)
    test_process = Test(semantic_tree_root, open_api_list, foREST_monitor)
    # test_process.foREST_tree_based_bfs()
    # end_time = datetime.datetime.now()


