import copy
from log.get_logging import external_log
from module.basic_fuzz import BasicFuzz
from module.genetic_algorithm import GeneticAlgorithm
from module.string_march import StringMatch
from entity.resource_pool import foREST_POST_resource_pool
from entity.request import Request


class ComposeRequest:
    """
        这个模块是用于生成单条请求的
    """

    def __init__(self, api_info, node):
        self.api_info = api_info
        self.node = node
        self.request = Request(api_info.base_url + api_info.path, api_info.http_method)
        self.optional_request_pool = []
        self.parent_source_list = []
        self.current_parent_source = None

    def get_path_parameter(self):
        base_url_list = self.api_info.base_url.split('/')
        for i in range(len(base_url_list), 0, -1):
            if StringMatch.is_path_variable(base_url_list[i]):
                if not StringMatch.is_path_variable(base_url_list[i - 1]):
                    self.current_parent_source = foREST_POST_resource_pool.find_resource_from_resource_name(
                        base_url_list[i - 1])
                if not self.current_parent_source and not StringMatch.is_path_variable(base_url_list[i - 2]):
                    self.current_parent_source = foREST_POST_resource_pool.find_resource_from_resource_name(
                        base_url_list[i - 2])
                path_parameter_list = self.current_parent_source.request.path_parameter_list
                for path_parameter in path_parameter_list:
                    self.request.add_parameter(0, path_parameter, path_parameter_list[path_parameter])
                field_info = self.find_field_from_name(base_url_list[i][1:-2])
                temp_name = StringMatch.get_value_from_external(self.api_info.path,
                                                                self.api_info.http_method,
                                                                field_info.field_name, 'real_field_name')
                if temp_name:
                    field_name = temp_name
                else:
                    field_name = field_info.field_name
                value = StringMatch.find_field_in_dic(self.current_parent_source.resource_data,
                                                      field_name,
                                                      field_info.field_type)
                self.request.add_parameter(0, field_info.field_name, value)

    def find_field_from_name(self, field_name):
        for field_info in self.api_info.req_param:
            if field_info.field_name == field_name:
                return field_info

    def get_value(self, field_info):
        # 获取参数值
        if field_info.field_type == 'bool':
            value = BasicFuzz.fuzz_value_from_field(field_info)
            return value
        value = StringMatch.get_value_from_external(self.api_info.path,
                                                    self.api_info.http_method,
                                                    field_info.field_name,
                                                    'value')
        # 先判断该参数有没有由外部指定
        if value:
            external_log.info('Key: ' + str(field_info.field_name) + 'Value: ' + str(value))
            return value
        if self.current_parent_source:
            value = self.current_parent_source.find_field_from_name(field_info.field_name, field_info.field_type)
            if value:
                return
        if field_info.depend_list[0]:
            # 判断该参数可否从其他请求的响应中获取
            genetic_algorithm = GeneticAlgorithm(field_info.depend_list[1])
            for i in range(len(field_info.depend_list[1])):
                winner_depend_field_index = genetic_algorithm.get_winner_index()
                value = redis_response_handle.get_specific_value_from_response_pool(
                    field_info.depend_list[0][int(winner_depend_field_index / 2)])
                if value:
                    self.request.add_genetic_algorithm(genetic_algorithm)
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
                        sub_field_value = ComposeRequest.get_value(sub_field_info)
                        if sub_field_value:
                            value[sub_field_info.field_name] = sub_field_value
                return value
        elif field_info.field_type == 'list':
            # 同上
            if isinstance(field_info.array, list):
                value = []
                sub_value = {}
                for array_field in field_info.array:
                    if array_field.require:
                        sub_value[array_field.field_name] = ComposeRequest.get_value(array_field)
                value.append(sub_value)
                return value
            elif isinstance(field_info.array, str):
                value = []
                for i in range(0, 5):
                    value.append(BasicFuzz.fuzz_value_from_type(field_info.array))
                return value
        if value is None:
            # 如果不能获得该参数的话，用fuzz
            value = BasicFuzz.fuzz_value_from_field(field_info)
        return value

    def compose_required_request(self):
        if not self.api_info.req_param:
            return
        for field_info in self.api_info.req_param:
            if field_info.require and field_info.location != 0:
                value = self.get_value(field_info)
                self.request.add_parameter(field_info.location, field_info.field_name, value)
        self.request.compose_request()
        return

    def compose_optional_request(self):
        if not self.api_info.req_param:
            return
        for field_info in self.api_info.req_param:
            if not field_info.require:
                request = copy.deepcopy(self.request)
                request.genetic_algorithm_list = Request.copy_genetic_algorithm_list(self.request)
                value = self.get_value(field_info)
                request.add_parameter(field_info.location, field_info.field_name, value)
                request.compose_request()
                self.optional_request_pool.append(request)

    def compose_request(self):
        # 该函数用于组装请求，是此类入口
        self.get_path_parameter()
        self.compose_required_request()

    def get_parameter_list(self):
        parameter_list = []
        for field_info in self.api_info.req_param:
            if not field_info.require:
                parameter_list.append(field_info)

    def get_optional_request(self):
        self.compose_optional_request()
        return self.optional_request_pool

    def get_required_request(self):
        # 返回生成的request
        self.compose_required_request()
        return self.request
