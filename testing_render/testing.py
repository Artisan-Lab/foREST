import random

from testing_render.composerequest import ComposeRequest
from log.get_logging import Log
from testing_render.responsehandle import ResponseJudge
from log.get_logging import summery_count


class Test:
    def __init__(self, semantic_tree_root, api_list, set_traverse_nums=1):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
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
        summery_count['api number'] = self.api_number
        summery_count['test rounds nember'] = set_traverse_nums
        summery_count['Expected requests number'] = self.api_number * set_traverse_nums * 2

    def api_testing(self, api_id):
        api_info = self.api_list[api_id]
        compose_request = ComposeRequest(api_info)
        compose_request.compose_request()
        request = compose_request.get_request
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
            elif response_status == 4:
                self.status_4xx_pool[api_info.api_id] += 1
                request.genetic_algorithm_faild()
            elif response_status == 5:
                self.status_5xx_pool[api_info.api_id] += 1
                request.genetic_algorithm_success()
        self.visited_pool[api_info.api_id] += 1

    def node_testing(self, node):
        exec_method_list = ['post', 'get', 'put', 'patch', 'delete', 'post']
        for exec_method in exec_method_list:
            if exec_method in node.method_dic:
                self.api_testing(node.method_dic[exec_method])

    def foREST_BFS(self):
        while self.traverse_nums < self.set_traverse_nums:
            self.node_queue = [self.semantic_tree_root]
            while self.node_queue:
                node = self.node_queue.pop(0)
                self.node_testing(node)
                if node.children:
                    for child in node.children:
                        self.node_queue.append(child)
            self.traverse_nums += 1

    def create_topology_graph(self):
        topology_graph = [[0 for i in range(self.api_number+1)] for i in range(self.api_number)]
        for api_info in self.api_list:
            if api_info.key_depend_api_list:
                for depend_api in api_info.key_depend_api_list:
                    topology_graph[api_info.api_id][depend_api] = 1
            topology_graph[api_info.api_id][-1] = len(api_info.key_depend_api_list)
        return topology_graph

    def topology(self):
        while self.traverse_nums < self.set_traverse_nums:
            topology_graph = self.create_topology_graph()
            while True:
                next_api_list = []
                min_depend_number = self.api_number
                for i in range(self.api_number):
                    if min_depend_number > topology_graph[i][-1] > -1:
                        min_depend_number = topology_graph[i][-1]
                        next_api_list = [i]
                    elif topology_graph[i][-1] == min_depend_number:
                        next_api_list.append(i)
                if next_api_list:
                    while next_api_list:
                        random.shuffle(next_api_list)
                        next_api = next_api_list.pop(0)
                        self.api_testing(next_api)
                        topology_graph[next_api][-1] = -1
                        for j in range(self.api_number):
                            if topology_graph[j][next_api]:
                                topology_graph[j][next_api] = 0
                                topology_graph[j][-1] -= 1
                else:
                    break
            self.traverse_nums += 1

