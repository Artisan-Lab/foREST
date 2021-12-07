import random
from testing_render.composerequest import ComposeRequest
from log.get_logging import summery_log, requests_log, status_2xx_log, status_4xx_log, status_5xx_log
from testing_render.responsehandle import ResponseJudge
from log.get_logging import summery_count


class CompleteTest:
    def __init__(self, semantic_tree_root, api_list, set_traverse_nums=1):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
        self.api_number = len(api_list)
        self.depend_graph = [[0 for i in range(0, self.api_number)] for j in range(0,self.api_number)]
        self.success_pool = [0 for i in range(0, self.api_number)]
        self.visited_pool = [0 for i in range(0, self.api_number)]
        self.vaild_pool = [0 for i in range(0, self.api_number)]
        self.status_2xx_pool = [0 for i in range(0, self.api_number)]
        self.status_4xx_pool = [0 for i in range(0, self.api_number)]
        self.status_5xx_pool = [0 for i in range(0, self.api_number)]
        self.timeout_pool = [0 for i in range(0, self.api_number)]
        self.success_request_pool = [[] for i in range(0, self.api_number)]
        self.set_traverse_nums = set_traverse_nums
        self.traverse_nums = 0
        self.node_queue = []
        summery_count['api number'] = self.api_number
        summery_count['test rounds nember'] = set_traverse_nums
        summery_count['Expected requests number'] = self.api_number * set_traverse_nums * 2

    def api_testing(self, api_id, required=True):
        api_info = self.api_list[api_id]
        compose_request = ComposeRequest(api_info)
        if required:
            compose_request.compose_required_request()
        request = compose_request.get_required_request
        requests_message = f'Sending: {api_info.http_method.upper()} {api_info.path} {request.url} \n' \
                           f'API_id: {api_info.api_id} header:{request.header}\n' \
                           f''f'data: {request.data}\n'
        summery_count['already send requests number'] += 1
        try:
            request.send_request()
            response = request.get_response
        except:
            status_timeout_log = Log(log_name='timeout_request')
            status_timeout_log.info(requests_message)
            self.timeout_pool[api_info.api_id] += 1
            summery_count['timeout requests number'] += 1
        else:
            response_handle = ResponseJudge(requests_message,
                                            response, api_info, self.success_pool, self.vaild_pool)
            self.success_pool, response_status = response_handle.response_judge()
            if response_status == 2:
                self.status_2xx_pool[api_info.api_id] += 1
                request.genetic_algorithm_success()
                self.success_request_pool[api_id].append(request)
            elif response_status == 4:
                self.status_4xx_pool[api_info.api_id] += 1
                request.genetic_algorithm_faild()
            elif response_status == 5:
                self.status_5xx_pool[api_info.api_id] += 1
                request.genetic_algorithm_success()
        self.visited_pool[api_info.api_id] += 1

    def simple_node_testing(self, node):
        exec_method_list = ['get', 'post', 'put', 'patch', 'delete', 'post']
        for exec_method in exec_method_list:
            if exec_method in node.method_dic:
                self.api_testing(node.method_dic[exec_method])

    def pre_foREST_BFS(self):
        self.node_queue = [self.semantic_tree_root]
        while self.node_queue:
            node = self.node_queue.pop(0)
            self.simple_node_testing(node)
            if node.children:
                self.node_queue += node.children
                random.shuffle(self.node_queue)

    def foREST_test(self):
        self.pre_foREST_BFS()
        # 先执行一遍所有的结点，只执行必选参数

    def post_testing(self, api_id):
        self.api_testing(api_id)
        api_info = self.api_list[api_id]
        compose_request = ComposeRequest(api_info)
        compose_request.compose_required_request()
        requests = compose_request.get_required_request




