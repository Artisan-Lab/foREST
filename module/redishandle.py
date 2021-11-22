import json
import redis
from module.jsonhandle import JsonHandle
from tool.tools import Tool
import random
redis_response_pool = redis.StrictRedis(host=Tool.readconfig('redis', 'redis_host'), port=Tool.readconfig('redis', 'redis_port'))


class RedisHandle:

    @staticmethod
    def get_api_response(api_id):
        return redis_response_pool.get(api_id)

    @staticmethod
    def set_api_response(api_id, response_list):
        return redis_response_pool.set(api_id, response_list)

    @staticmethod
    def add_data_to_redis(response, api_id):
        response_dic = JsonHandle.json2dic(response.text)
        if RedisHandle.get_api_response(api_id):
            redis_response_list = JsonHandle.json2dic(RedisHandle.get_api_response(api_id))
            if response_dic not in redis_response_list:
                parameter_list = redis_response_list + [response_dic]
            else:
                parameter_list = redis_response_list
            redis_response_list = JsonHandle.dic2json(parameter_list)
            RedisHandle.set_api_response(api_id, redis_response_list)
        else:
            parameter_list = [response_dic]
            redis_response_list = JsonHandle.dic2json(parameter_list)
            RedisHandle.set_api_response(api_id, redis_response_list)

    def get_value_from_response_pool(self, field_info):
        value = None
        depend_list = field_info.depend_list
        random.shuffle(depend_list)
        for depended_api in depend_list:
            if RedisHandle.get_api_response(depended_api):
                redis_parameter_dic = json.loads(RedisHandle.get_api_response(depended_api))
                value = RedisHandle.find_field_in_dic(redis_parameter_dic, field_info)
        return value

    @staticmethod
    def find_specific_parameter_in_dic(dic, parameter_path):
        if len(parameter_path) == 1:
            if parameter_path[0] in dic:
                return dic[parameter_path[0]]


    @staticmethod
    def find_field_in_dic(dic, field_info):
        if isinstance(dic, dict):
            for key in dic:
                if key == field_info.field_name and (type(dic[key]).__name__ == field_info.field_type):
                    value = dic[key]
                    return value
                else:
                    if isinstance(dic[key], dict) or isinstance(dic[key], list):
                        value = RedisHandle.find_field_in_dic(dic[key], field_info)
                        if value:
                            return value
        elif isinstance(dic, list):
            if (dic is not None) and (len(dic) > 0) and (isinstance(dic[0], dict) or isinstance(dic[0], list)):
                for sub_dic in dic:
                    value = RedisHandle.find_field_in_dic(sub_dic, field_info)
                    if value:
                        return value
        return None


redis_response_handle = RedisHandle()
