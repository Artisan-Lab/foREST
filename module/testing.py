import re
import json
import datetime
import random
import copy
from module.composerequest import ComposeRequest
from log.get_logging import summery_log, requests_log, status_2xx_log, \
                            status_3xx_log, status_4xx_log, status_5xx_log, status_timeout_log
from log.get_logging import summery_count
from entity.resource_pool import foREST_POST_resource_pool
from module.jsonhandle import JsonHandle
from module.foREST_monitor import foRESTMonitor
from utils.foREST_setting import TESTING_TIME, START_TIME


foREST_POST_resource_pool_copy = copy.deepcopy(foREST_POST_resource_pool)


class Test:
    def __init__(self, semantic_tree_root, api_list, foREST_monitor: foRESTMonitor):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
        self.api_info = None
        self.api_number = len(api_list)
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
        self.foREST_monitor = foREST_monitor
        self.success_api_sequence = []
        summery_count['api number'] = self.api_number
        summery_count['already send rounds'] = 0
        summery_count['success api number'] = 0

    def foREST_tree_based_bfs(self):
        while True:
            self.node_queue = [self.semantic_tree_root]
            while self.node_queue:
                self.node = self.node_queue.pop(0)
                self.node_testing(self.node)
                if self.node.children:
                    for child in self.node.children:
                        self.node_queue.append(child)
            self.traverse_nums += 1
            summery_count['already send rounds'] = self.traverse_nums
            if datetime.datetime.now() - START_TIME > datetime.timedelta(minutes=TESTING_TIME):
                break


    def node_testing(self, node):
        exec_method_list = ['get', 'post', 'put', 'patch', 'delete']
        for exec_method in exec_method_list:
            if exec_method in node.method_dic:
                api_id = node.method_dic[exec_method]
                if exec_method == 'post' and (api_id not in foREST_POST_resource_pool.resource_api_id_dict
                                              or len(foREST_POST_resource_pool.resource_api_id_dict[api_id])) < 100:
                    k = random.randint(1, 5)
                    for _ in range(k):
                        self.api_testing(api_id)
                else:
                    self.api_testing(api_id)

    # def create_topology_graph(self):
    #     topology_graph = [[0 for i in range(self.api_number + 1)] for i in range(self.api_number)]
    #     for api_info in self.api_list:
    #         if api_info.key_depend_api_list:
    #             for depend_api in api_info.key_depend_api_list:
    #                 topology_graph[api_info.api_id][depend_api] = 1
    #         topology_graph[api_info.api_id][-1] = len(api_info.key_depend_api_list)
    #     return topology_graph

    # def topology(self):
    #     while True:
    #         topology_graph = self.create_topology_graph()
    #         while True:
    #             next_api_list = []
    #             min_depend_number = self.api_number
    #             for i in range(self.api_number):
    #                 if min_depend_number > topology_graph[i][-1] > -1:
    #                     min_depend_number = topology_graph[i][-1]
    #                     next_api_list = [i]
    #                 elif topology_graph[i][-1] == min_depend_number:
    #                     next_api_list.append(i)
    #             if next_api_list:
    #                 while next_api_list:
    #                     random.shuffle(next_api_list)
    #                     next_api = next_api_list.pop(0)
    #                     self.api_testing(next_api)
    #                     topology_graph[next_api][-1] = -1
    #                     for j in range(self.api_number):
    #                         if topology_graph[j][next_api]:
    #                             topology_graph[j][next_api] = 0
    #                             topology_graph[j][-1] -= 1
    #             else:
    #                 break
    #         self.traverse_nums += 1
    #         summery_count['already send rounds'] = self.traverse_nums
    #         if datetime.datetime.now() - self.start_time > datetime.timedelta(minutes=self.time):
    #             break

    # def graph_bfs(self):
    #     while True:
    #         topology_graph = self.create_topology_graph()
    #         reset_resource_pool()
    #         while True:
    #             next_api_list = []
    #             min_depend_number = self.api_number
    #             for i in range(self.api_number):
    #                 if min_depend_number > topology_graph[i][-1] > -1:
    #                     min_depend_number = topology_graph[i][-1]
    #                     next_api_list = [i]
    #                 elif topology_graph[i][-1] == min_depend_number:
    #                     next_api_list.append(i)
    #             if next_api_list:
    #                 while next_api_list:
    #                     random.shuffle(next_api_list)
    #                     next_api = next_api_list.pop(0)
    #                     self.api_testing(next_api)
    #                     topology_graph[next_api][-1] = -1
    #                     for j in range(self.api_number):
    #                         if topology_graph[j][next_api]:
    #                             topology_graph[j][next_api] = 0
    #                             topology_graph[j][-1] -= 1
    #             else:
    #                 break
    #         if datetime.datetime.now() - self.start_time > datetime.timedelta(minutes=self.time):
    #             break

    def api_testing(self, api_id):
        self.api_info = self.api_list[api_id]
        self.compose_request = ComposeRequest(self.api_info, self.node)
        self.compose_request.get_path_parameter()
        self.compose_request.compose_required_request()
        if self.api_info.http_method == 'post':
            self.post_api_testing()
        elif self.api_info.http_method == 'delete':
            self.delete_api_testing()
        elif self.api_info.http_method == 'get':
            self.get_api_testing()
        elif self.api_info.http_method == 'put':
            self.put_api_testing()
        elif self.api_info.http_method == 'patch':
            self.patch_api_testing()

    def optional_request_testing(self):
        optional_request_list = self.compose_request.get_optional_request
        for optional_request in optional_request_list:
            self.testing_evaluate(optional_request)

    def post_api_testing(self):
        request = self.compose_request.request
        response_status = self.testing_evaluate(request)
        if response_status == 2:
            self.compose_request.recompose_optional_request()
            self.optional_request_testing()

    def get_api_testing(self):
        request = self.compose_request.request
        response_status = self.testing_evaluate(request)
        if response_status == 2 or response_status == 5:
            self.compose_request.compose_optional_request()
            self.optional_request_testing()

    def put_api_testing(self):
        request = self.compose_request.request
        response_status = self.testing_evaluate(request)
        self.compose_request.compose_optional_request()
        self.optional_request_testing()

    def delete_api_testing(self):
        request = self.compose_request.request
        response_status = self.testing_evaluate(request)
        if response_status == 2 or response_status == 5:
            foREST_POST_resource_pool.delete_resource(self.compose_request.current_parent_source)

    def patch_api_testing(self):
        request = self.compose_request.request
        response_status = self.testing_evaluate(request)

    def testing_evaluate(self, request):
        summery_count['already send requests number'] += 1
        self.request_message = f'Sending: {self.api_info.http_method.upper()} {self.api_info.path} {request.url} \n' \
                           f'API_id: {self.api_info.api_id} header:{request.base_header}\n' \
                           f''f'data: {request.data}\n'
        try:
            request.send_request()
            response = request.get_response()
        except:
            status_timeout_log.info(self.request_message)
            self.timeout_pool[self.api_info.api_id] += 1
            summery_count['timeout requests number'] += 1
            response_status = 0
        else:
            response_status = self.response_handle(request, response)
        return response_status

    def response_handle(self, request, response):
        if JsonHandle.is_json(response.text.split('Connection to server successfully')[0]):
            response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.text} \n\n'
        else:
            response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.raw.data} \n\n'
        requests_log.info(self.request_message + response_message)
        requests_log.info(self.success_pool)
        response_status = 0
        if re.match('2..', str(response.status_code)):
            if request.method == 'post':
                if response.text:
                    foREST_POST_resource_pool.save_response(self.api_info, request,
                                                        json.loads(request.response.text),
                                                        self.compose_request.current_parent_source)
            response_status = 2
            summery_count['2xx requests number'] += 1
            status_2xx_log.info(self.request_message + response_message)
            if self.success_pool[self.api_info.api_id] == 0:
                self.success_pool[self.api_info.api_id] = 1
                summery_count['success api number'] += 1
            request.genetic_algorithm_success()
        elif re.match('3..', str(response.status_code)):
            summery_count['3xx requests number'] += 1
            status_3xx_log.info(self.request_message + response_message)
            response_status = 3
            request.genetic_algorithm_fail()
        elif re.match('4..', str(response.status_code)):
            summery_count['4xx requests number'] += 1
            response_status = 4
            status_4xx_log.info(self.request_message + response_message)
            request.genetic_algorithm_fail()
        elif re.match('5..', str(response.status_code)):
            summery_count['5xx requests number'] += 1
            response_status = 5
            status_5xx_log.info(self.request_message + response_message)
        summery_log.info(str(summery_count))
        return response_status





