import json
from entity.logpool import log_pool
from module.data_analysis.log_parser.log_parser import JsonParser
from module.data_analysis.log_parser.foREST_log_parser import foREST_log_parser
from module.data_analysis.find_dependency import FindDependency


def data_analysis(log_type, log_path, save_type):
    if log_type == "json":
        with open(log_path, 'r') as log_file:
            log_data = json.load(log_file)
        JsonParser(log_data)
        with open('structure.json', 'r') as structure_file:
            structure_data = json.load(structure_file)
        log_pool.save_log(log_data, structure_data)
    elif log_type == "foREST":
        foREST_log_parser(log_path)
    else:
        raise Exception(f"unsupported log file type {log_type}")
    log_dependency_analysis = FindDependency(save_type)
    return log_dependency_analysis.result

if __name__ == '__main__':
    data_analysis("foREST", "E:\\code\\restful_test\\experiment\\foREST\\project_1\\logs\\2xx_request", "rbtree")