from module.basic_fuzz import BasicFuzz
from module.redishandle import redis_response_handle
from tool.tools import redis_external_key
from log.get_logging import Log
from entity.request import Request


class ComposeRequest:
    """

    """

    def __init__(self, api_info, close_api_list):
        self.api_info = api_info
        self.request = Request(api_info.base_url+api_info.path, api_info.http_method)
        self.close_api_list = close_api_list

    @staticmethod
    def get_required_value(field_info):
        value = None
        if redis_external_key.exists(field_info.field_name):
            value = redis_external_key.get(field_info.field_name)
            log = Log(log_name='hit_external_field')
            log.info('Key: ' + str(field_info.field_name) + 'Value: ' + str(value))
            return value
        if field_info.depend_list:
            value = redis_response_handle.get_value_from_response_pool(field_info)
            if value:
                return value
        if field_info.field_type == 'object':
            value = {}
            if field_info.object:
                for sub_field_info in field_info.object:
                    if sub_field_info.require:
                        sub_field_value = ComposeRequest.get_required_value(sub_field_info)
                        if sub_field_value:
                            value[sub_field_info.field_name] = sub_field_value
                return value
        elif field_info.field_type == 'array':
            if isinstance(field_info.array, list):
                value = []
                sub_value = {}
                for array_field in field_info.array:
                    if array_field.require:
                        sub_value[array_field.field_name] = ComposeRequest.get_required_value(array_field)
                value.append(sub_value)
                return value
            elif isinstance(field_info.array, str):
                value = []
                for i in range(0, 5):
                    value.append(BasicFuzz.fuzz_value_from_type(field_info.array))
                return value
        if value is None:
            value = BasicFuzz.fuzz_value(field_info)
        return value

    def compose_request(self):
        if not self.api_info.req_param:
            return
        for field_info in self.api_info.req_param:
            if field_info.require:
                value = self.get_required_value(field_info)
                self.request.add_parameter(field_info.location, field_info.field_name, value)
        self.request.compose_request()
        return

    @property
    def get_request(self):
        return self.request

