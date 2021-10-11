import json
import redis
from module.jsonhandle import JsonHandle
from tool.tools import Tool
from log.get_logging import DebugLog
import random
redis_response_pool = redis.StrictRedis(host=Tool.readconfig('redis', 'redis_host'), port=Tool.readconfig('redis', 'redisport'))


class ResponseRedis:


    def __init__(self, response_pool):
        self.response_pool = response_pool

    def get_api_response(self, api_id):
        return self.response_pool.get(api_id)

    def set_api_response(self, api_id, response_list):
        return self.response_pool.set(api_id, response_list)

    def add_data_to_redis(self, response, api_id, only_save_one_data=True):
        response_dic = JsonHandle.json2dic(response.text)
        if only_save_one_data:
            response_dic["data"] = [random.choice(response_dic.get("data"))]
        if self.response_pool.get_api_response(api_id):
            redis_response_list = JsonHandle.json2dic(self.response_pool.get_api_response(api_id))
            parameter_list = redis_response_list + [response_dic]
            redis_response_list = JsonHandle.dic2json(parameter_list)
            self.response_pool.set_api_response(api_id, redis_response_list)
        else:
            parameter_list = [response_dic]
            redis_response_list = JsonHandle.dic2json(parameter_list)
            self.response_pool.set_api_response(api_id, redis_response_list)

    def get_value_from_response_pool(self, depend_list):
        value = None
        random.shuffle(depend_list)
        for depended_api in depend_list:
            if self.response_pool.get(depended_api):
                redis_parameter_dic = json.loads(self.response_pool.get(depended_api))

        return value

