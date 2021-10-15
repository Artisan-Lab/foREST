from module.basic_fuzz_value import BasicFuzzValue
import redis
import csv
from tool.tools import Tool
from log.get_logging import Log

redis_external_key = redis.StrictRedis(host=Tool.readconfig('redis', 'redis_host'), port=Tool.readconfig('redis', 'redis_port'))


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
        reader = csv.reader(open(path))
        for line in reader:
            key, value = line[0], line[1]
            redis_external_key.set(key, value)

    @staticmethod
    def find_field_in_dic(dic, field_info, simple_compare):
        if isinstance(dic, dict):
            for key in dic:
                if key == field_info.field_type and (isinstance(dic[key], int) and field_info.field_type == 'integer' or
                                                     isinstance(dic[key], str) and field_info.field_type == 'string' or
                                                     isinstance(dic[key], list) and field_info.field_type == 'array' or
                                                     isinstance(dic[key], dict) and field_info.field_type == 'object' or
                                                     isinstance(dic[key], bool) and field_info.field_type == 'boolean'):
                    value = dic[key]
                    return value
                else:
                    value = ComposeRequest.find_field_in_dic(dic[key], field_info)
                    if value:
                        return value
        elif isinstance(dic, list)                :
            if (dic is not None) and (len(dic) > 0 ) and isinstance(dic[0], dict):
                for sub_dic in dic:
                    value = ComposeRequest.find_field_in_dic(sub_dic, field_info)
                    if value:
                        return value
        return None

    @staticmethod
    def get_required_value(field_info, redis_parameter_pool):
        value = None
        if redis_external_key.exists(field_info.field_name):
            value = redis_external_key.get(field_info.field_name)
            log = Log(log_name='hit_external_field')
            log.info('Key: ' + str(field_info.field_name) + 'Value: ' + str(value))
            return value
        if field_info.depend_list:
            value = redis_parameter_pool.get_value_from_response_pool(field_info)
            if value:
                return value
        if field_info.field_type == 'object':
            value = {}
            if field_info.object:
                for sub_field_info in field_info.object:
                    if sub_field_info.require:
                        sub_field_value = ComposeRequest.get_required_value(sub_field_info, redis_parameter_pool)
                        if sub_field_value:
                            value[sub_field_info.field_name] = sub_field_value
                return value
        elif field_info.field_type == 'array':
            if isinstance(field_info.array, list):
                value = []
                sub_value = {}
                for array_field in field_info.array:
                    if array_field.require:
                        sub_value[array_field.field_name] = ComposeRequest.get_required_value(array_field, redis_parameter_pool)
                value.append(sub_value)
                return value
            elif isinstance(field_info.array, str):
                value = []
                for i in range(0, 5):
                    value.append(BasicFuzzValue.)





