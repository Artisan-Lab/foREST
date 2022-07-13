from module.data_analysis.logpool import *


class FindParameterDependency:

    def __init__(self, max_sequence_length):
        self.current_parameter_path = []
        self.parameter_log_index = None
        self.value = ""
        self.data_dict = {}
        self._result = {}
        self._max_sequence_length = max_sequence_length
        for user in log_pool.user_dict:
            self.log_list = log_pool.user_dict[user]
            for log in self.log_list:  # type: LogEntity
                self.current_parameter_path.append(log.identifier)
                if not isinstance(log.body, str):
                    self.find_value(log.body, False)
                if log.path_parameter:
                    self.find_value(log.path_parameter, False)
                if log.query_parameter:
                    self.find_value(log.query_parameter, False)
                if log.response_data and not isinstance(log.response_data, str):
                    self.find_value(log.response_data, True)
                self.current_parameter_path.pop()

    @property
    def result(self):
        return self._result

    def find_value(self, parameter_list, save):
        if isinstance(parameter_list, dict):
            for key in parameter_list:
                self.current_parameter_path.append(key)
                self.find_value(parameter_list[key], save)
                self.current_parameter_path.pop()
        elif isinstance(parameter_list, list):
            for item in parameter_list:
                self.current_parameter_path.append('list')
                self.find_value(item, save)
                self.current_parameter_path.pop()
        elif parameter_list and not isinstance(parameter_list, bool):
            if save:
                identifier = self.current_parameter_path[0].lower() + "  " + "/".join(self.current_parameter_path[1:])
                if str(parameter_list) in self.data_dict:
                    if identifier not in self.data_dict[str(parameter_list)]:
                        self.data_dict[str(parameter_list)].append(identifier)
                else:
                    self.data_dict[str(parameter_list)] = [identifier]
            else:
                if str(parameter_list) in self.data_dict:
                    current_api_identifier = self.current_parameter_path[0].lower()
                    current_parameter_identifier = "/".join(self.current_parameter_path[1:])
                    if current_api_identifier not in self.result:
                        self.result[current_api_identifier] = {}
                    if current_parameter_identifier not in self.result[current_api_identifier]:
                        self.result[current_api_identifier][current_parameter_identifier] = {}
                    tmp = self.result[current_api_identifier][current_parameter_identifier]
                    for depend_parameter_identifier in self.data_dict[str(parameter_list)]:
                        new = "  ".join(depend_parameter_identifier.split()[:2])
                        if new == current_api_identifier:
                            continue
                        if depend_parameter_identifier in tmp:
                            tmp[depend_parameter_identifier] += 1
                        else:
                            tmp[depend_parameter_identifier] = 1
