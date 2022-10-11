import re
import random
from foREST_setting import foRESTSettings
from module.testing.composerequest import ComposeRequest
from log.get_logging import *
from entity.resource_pool import resource_pool
from entity.request import Request
from module.utils.utils import JsonHandle
from module.foREST_monitor.foREST_monitor import Monitor


class TestingMonitor:

    def __init__(self, semantic_tree_root, alternative_sequence=None):
        self.semantic_tree_root = semantic_tree_root
        self.alternative_sequence = alternative_sequence
        self.api_list = Monitor().api_list
        self.api_info = None
        self.api_number = len(self.api_list)
        self.node = None
        self.dependency_graph = [[0 for _ in range(self.api_number)] for i in range(self.api_number)]
        self.success_pool = [0 for _ in range(self.api_number)]
        self.visited_pool = [0 for _ in range(self.api_number)]
        self.valid_pool = [0 for _ in range(self.api_number)]
        self.status_2xx_pool = [0 for _ in range(self.api_number)]
        self.status_4xx_pool = [0 for _ in range(self.api_number)]
        self.status_5xx_pool = [0 for _ in range(self.api_number)]
        self.timeout_pool = [0 for _ in range(self.api_number)]
        self.traverse_nums = 0
        self.node_queue = []
        self.request_message = None
        self.compose_request = None
        self.success_api_sequence = []
        self.summery_count = {'api number': self.api_number, 'already send requests number': 0,
                              '2xx requests number': 0, '4xx requests number': 0, '3xx requests number': 0,
                              '5xx requests number': 0, 'timeout requests number': 0, 'already send rounds': 0,
                              'success api number': 0}

    def foREST_tree_based_bfs(self):
        while Monitor().time_monitor.is_alive():
            self.node_queue = [self.semantic_tree_root]
            while self.node_queue:
                self.node = self.node_queue.pop(0)
                self.node_testing(self.node)
                if self.node.children:
                    for child in self.node.children:
                        self.node_queue.append(child)
            self.traverse_nums += 1
            self.summery_count['already send rounds'] = self.traverse_nums
            result_log.save_and_print(self.summery_count)

    def node_testing(self, node):
        exec_method_list = ['get', 'post', 'put', 'patch', 'delete']
        for exec_method in exec_method_list:
            if exec_method in node.method_dic:
                api_id = node.method_dic[exec_method]
                if exec_method == 'post':
                    k = random.randint(1, 5)
                    for _ in range(k):
                        self.api_testing(api_id)
                else:
                    self.api_testing(api_id)
        for method in node.method_dic:
            if method not in exec_method_list:
                api_id = node.method_dic[method]
                self.api_testing(api_id)

    def create_topology_graph(self):
        topology_graph = [[0 for i in range(self.api_number + 1)] for i in range(self.api_number)]
        for api_info in self.api_list:
            if api_info.key_depend_api_list:
                for depend_api in api_info.key_depend_api_list:
                    topology_graph[api_info.api_id][depend_api] = 1
            topology_graph[api_info.api_id][-1] = len(api_info.key_depend_api_list)
        return topology_graph

    def topology(self):
        while Monitor().time_monitor.is_alive():
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
            self.summery_count['already send rounds'] = self.traverse_nums

    def graph_bfs(self):
        while Monitor().time_monitor.is_alive():
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

    def api_testing(self, api_id):
        self.api_info = self.api_list[api_id]
        self.compose_request = ComposeRequest(self.api_info, self.node)
        self.compose_request.get_path_parameter()
        self.compose_request.compose_required_request()
        requests = self.compose_request.request
        requests_status = self.testing_evaluate(requests)
        self.compose_request.compose_optional_request()
        self.optional_request_testing()

    def optional_request_testing(self):
        optional_request_list = self.compose_request.optional_request
        for optional_request in optional_request_list:
            self.testing_evaluate(optional_request)

    def testing_evaluate(self, request: Request):
        self.summery_count['already send requests number'] += 1
        self.request_message = f'Sending: {self.api_info.http_method.upper()} {self.api_info.path} {request.url} \n' \
                           f'API_id: {self.api_info.api_id} header:{request.header}\n' \
                           f''f'data: {request.data}\n'
        try:
            request.send_request()
        except:
            status_timeout_log.save(self.request_message)
            self.timeout_pool[self.api_info.api_id] += 1
            self.summery_count['timeout requests number'] += 1
        if request.response is not None:
            response_status = self.response_handle(request)
        else:
            response_status = 0
        return response_status

    def response_handle(self, request: Request):
        response = request.response
        if JsonHandle.is_json(request.response.text):
            response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.text} \n\n'
        else:
            response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.text} \n\n'
        requests_log.save(self.request_message + response_message)
        summery_log.save(self.success_pool)
        response_status = 0
        if re.match('2..', str(response.status_code)):
            if response.text and JsonHandle.is_json(response.text):
                resource_pool().create_resource(self.api_info,
                                                json.loads(request.response.text), request,
                                                self.compose_request.parent_resource)
            response_status = 2
            self.summery_count['2xx requests number'] += 1
            status_2xx_log.save(self.request_message + response_message)
            if self.success_pool[self.api_info.api_id] == 0:
                self.success_pool[self.api_info.api_id] = 1
                self.summery_count['success api number'] += 1
            request.genetic_algorithm_success()
        elif re.match('3..', str(response.status_code)):
            self.summery_count['3xx requests number'] += 1
            status_3xx_log.save(self.request_message + response_message)
            response_status = 3
            request.genetic_algorithm_fail()
        elif re.match('4..', str(response.status_code)):
            self.summery_count['4xx requests number'] += 1
            response_status = 4
            status_4xx_log.save(self.request_message + response_message)
            request.genetic_algorithm_fail()
        elif re.match('5..', str(response.status_code)):
            self.summery_count['5xx requests number'] += 1
            response_status = 5
            status_5xx_log.save(self.request_message + response_message)
        summery_log.save(str(self.summery_count))
        Monitor().time_monitor.message = f"Already send requests {self.summery_count['already send requests number']}, " \
                                         f"2xx requests number {self.summery_count['2xx requests number']}, " \
                                         f"success API number {self.summery_count['success api number']}"
        return response_status





