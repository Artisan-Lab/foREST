from foREST_setting import foRESTSetting
import argparse
from log.get_logging import *
from entity.resource_pool import ResourcePool
from module.foREST_monitor.foREST_monitor import foRESTMonitor
from module.parser.api_parser import *
from module.testing.testing import TestingMonitor


if __name__ == "__main__":
    # command-line arguments
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--time_budget',
                            help='Testing run time in hours '
                                 f'(default 1 hours)',
                            type=float, default=1, required=False)
    arg_parser.add_argument('--api_file_path',
                            help='The read path of the API documentation',
                            type=str, required=True)
    arg_parser.add_argument('--settings_file',
                            help='Custom user settings file path',
                            type=str, default='', required=False)
    arg_parser.add_argument('--target_ip',
                            help='service under testing ip',
                            type=str)
    arg_parser.add_argument('--out_put',
                            help='log out put dirt',
                            type=str
                            )
    args = arg_parser.parse_args()

    # convert the command-line arguments to a dict
    args_dict = vars(args)

    # combine settings from settings file to the command-line arguments
    if args.settings_file:
        try:
            with open(args.settings_file, "r") as file:
                setting_file = json.load(file)
            args_dict.update(setting_file)
        except Exception as error:
            print(f"\n Argument Error::\n\t{error!s}")
            sys.exit(-1)

    # configure restler setting and start monitor
    foREST_settings = foRESTSetting(args_dict)
    foREST_monitor = foRESTMonitor()

    set_out_put(foREST_settings.out_put)
    # parsing API file
    foREST_log.save_and_print("Start parsing API file")
    APIListParser().parsing_api_file(foREST_settings.api_file_path)
    foREST_monitor.api_list = api_list_parser().api_list
    api_list = foREST_monitor.api_list
    foREST_log.save_and_print(f"Finish parsing API file, {api_list_parser().len} API identified")

    # Initialize the resource pool
    resource_pool = ResourcePool(api_list)
    foREST_monitor.resource_pool = resource_pool

    # api dependency analysis
    foREST_log.save_and_print("Start dependency analysis")
    no_reference_field = api_list_parser().foREST_dependency_analysis()
    foREST_log.save_and_print(f"Dependency analysis done, "
                              f"{len(no_reference_field)} parameter dependencies could not be found")

    # start time monitor
    foREST_log.save_and_print("start testing")
    foREST_monitor.create_time_monitor(foREST_settings.time_budget)
    foREST_monitor.start_time_monitor()

    testing_monitor = TestingMonitor(api_list_parser().root)
    testing_monitor.foREST_tree_based_bfs()
    foREST_monitor.time_monitor.terminate()

