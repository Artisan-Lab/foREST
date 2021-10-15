import redis
from tool.tools import Tool
from entity import Request

redis_host = Tool.readconfig('redis', 'redis_host')
redis_port = Tool.readconfig('redis', 'redis_port')
response_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=0)
result_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=1)

class Test:
    def __init__(self, semantic_tree_root, api_list, set_traverse_nums=1):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
        api_number = len(api_list)
        self.result_dic = {'visited': 0, 'success': 0, 'valid': 0, '2xx': 0, '4xx': 0, '5xx': 0, 'timeout': 0}
        self.visited_pool = [0 for i in range(api_number)]
        self.status_2xx_pool = [0 for i in range(api_number)]
        self.status_4xx_pool = [0 for i in range(api_number)]
        self.status_5xx_pool = [0 for i in range(api_number)]
        self.timeout_pool = [0 for i in range(api_number)]
        self.set_traverse_nums = set_traverse_nums
        self.traverse_nums = 0
        self.node_queue = [semantic_tree_root]

    def api_testing(self, node, method):
        api_info = self.api_list[node.method_dic[method]]
        request = Request(api_info.base_url,api_info.http_method)

    @staticmethod
    def get_required_value(field_info):

        value = None
        if field_info.depend_list




    def node_testing(self, node):
        close_api_list = []
        if node.parent:
            close_api_list.append(node.parent.method_dic)
        close_api_list.append(node.method_dic)
        exec_method_list = ['post', 'get', 'put', 'delete', 'delete', 'put', 'get', 'post']
        for exec_method in exec_method_list:
            if exec_method:
                self.api_testing(node, exec_method)



    def BFS(self):
        while self.node_queue:
            node = self.node_queue.pop(0)
            self.node_testing(node)
            if node.children:
                for child in node.children:
                    self.node_queue.append(child)
        self.traverse_nums += 1

    def generate_require_case(self):






