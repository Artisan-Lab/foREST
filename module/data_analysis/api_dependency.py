from module.data_analysis.logpool import *
from module.foREST_monitor.sequence_monitor import *
import itertools


def api_dependency(max_sequence_length: int):
    global result
    for user in log_pool.user_dict:
        log_list = log_pool.user_dict[user]
        for i in range(len(log_list)):
            tmp_log_list = []
            tmp_identifier_list = []
            for j in range(max_sequence_length):
                if i+j >= len(log_list) or log_list[i+j].identifier in tmp_identifier_list:
                    break
                tmp_log_list.append(log_list[i+j])
                tmp_identifier_list.append(log_list[i+j].identifier)
                if len(tmp_log_list) <= 1:
                    continue
                param_depend_info = parameter_dependency_analysis(tmp_log_list)
                sequence_list = sequence_generate(tmp_log_list, param_depend_info)
                Sequence_Monitor().append_sequences(sequence_list)


def parameter_dependency_analysis(log_list: [LogEntity]):
    current_parameter_path = []
    data_dict = {}
    param_depend = {}

    def find_dependency(parameter_list, save):
        if isinstance(parameter_list, dict):
            for key in parameter_list:
                current_parameter_path.append(key)
                find_dependency(parameter_list[key], save)
                current_parameter_path.pop()
        elif isinstance(parameter_list, list):
            for item in parameter_list:
                current_parameter_path.append('list')
                find_dependency(item, save)
                current_parameter_path.pop()
        elif parameter_list and not isinstance(parameter_list, bool):
            if save:
                identifier = current_parameter_path[0].lower() + "  " + "/".join(current_parameter_path[1:])
                if str(parameter_list) in data_dict:
                    if identifier not in data_dict[str(parameter_list)]:
                        data_dict[str(parameter_list)].append(identifier)
                else:
                    data_dict[str(parameter_list)] = [identifier]
            else:
                if str(parameter_list) in data_dict:
                    current_api_identifier = current_parameter_path[0].lower()
                    current_parameter_identifier = "/".join(current_parameter_path[1:])
                    for depend_parameter_identifier in data_dict[str(parameter_list)]:
                        new = "  ".join(depend_parameter_identifier.split()[:2])
                        if new == current_api_identifier:
                            continue
                        identifier = "  ".join([current_api_identifier, current_parameter_identifier])
                        if identifier not in param_depend:
                            param_depend[identifier] = []
                        if depend_parameter_identifier not in param_depend[identifier]:
                            param_depend[identifier].append(depend_parameter_identifier)

    for log in log_list:  # type: LogEntity
        current_parameter_path.append(log.identifier)
        if not isinstance(log.body, str):
            find_dependency(log.body, False)
        if log.path_parameter:
            find_dependency(log.path_parameter, False)
        if log.query_parameter:
            find_dependency(log.query_parameter, False)
        if log.response_data and not isinstance(log.response_data, str):
            find_dependency(log.response_data, True)
        current_parameter_path.pop()
    return param_depend


def sequence_generate(log_list, parm_depend_info):
    sequence_list = []
    if parm_depend_info:
        sequence = Sequence()
        for log in log_list:
            api_depend_info = APIDependency(log.identifier)
            for key in parm_depend_info.keys():
                if log.identifier == "  ".join(key.split()[:2]):
                    for parm_depend in parm_depend_info[key]:
                        api_depend_info.append(key.split()[-1], parm_depend)
            sequence.append(api_depend_info)
        sequence_list.append(sequence)
    sequence = Sequence()
    for log in log_list:
        sequence.append(APIDependency(log.identifier))
    sequence_list.append(sequence)
    return sequence_list



