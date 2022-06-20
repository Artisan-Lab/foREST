import json
from entity.logpool import log_pool
from module.parser.log_parser.jsonparser import JsonParser
from module.parser.log_parser.foREST_log_parser import foREST_log_parser
from find_dependency import FindDependency


def main():
    with open('log.json', 'r') as log_file:
        log_data = json.load(log_file)
    JsonParser(log_data)
    with open('structure.json', 'r') as structure_file:
        structure_data = json.load(structure_file)
    # log_pool.save_log(log_data, structure_data)
    # log_pool.user_classification()
    foREST_log_parser('./logs/2xx_request')
    for log in log_pool.log_list:
        for api_info in api_list:
            if api_info.path == log.path:
                log.set_api_id(api_info.api_id)
    log_dependency_analysis = FindDependency()




if __name__ == '__main__':
    main()
