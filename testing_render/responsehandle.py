import json
import re
from module.redishandle import RedisHandle
from log.get_logging import Log
from module.jsonhandle import JsonHandle
from module.redishandle import redis_response_handle
from log.get_logging import summery_count
from log.get_logging import summery_log


class ResponseJudge:

    def __init__(self, request_message, response, api_info, success_pool, valid_pool):
        self.request_message = request_message
        if JsonHandle.is_json(response.text):
            self.response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.text} \n\n'
        else:
            self.response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.raw.data} \n\n'
        self.response = response
        self.success_pool = success_pool
        self.valid_pool = valid_pool
        self.api_info = api_info
        self.response_status = 0

    def response_judge(self):
        requests_log = Log(log_name='total_request')
        status_2xx_log = Log(log_name='2xx_request')
        status_4xx_log = Log(log_name='4xx_request')
        status_5xx_log = Log(log_name='5xx_request')
        requests_log.debug(self.request_message + self.response_message)
        if re.match('2..', str(self.response.status_code)):
            self.response_status = 2
            summery_count['2xx requests number'] += 1
            status_2xx_log.info(self.request_message + self.response_message)
            self.success_pool[self.api_info.api_id] = 1
            redis_response_handle.add_data_to_redis(self.response, self.api_info)
        elif re.match('4..', str(self.response.status_code)):
            summery_count['4xx requests number'] += 1
            self.response_status = 4
            status_4xx_log.info(self.request_message + self.response_message)
        elif re.match('5..', str(self.response.status_code)):
            summery_count['5xx requests number'] += 1
            self.response_status = 5
            status_5xx_log.info(self.request_message + self.response_message)
        summery_log.debug(str(summery_count))
        return self.success_pool, self.response_status

