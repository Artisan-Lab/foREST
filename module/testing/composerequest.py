import copy, collections
from allpairspy import AllPairs
from entity.api_info import *
from foREST_setting import foRESTSettings
from module.foREST_monitor.foREST_monitor import Monitor
from module.testing.basic_fuzz import BasicFuzz
from module.utils.utils import *
from entity.resource_pool import resource_pool
from entity.request import Request


def get_all_field(parameter_list):
    ans, current_path = [], []

    def dfs(parameter):
        if parameter.require:
            return
        if parameter.field_name:
            current_path.append(parameter.field_name)
            ans.append(current_path[:])
        elif parameter.array:
            current_path.append("list")
            ans.append(current_path[:])
        else:
            current_path.append(parameter.field_type)
            ans.append(current_path[:])
        if parameter.object:
            for sub_parameter in parameter.object:
                dfs(sub_parameter)
        elif parameter.array:
            dfs(parameter.array)
        current_path.pop()

    for parameter in parameter_list:
        dfs(parameter)
        if current_path:
            print(1)
    return ans


class ComposeRequest:
    """
        这个模块是用于生成请求的
    """

    def __init__(self, api_info, node):
        self.api_info = api_info  # type: APIInfo
        self.node = node
        self.request = Request(api_info)  # type: Request
        self.optional_request_pool = []
        self.parent_source_list = []
        self.parent_resource = None
        self.request = self.request
        self.path = []
        self.current_para_list = []
        self.parameter_list = []

    def get_path_parameter(self):
        self.parent_resource = None
        self.parent_resource = resource_pool().find_parent_resource(self.api_info.path)
        if self.parent_resource:
            if self.parent_resource.api_info == self.api_info.api_id:
                self.parent_resource = None
            self.get_path_parameter_from_parent_resource(self.request)

    def get_path_parameter_from_parent_resource(self, request):
        path_parameter_list = self.parent_resource.request.path_parameter_list
        for path_parameter in path_parameter_list:
            request.add_parameter(0, path_parameter, path_parameter_list[path_parameter])

    @staticmethod
    def get_value_from_depend(field_info):
        depend_point = field_info.genetic_algorithm()
        if depend_point.api_info is None and (field_info.field_type == 'int' or field_info.field_type == 'str'):
            return BasicFuzz.fuzz_value_from_field(field_info)
        else:
            value = resource_pool().get_special_value_from_resource(depend_point.api_info.identifier, depend_point.path)
        if value:
            if depend_point.flag == "base":
                return value
            elif depend_point.flag == "mutate":
                if field_info.field_type == "string":
                    return BasicFuzz.fuzz_mutation_parameter(value)
                else:
                    return value
            else:
                raise Exception("unknown dependency type")
        depend_point.minus_score()

    def get_value(self, field_info: FieldInfo):
        value = None
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            return value
        if foRESTSettings().annotation_table:
            value = annotation_table_parse(Monitor().annotation_table,
                                           self.api_info.path,
                                           self.api_info.http_method,
                                           field_info.field_name,
                                           field_info.location
                                           )
            return value
        if field_info.depend_list:
            value = ComposeRequest.get_value_from_depend(field_info)
            if value:
                return value
        if field_info.field_type == 'dict':
            value = {}
            if not field_info.object:
                return BasicFuzz.fuzz_dict()
            for sub_field_info in field_info.object:
                sub_field_value = self.get_value(sub_field_info)
                if sub_field_value:
                    value[sub_field_info.field_name] = sub_field_value
            return value
        elif field_info.field_type == 'list':
            value = []
            if field_info.array.field_type == 'dict':
                sub_value = {}
                if field_info.array.object:
                    for array_field in field_info.array.object:
                        sub_value[array_field.field_name] = self.get_value(array_field)
                    value.append(sub_value)
                return value
            else:
                value = BasicFuzz.fuzz_list()
                return value
        if value is None:
            value = BasicFuzz.fuzz_value_from_field(field_info)
        return value

    def compose_required_request(self):
        if not self.api_info.req_param:
            self.request.compose_request()
            return
        for field_info in self.api_info.req_param:
            if field_info.require and field_info.field_name not in self.request.path_parameter_list:
                value = self.get_value(field_info)
                self.request.add_parameter(field_info.location, field_info.field_name, value)
        self.request.compose_request()
        return

    def get_option_value(self, field_info: FieldInfo):
        if field_info.field_name:
            self.path.append(field_info.field_name)
        elif field_info.array:
            self.path.append("list")
        elif field_info.field_type == "dict":
            self.path.append("dict")
        if self.path not in self.current_para_list:
            self.path.pop()
            return
        value = None
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            self.path.pop()
            return value
        if foRESTSettings().annotation_table:
            value = annotation_table_parse(Monitor().annotation_table,
                                           self.api_info.path,
                                           self.api_info.http_method,
                                           field_info.field_name,
                                           field_info.location
                                           )
            self.path.pop()
            return value
        if field_info.depend_list:
            value = ComposeRequest.get_value_from_depend(field_info)
            if value:
                self.path.pop()
                return value
        if field_info.field_type == 'dict':
            value = {}
            if not field_info.object:
                self.path.pop()
                return BasicFuzz.fuzz_dict()
            for sub_field_info in field_info.object:
                sub_field_value = self.get_value(sub_field_info)
                if sub_field_value:
                    value[sub_field_info.field_name] = sub_field_value
            self.path.pop()
            return value
        elif field_info.field_type == 'list':
            value = []
            if field_info.array.field_type == 'dict':
                sub_value = {}
                if field_info.array.object:
                    for array_field in field_info.array.object:
                        sub_value[array_field.field_name] = self.get_value(array_field)
                    value.append(sub_value)
                self.path.pop()
                return value
            else:
                value = BasicFuzz.fuzz_list()
                self.path.pop()
                return value
        if value is None:
            value = BasicFuzz.fuzz_value_from_field(field_info)
        self.path.pop()
        return value

    def compose_optional_request(self):
        if not self.api_info.req_param:
            return
        parameter_list = get_all_field(self.api_info.req_param)
        if len(parameter_list) == 0:
            optional_parameter_pairs = []
        elif len(parameter_list) == 1:
            optional_parameter_pairs = [[1]]
        else:
            random.shuffle(parameter_list)
            optional_parameter_pairs = AllPairs([[1, 0] for i in range(len(parameter_list))])
        for choice_number in optional_parameter_pairs:
            choice_parameters = []
            for i, id in enumerate(choice_number):
                if id == 1:
                    choice_parameters.append(parameter_list[i])
            choice_parameters.sort(key=lambda x: len(x))
            self.parameter_list.append(choice_parameters)

        for self.current_para_list in self.parameter_list:
            self.request = Request(self.api_info)
            self.compose_required_request()
            for field_info in self.api_info.req_param:
                value = self.get_option_value(field_info)
                if value is not None:
                    self.request.add_parameter(field_info.location, field_info.field_name, value)
            self.request.compose_request()
            self.optional_request_pool.append(copy.deepcopy(self.request))

    @property
    def optional_request(self):
        return self.optional_request_pool

    def get_required_request(self):
        self.compose_required_request()
        return self.request

    def find_field_from_name(self, field_name):
        for field_info in self.api_info.req_param:
            if field_info.field_name == field_name:
                return field_info
