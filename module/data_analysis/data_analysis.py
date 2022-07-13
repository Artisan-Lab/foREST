import json, os
from module.data_analysis.logpool import log_pool
from module.data_analysis.log_parser.log_parser import JsonParser
from module.data_analysis.log_parser.foREST_log_parser import foREST_log_parser
from module.data_analysis.parameter_dependency import FindParameterDependency
from module.data_analysis.api_dependency import api_dependency
from module.foREST_monitor.sequence_monitor import SequenceMonitor


def data_analysis(log_type, log_path, save_path, max_sequence_length):
    sequence_monitor = SequenceMonitor()
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
    log_dependency_analysis = FindParameterDependency(max_sequence_length)

    result = log_dependency_analysis.result
    api_dependency(max_sequence_length)

    for api in result:
        for parameter in result[api]:
            tmp = sorted(result[api][parameter].items(), key=lambda s: s[1], reverse=True)
            result[api][parameter] = {}
            for i, (key, value) in enumerate(tmp):
                if i > 4:
                    break
                result[api][parameter][key] = value
    with open(os.path.join(save_path, "parameter_dependency.json"), "w") as file:
        json.dump(result, file, indent=4)
    with open(os.path.join(save_path, "api_dependency.json"), "w") as file:
        json.dump(api_sequence_list, file, indent=4)

if __name__ == '__main__':
    data_analysis("foREST", "E:\\code\\restful_test\\experiment\\foREST\\project_1\\logs\\2xx_request", "E:\\code\\restful_test\\foREST\\log", 20)