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
    def add_data_to_redis(response, api_info):
        if JsonHandle.json_judge(response.text):
            response_dic = JsonHandle.json2dic(response.text)
        else:
            response_dic = response.text
        if RedisHandle.get_api_response(api_info.api_id):
            redis_response_list = JsonHandle.json2dic(RedisHandle.get_api_response(api_info.api_id))
        else:
            redis_response_list = []
        if isinstance(response_dic, list):
            redis_response_list += response_dic
        else:
            redis_response_list.append(response_dic)
        redis_response_list = Tool.list_de_duplicate(redis_response_list)
        redis_response_list = JsonHandle.dic2json(redis_response_list)
        RedisHandle.set_api_response(api_info.api_id, redis_response_list)

    @staticmethod
    def get_value_from_response_pool(field_info):
        value = None
        depend_list = field_info.depend_list
        random.shuffle(depend_list)
        for depended_api in depend_list:
            if RedisHandle.get_api_response(depended_api):
                redis_parameter_dic = json.loads(RedisHandle.get_api_response(depended_api))
                value = RedisHandle.find_field_in_dic(redis_parameter_dic, field_info)
        return value

    @staticmethod
    def get_specific_value_from_response_pool(field_path):
        value = None
        api_id = field_path[0]
        if RedisHandle.get_api_response(api_id):
            redis_parameter_dic = json.loads(RedisHandle.get_api_response(api_id))
            random.shuffle(redis_parameter_dic)
            if field_path[1] is None:
                field_path.pop(1)
            for single_response in redis_parameter_dic:
                if single_response:
                    value = RedisHandle.find_specific_parameter_in_dic(single_response, field_path[1:])
                if value:
                    return value
        return value

    @staticmethod
    def find_specific_parameter_in_dic(dic, parameter_path):
        if len(parameter_path) == 1:
            if parameter_path[0] in dic:
                return dic[parameter_path[0]]
        if isinstance(dic, dict) and parameter_path[0] in dic:
            return RedisHandle.find_specific_parameter_in_dic(dic[parameter_path[0]], parameter_path[1:])
        if isinstance(dic, list) and parameter_path[0] is None:
            value = None
            for sub_dict in dic:
                value = RedisHandle.find_specific_parameter_in_dic(sub_dict, parameter_path[1:])
                if value:
                    return value
        return None

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
