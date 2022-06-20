from entity.logpool import log_pool
from parsers.parser import api_list


class FindDependency:

    def __init__(self):
        self.current_parameter_path = []
        self.current_response_path = []
        self.parameter_log_index = None
        self.value = ""
        self.parameter_api_info = None
        self.response_api_info = None
        for user in log_pool.user_dict:
            self.log_list = log_pool.user_dict[user]
            for i in range(len(self.log_list)):
                self.parameter_log_index = i
                log = self.log_list[i]
                self.parameter_api_info = api_list[log.api_id]
                if not isinstance(log.body, str):
                    self.get_dependency(log.body)
                if log.path_parameter:
                    self.get_dependency(log.path_parameter)
                if log.query_parameter:
                    self.get_dependency(log.query_parameter)
                print(f"finish {i/len(self.log_list)}", end='\r')

    def get_dependency(self, parameter_list):
        if isinstance(parameter_list, dict):
            for key in parameter_list:
                self.current_parameter_path.append(key)
                self.get_dependency(parameter_list[key])
                self.current_parameter_path.pop()
        elif isinstance(parameter_list, list):
            for item in parameter_list:
                self.current_parameter_path.append(None)
                self.get_dependency(item)
                self.current_parameter_path.pop()
        else:
            if parameter_list == 'True' or parameter_list == 'False':
                return
            self.value = parameter_list
            if self.parameter_log_index < 100:
                for i in range(0, self.parameter_log_index):
                    response_log = self.log_list[i]
                    self.current_response_path.append(str(response_log.api_id))
                    self.get_log2_key(response_log.response_data)
                    self.current_response_path.pop()
            else:
                for i in range(self.parameter_log_index-100, self.parameter_log_index):
                    response_log = self.log_list[i]
                    self.current_response_path.append(str(response_log.api_id))
                    self.get_log2_key(response_log.response_data)
                    self.current_response_path.pop()

    def get_log2_key(self, response_list):
        if isinstance(response_list, dict):
            for key in response_list:
                self.current_response_path.append(key)
                self.get_log2_key(response_list[key])
                self.current_response_path.pop()
        if isinstance(response_list, list):
            for item in response_list:
                self.get_log2_key(item)
        else:
            if self.value == response_list:
                self.add_to_dict(self.parameter_api_info.req_param)

    def add_to_dict(self, field_info_list):
        if isinstance(field_info_list, list):
            for field_info in field_info_list:
                self.add_to_dict(field_info)
        else:
            if field_info_list.field_name == self.current_parameter_path[0]:
                tmp_path = self.current_parameter_path.pop(0)
                if self.current_parameter_path:
                    if field_info_list.object:
                        self.add_to_dict(field_info_list.object)
                    elif field_info_list.array:
                        self.add_to_dict(field_info_list.array)
                else:
                    if '-'.join(self.current_response_path) in field_info_list.depend_list:
                        field_info_list.depend_list['-'.join(self.current_response_path)] += 1
                    else:
                        field_info_list.depend_list['-'.join(self.current_response_path)] = 1
                self.current_parameter_path.insert(0, tmp_path)


log_dependency_analysis = FindDependency()