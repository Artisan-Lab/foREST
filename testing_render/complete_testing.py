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
            if JsonHandle.json_judge(response.text):
                response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.text} \n\n'
            else:
                response_message = f'Received: \'HTTP/1.1 {response.status_code} response : {response.raw.data} \n\n'
            requests_log.warning(self.request_message + response_message)
            response_status= 0
            if re.match('2..', str(response.status_code)):
                response_status = 2
                summery_count['2xx requests number'] += 1
                status_2xx_log.info(self.request_message + response_message)
                self.success_pool[self.api_info.api_id] = 1
                request.genetic_algorithm_success()
                redis_response_handle.add_data_to_redis(response, self.api_info)
            elif re.match('3..', str(response.status_code)):
                summery_count['3xx requests number'] += 1
                response_status = 3
                request.genetic_algorithm_faild()
            elif re.match('4..', str(response.status_code)):
                summery_count['4xx requests number'] += 1
                response_status = 4
                status_4xx_log.info(self.request_message + response_message)
                request.genetic_algorithm_faild()
            elif re.match('5..', str(response.status_code)):
                summery_count['5xx requests number'] += 1
                response_status = 5
                status_5xx_log.info(self.request_message + response_message)
            summery_log.debug(str(summery_count))
        return response_status

    def api_testing(self, api_id):
        self.api_info = self.api_list[api_id]
        compose_request = ComposeRequest(self.api_info)
        compose_request.compose_required_request()
        request = compose_request.get_required_request()
        response_status = self.testing_evaluate(request)
        if request.method == 'put':
            optional_request_list = compose_request.get_optional_request()
            for optional_request in optional_request_list:
                self.testing_evaluate(optional_request)
        if response_status == 2:
            optional_request_list = compose_request.get_optional_request()
            for optional_request in optional_request_list:
                self.testing_evaluate(optional_request)

    def node_testing(self, node):
        exec_method_list = ['get', 'post', 'put', 'patch', 'delete', 'post']
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

    # def create_topology_graph(self):
    #     topology_graph = [[0 for i in range(self.api_number+1)] for i in range(self.api_number)]
    #     for api_info in self.api_list:
    #         if api_info.key_depend_api_list:
    #             for depend_api in api_info.key_depend_api_list:
    #                 topology_graph[api_info.api_id][depend_api] = 1
    #         topology_graph[api_info.api_id][-1] = len(api_info.key_depend_api_list)
    #     return topology_graph
    #
    # def topology(self):
    #     while self.traverse_nums < self.set_traverse_nums:
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

