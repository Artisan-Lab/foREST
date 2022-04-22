import copy
from log.get_logging import external_log
from module.basic_fuzz import BasicFuzz
from module.genetic_algorithm import GeneticAlgorithm
from module.string_march import StringMatch
from entity.resource_pool import foREST_POST_resource_pool
from entity.request import Request


class ComposeRequest:
    """
        这个模块是用于生成请求的
    """

    def __init__(self, api_info, node):
        self.api_info = api_info
        self.node = node
        self.request = Request(api_info.base_url + api_info.path, api_info.http_method)
        self.optional_request_pool = []
        self.parent_source_list = []
        self.current_parent_source = None
        self.current_request = self.request

    def get_path_parameter(self):
        self.current_parent_source = None
        base_url_list = self.api_info.path.split('/')
        base_url_list.remove('')
        for path in base_url_list[::-1]:
            if not StringMatch.is_path_variable(path):
                # 从后往前找到路径中的定值
                self.current_parent_source = foREST_POST_resource_pool.find_resource_from_resource_name(path) # 在资源池中检索是否有该资源
                if self.current_parent_source:
                    if self.current_parent_source.resource_api_id == self.api_info.api_id:
                        # 排除掉自己做自己父资源的情况
                        self.current_parent_source = None
                        continue
                    self.get_path_parameter_from_parent_resource(self.request)
                    break

    def get_path_parameter_from_parent_resource(self, request):
        path_parameter_list = self.current_parent_source.get_resource_request.path_parameter_list
        for path_parameter in path_parameter_list:
            request.add_parameter(0, path_parameter, path_parameter_list[path_parameter])

    def get_value(self, field_info):
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            return value
        value = StringMatch.get_value_from_external(self.api_info.path,
                                                    self.api_info.http_method,
                                                    field_info.field_name,
                                                    field_info.location
                                                    )
        if value:
            external_log.info('Key: ' + str(field_info.field_name) + 'Value: ' + str(value))
            return value
        # if self.current_parent_source:
        #     value = self.current_parent_source.find_field_from_name(field_info.field_name, field_info.field_type)
        #     if value:
        #         return
        if field_info.depend_list[0]:
            # 判断该参数可否从其他请求的响应中获取
            genetic_algorithm = GeneticAlgorithm(field_info.depend_list[1])
            for i in range(len(field_info.depend_list[1])):
                winner_depend_field_index = genetic_algorithm.get_winner_index()
                field_path = field_info.depend_list[0][int(winner_depend_field_index / 2)]
                if field_path == -1 and (field_info.field_type == 'int' or field_info.field_type == 'str'):
                    return BasicFuzz.fuzz_value_from_field(field_info)
                if self.current_parent_source and field_path[0] == self.current_parent_source.resource_api_id:
                    value = self.current_parent_source.find_field_from_path(self.current_parent_source.resource_data,
                                                                            field_path[1:])
                else:
                    value = foREST_POST_resource_pool.get_special_value_from_resource(field_path[0], field_path[1:])
                if value:
                    self.current_request.add_genetic_algorithm(genetic_algorithm)
                    if winner_depend_field_index % 2 == 0 and (isinstance(value, str)):
                        return BasicFuzz.fuzz_mutation_parameter(value)
                    else:
                        return value
                genetic_algorithm.winner_failed()
            field_info.depend_list[1] = genetic_algorithm.get_survival_points_list
        if field_info.field_type == 'dict':
            # 如果没有得到并且该参数是dict类型的话，将递归生成该参数
            value = {}
            if field_info.object:
                for sub_field_info in field_info.object:
                    if sub_field_info.require:
                        sub_field_value = self.get_value(sub_field_info)
                        if sub_field_value:
                            value[sub_field_info.field_name] = sub_field_value
                return value
        elif field_info.field_type == 'list':
            # 同上
            if field_info.array.field_type == 'dict':
                value = []
                sub_value = {}
                if field_info.array.object:
                    for array_field in field_info.array.object:
                        if array_field.require:
                            sub_value[array_field.field_name] = self.get_value(array_field)
                    value.append(sub_value)
                return value
            else:
                value = []
                for i in range(0, 5):
                    value.append(BasicFuzz.fuzz_value_from_type(field_info.array.field_type))
                return value
        if value is None:
            # 如果不能获得该参数的话，用fuzz
            value = BasicFuzz.fuzz_value_from_field(field_info)
        return value

    def compose_required_request(self):
        # 组装必选参数
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
        if self.api_info.api_id == 0:
            print(1)
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
                request.genetic_algorithm_list = Request.copy_genetic_algorithm_list(self.request)
                self.current_request = request
                value = self.get_value(field_info)
                self.current_request.add_parameter(field_info.location, field_info.field_name, value)
                self.current_request.compose_request()
                self.optional_request_pool.append(self.current_request)

    @property
    def get_optional_request(self):
        return self.optional_request_pool

    def get_required_request(self):
        # 返回生成的request
        self.compose_required_request()
        return self.request

    def find_field_from_name(self, field_name):
        for field_info in self.api_info.req_param:
            if field_info.field_name == field_name:
                return field_info
