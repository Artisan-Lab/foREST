from entity.logpool import *
from module.data_analysis.RB_tree import *


class DependPoint:
    def __init__(self, api_id: int, path: list, score):
        self._api_id = api_id
        self._path = path
        self._score = score
        self._mutate_score = score
        self._time = 0

    @property
    def api_id(self):
        return self._api_id

    @property
    def path(self):
        return self._path

    @property
    def score(self):
        return self._score

    @property
    def mutate_score(self):
        return self._mutate_score

    @property
    def time(self):
        return self._time

    def add_score(self):
        self._score += pow((1 - self.score), 2)

    def minus_score(self):
        self._score -= pow(self.score, 2)

    def add_time(self):
        self._time += 1

class FindDependency:

    def __init__(self, save_type):
        self.current_parameter_path = []
        self.parameter_log_index = None
        self.value = ""
        self.data_RBtree = Rbtree()
        self.data_dict = {}
        self._result = {}
        self.save_type = save_type
        for user in log_pool.user_dict:
            self.log_list = log_pool.user_dict[user]
            for log in self.log_list:  # type: LogEntity
                if log.log_id % 1000 == 0:
                    print(log.log_id)
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
            if self.save_type == 'dict':
                if save:
                    identifier = self.current_parameter_path[0] + "  " + "/".join(self.current_parameter_path[1:])
                    if str(parameter_list) in self.data_dict:
                        if identifier not in self.data_dict[str(parameter_list)]:
                            self.data_dict[str(parameter_list)].append(identifier)
                    else:
                        self.data_dict[str(parameter_list)] = [identifier]
                else:
                    if str(parameter_list) in self.data_dict:
                        current_api_identifier = self.current_parameter_path[0]
                        current_parameter_identifier = "-".join(self.current_parameter_path[1:])
                        if current_api_identifier not in self.result:
                            self.result[current_api_identifier] = {}
                        if current_parameter_identifier not in self.result[current_api_identifier]:
                            self.result[current_api_identifier][current_parameter_identifier] = {}
                        tmp = self.result[current_api_identifier][current_parameter_identifier]
                        for depend_parameter_identifier in self.data_dict[str(parameter_list)]:
                            if depend_parameter_identifier in tmp:
                                tmp[depend_parameter_identifier] += 1
                            else:
                                tmp[depend_parameter_identifier] = 1
            elif self.save_type == 'rbtree':
                find_point = self.data_RBtree.find(str(parameter_list))
                if save:
                    identifier = self.current_parameter_path[0] + "  " + "/".join(self.current_parameter_path[1:])
                    if find_point:
                        if identifier not in find_point.info:
                            find_point.info.append(identifier)
                    else:
                        p = RbPoint(str(parameter_list), identifier)
                        self.data_RBtree.insert(p)
                else:
                    if find_point:
                        current_api_identifier = self.current_parameter_path[0]
                        current_parameter_identifier = "-".join(self.current_parameter_path[1:])
                        if current_api_identifier not in self.result:
                            self.result[current_api_identifier] = {}
                        if current_parameter_identifier not in self.result[current_api_identifier]:
                            self.result[current_api_identifier][current_parameter_identifier] = {}
                        tmp = self.result[current_api_identifier][current_parameter_identifier]
                        for depend_parameter_identifier in find_point.info:
                            if depend_parameter_identifier in tmp:
                                tmp[depend_parameter_identifier] += 1
                            else:
                                tmp[depend_parameter_identifier] = 1



    # def add_to_depend(self, field_info: FieldInfo, parameter_path: list, find_point):
    #     if not parameter_path:
    #         return
    #     if field_info.field_type == "dict" and field_info.field_name == parameter_path[0]:
    #         for sub_field_info in field_info.object:
    #             self.add_to_depend(sub_field_info, parameter_path[1:], find_point)
    #     elif field_info.field_type == "list" and not parameter_path[0]:
    #         for sub_field_info in field_info.array:
    #             self.add_to_depend(sub_field_info, parameter_path[1:], find_point)
    #     else:
    #         if len(parameter_path) == 1 and field_info.field_name == parameter_path[0]:
    #             api_id_1, api_path_1, api_id_2, api_path_2, time = []
    #             for api_id, path in find_point:
    #                 depend_node = field_info.get_depend(api_id, path)
    #                 if depend_node:
    #                     depend_node.add_time()
    #                 else:


