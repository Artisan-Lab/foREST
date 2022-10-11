import random


class DependPoint:

    def __init__(self, api_info, path: list, score):
        self._api_info = api_info
        self._path = path
        self._base_score = score
        self._mutate_score = score
        self._time = 0
        self.flag = None

    def __repr__(self):
        return self.api_info.identifier
    @property
    def api_info(self):
        return self._api_info

    @property
    def path(self):
        return self._path

    @property
    def base_score(self):
        return self._base_score

    @base_score.setter
    def base_score(self, value):
        self._base_score = value
        self._mutate_score = value

    @property
    def mutate_score(self):
        return self._mutate_score

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = value

    def add_score(self):
        if self.flag == "base":
            self._base_score += pow((1 - self.base_score), 2)
        elif self.flag == "mutate":
            self._mutate_score += pow((1 - self.mutate_score), 2)

    def minus_score(self):
        if self.flag == "base":
            self._base_score -= pow(self.base_score, 2)
        elif self.flag == "mutate":
            self._mutate_score -= pow(self._mutate_score, 2)

    def add_time(self):
        self._time += 1


class FieldInfo:

    def __init__(self, field_name, type_, require, location, max_lenth=None, min_lenth=None, default=None,
                 description=None, enum=None, object=None, array=None, max=None, min=None, format=None, pattern=None):
        self.field_name = field_name
        self.field_type = type_  # int\str\list\object
        self.require = require
        self.default = default
        self.location = location
        self.max_lenth = max_lenth
        self.min_lenth = min_lenth
        self.enum = enum
        self.description = description
        self.object = object  # type: [FieldInfo]
        self.array = array
        self.maximum = max
        self.minimum = min
        self.pattern = pattern
        self.format = format
        self.depend_list = []  # type: list[DependPoint]
        if self.field_type == 'int' or self.field_type == 'str':
            self.depend_list.append(DependPoint(None, [], 0.5))

    def __repr__(self):
        if self.field_name:
            return self.field_name
        else:
            return self.field_type

    def get_depend(self, api_id, path):
        for depend in self.depend_list:
            if depend.api_info and depend.api_info.api_id == api_id and depend.path == path:
                return depend
        return None

    def add_log_depend(self, api_identifier, param_path, api_list, time):
        for api_info in api_list:
            if api_info.identifier == api_identifier:
                for depend_info in self.depend_list:
                    if depend_info.api_info == api_info and depend_info.path == param_path:
                        depend_info.time = time
                        break
                else:
                    depend_point = DependPoint(api_info, param_path, 0)
                    depend_point.time = time
                    self.depend_list.append(depend_point)

    def genetic_algorithm(self) -> DependPoint:
        depend_point = random.choices(self.depend_list,
                                      weights=[point.mutate_score + point.base_score for point in self.depend_list])[0]
        depend_point.flag = random.choices(["base", "mutate"],
                                           weights=[depend_point.base_score, depend_point.mutate_score])[0]
        return depend_point



def get_param(param_path: list, field_info_list):
    for field_info in field_info_list:  # type: FieldInfo
        if field_info.field_name == param_path[0] or (param_path[0] == 'list' and field_info.field_type == 'list'):
            if len(param_path) == 1:
                return field_info
            elif field_info.object:
                return get_param(param_path[1:], field_info.object)
            else:
                return None
    else:
        return None

class APIInfo:

    def __init__(self, api_id, base_url, path:str, req_param, resp_param, http_method, produces, consumes):
        self.api_id = api_id
        path = path
        self.identifier = http_method + " " + path
        self.base_url = base_url
        self.path = path
        self.close_api = []
        self.key_depend_api_list = []
        self.req_param = req_param  # type: list[FieldInfo]
        self.resp_param = resp_param  # type: list[FieldInfo]
        self.http_method = http_method
        self.produces = produces
        self.consumes = consumes

    def __repr__(self):
        return self.identifier

    def get_req_param(self, path):
        return get_param(path, self.req_param)

    def get_resp_param(self, path):
        return get_param(path, self.resp_param)

    def add_depend_api(self, api_id):
        if api_id not in self.key_depend_api_list:
            self.key_depend_api_list.append(api_id)







