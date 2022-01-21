import copy
import json
import random

from log.get_logging import external_log
from module.basic_fuzz import BasicFuzz
from module.genetic_algorithm import GeneticAlgorithm
from module.string_march import StringMatch
from entity.request import Request


class ComposeRequest:
    """
        这个模块是用于生成请求的
    """

    def __init__(self, api_info, request_list):
        self.api_info = api_info
        self.request_list = request_list
        self.request = Request(api_info.base_url + api_info.path, api_info.http_method, api_info.api_id)
        self.optional_request_pool = []
        self.parent_source_list = []
        for request in request_list:
            self.parent_source_list.append(request.api_id)
        self.current_parent_source = None
        self.current_request = self.request

    def get_value(self, field_info):
        # 获取参数值
        if field_info.field_type == 'bool':
            return random.choice([True, False])
        # if self.current_parent_source:
        #     value = self.current_parent_source.find_field_from_name(field_info.field_name, field_info.field_type)
        #     if value:
        #         return
        if field_info.depend_list[0]:
            # 判断该参数可否从其他请求的响应中获取
            for i in range(0, len(field_info.depend_list[0])):
                value = None
                field_path = field_info.depend_list[0][i]
                if field_path[0] in self.parent_source_list:
                    value = self.find_value(field_path)
                if value:
                    return value

    def find_value(self, path):
        for request in self.request_list:
            if request.api_id == path[0]:
                response_dict = json.loads(request.response.text.split('Connection to server successfully...')[0])
                value = ComposeRequest.get_value_from_dict(response_dict, path[1:])
                return value

    @staticmethod
    def get_value_from_dict(response_dict, path):
        if len(path) == 1:
            return response_dict[path[0]]
        if path[0] in response_dict:
            ComposeRequest.get_value_from_dict(response_dict[path[0]], path[1:])


    def compose_required_request(self):
        # 组装必选参数
        if not self.api_info.req_param:
            self.request.compose_request()
        for field_info in self.api_info.req_param:
            if field_info.require:
                value = self.get_value(field_info)
                self.request.add_parameter(field_info.location, field_info.field_name, value)
        self.request.compose_request()
        return self.request


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