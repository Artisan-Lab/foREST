from module.basic_fuzz_value import BasicFuzzValue
import redis
import csv
from log.get_logging import Log




class ComposeRequest:
    """

    """

    def __init__(self, api_info, redis_parameter_pool, close_api_list):
        self.api_info = api_info
        self.base_url = api_info.path
        self.method = api_info.http_method
        self.required_url = api_info.path
        self.redis_parameter_pool = redis_parameter_pool
        self.close_api_list = close_api_list
        self.required_data = {}
        self.required_header = {'Content-Type': "application/json"}


    @staticmethod
    def set_external_fields_from_file(path):