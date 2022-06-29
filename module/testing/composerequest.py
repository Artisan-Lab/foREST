import copy
from entity.api_info import *
from foREST_setting import foRESTSettings
from module.foREST_monitor.foREST_monitor import Monitor
from module.testing.basic_fuzz import BasicFuzz
from module.utils.utils import *
from entity.resource_pool import resource_pool
from entity.request import Request


class ComposeRequest:
    """
        这个模块是用于生成请求的
    """

    def __init__(self, api_info, node):
        self.api_info = api_info  # type: APIInfo
        self.node = node
        self.request = Request(api_info.base_url + api_info.path, api_info.http_method)  # type: Request
        self.optional_request_pool = []
        self.parent_source_list = []
        self.current_parent_source = None
        self.current_request = self.request

    def get_path_parameter(self):
        self.current_parent_source = None
        base_url_list = self.api_info.path.split('/')
        base_url_list.remove('')
        for path in base_url_list[::-1]:
            if not is_path_variable(path):
                self.current_parent_source = resource_pool().find_resource_from_resource_name(
                    path)
                if self.current_parent_source:
                    if self.current_parent_source.resource_api_id == self.api_info.api_id:
                        self.current_parent_source = None
                        continue
                    self.get_path_parameter_from_parent_resource(self.request)
                    break

    def get_path_parameter_from_parent_resource(self, request):
        path_parameter_list = self.current_parent_source.get_resource_request.path_parameter_list
        for path_parameter in path_parameter_list:
            request.add_parameter(0, path_parameter, path_parameter_list[path_parameter])

    def get_value(self, field_info: FieldInfo):
        value = None
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            return value
        if foRESTSettings().annotation_table:
            value = get_value_from_external(Monitor().annotation_table,
                                            self.api_info.path,
                                            self.api_info.http_method,
                                            field_info.field_name,
                                            field_info.location
                                            )
            return value
        if field_info.depend_list:
            depend_point = field_info.genetic_algorithm()
            if depend_point.api_id == -1 and (field_info.field_type == 'int' or field_info.field_type == 'str'):
                return BasicFuzz.fuzz_value_from_field(field_info)
            else:
                value = resource_pool().get_special_value_from_resource(depend_point.api_id, depend_point.path)
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
        if field_info.field_type == 'dict' and field_info.object:
            value = {}
            for sub_field_info in field_info.object:
                if sub_field_info.require:
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
                        if array_field.require:
                            sub_value[array_field.field_name] = self.get_value(array_field)
                    value.append(sub_value)
                return value
            else:
                for i in range(0, 5):
                    value.append(BasicFuzz.fuzz_value_from_field(field_info.array))
                return value
        if value is None:
            value = BasicFuzz.fuzz_value_from_field(field_info)
        return value

    def compose_required_request(self):
        if not self.api_info.req_param:
            return
        for field_info in self.api_info.req_param:
            if field_info.require and field_info.field_name not in self.current_request.path_parameter_list:
                value = self.get_value(field_info)
                self.request.add_parameter(field_info.location, field_info.field_name, value)
        self.request.compose_request()
        return

    def recompose_optional_request(self):
        request = copy.deepcopy(self.request)
        request.initialization()
        if self.current_parent_source:
            self.get_path_parameter_from_parent_resource(request)
        for field_info in self.api_info.req_param:
            if not field_info.require:
                self.current_request = copy.deepcopy(request)
                for req_field_info in self.api_info.req_param:
                    if req_field_info.require and req_field_info.field_name not in self.request.path_parameter_list:
                        value = self.get_value(req_field_info)
                        self.current_request.add_parameter(req_field_info.location, req_field_info.field_name, value)
                value = self.get_value(field_info)
                self.current_request.add_parameter(field_info.location, field_info.field_name, value)
                self.current_request.compose_request()
                self.optional_request_pool.append(self.current_request)

    def compose_optional_request(self):
        if not self.api_info.req_param:
            return
        for field_info in self.api_info.req_param:
            if not field_info.require:
                request = copy.deepcopy(self.request)
                request.depend_point_list = copy.deepcopy(self.request.depend_point_list)
                self.current_request = request
                value = self.get_value(field_info)
                self.current_request.add_parameter(field_info.location, field_info.field_name, value)
                self.current_request.compose_request()
                self.optional_request_pool.append(self.current_request)

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
