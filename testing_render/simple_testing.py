from testing_render.composerequest import ComposeRequest
from log.get_logging import summery_log, requests_log, status_2xx_log, \
                            status_4xx_log, status_5xx_log, status_timeout_log
from log.get_logging import summery_count
import re
from module.redishandle import redis_response_handle
from module.jsonhandle import JsonHandle

class Test:
    def __init__(self, semantic_tree_root, api_list, set_traverse_nums=1):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
        self.api_info = None
        self.api_number = len(api_list)
        self.success_pool = [0 for i in range(0, self.api_number)]
        self.visited_pool = [0 for i in range(0, self.api_number)]
        self.vaild_pool = [0 for i in range(0, self.api_number)]
        self.status_2xx_pool = [0 for i in range(0, self.api_number)]
        self.status_4xx_pool = [0 for i in range(0, self.api_number)]
        self.status_5xx_pool = [0 for i in range(0, self.api_number)]
        self.timeout_pool = [0 for i in range(0, self.api_number)]
        self.set_traverse_nums = set_traverse_nums
        self.traverse_nums = 0
        self.node_queue = []
        self.request_message = None
        summery_count['api number'] = self.api_number
        summery_count['test rounds nember'] = set_traverse_nums


