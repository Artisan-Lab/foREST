import datetime
import random
import copy
from testing_render.composerequest import ComposeRequest
from log.get_logging import summery_log, requests_log, status_2xx_log, \
                            status_3xx_log, status_4xx_log, status_5xx_log, status_timeout_log
from log.get_logging import summery_count
import re
import json
from module.jsonhandle import JsonHandle


class Test:
    def __init__(self, semantic_tree_root, api_list, start_time, time=10, max_length=10):
        self.semantic_tree_root = semantic_tree_root
        self.api_list = api_list
        self.api_info = None
        self.api_number = len(api_list)
        self.node = None
        self.dependency_graph = [[0 for j in range(self.api_number)] for i in range(self.api_number)]
        self.success_pool = [0 for i in range(self.api_number)]
        self.visited_pool = [0 for i in range(self.api_number)]
        self.valid_pool = [0 for i in range(self.api_number)]
        self.status_2xx_pool = [0 for i in range(self.api_number)]
        self.status_4xx_pool = [0 for i in range(self.api_number)]
        self.status_5xx_pool = [0 for i in range(self.api_number)]
        self.timeout_pool = [0 for i in range(self.api_number)]
        self.traverse_nums = 0
        self.node_queue = []
        self.request_message = None
        self.compose_request = None
        self.start_time = start_time
        self.time = time
        self.success_api_sequence = []
        self.max_length = max_length
        summery_count['api number'] = self.api_number
        summery_count['already send rounds'] = 0
        summery_count['success api number'] = 0

    def create_topology_graph(self):
        topology_graph = [[0 for i in range(self.api_number + 1)] for i in range(self.api_number)]
        for api_info in self.api_list:
            if api_info.key_depend_api_list:
                for depend_api in api_info.key_depend_api_list:
                    topology_graph[api_info.api_id][depend_api] = 1
            topology_graph[api_info.api_id][-1] = len(api_info.key_depend_api_list)
        return topology_graph

    def graph_bfs(self):
        while True:
            n = 1
            while n<=self.max_length:
                self.extend()
                self.render()
            if datetime.datetime.now() - self.start_time > datetime.timedelta(minutes=self.time):
                break

    def extend(self):
        new_seqset = []
        if not self.success_api_sequence:
            for api_info in self.api_list:
                if self.dependencies([], api_info):
                    new_seqset.append([api_info])
        else:
            for seq in self.success_api_sequence:
                for api_info in self.api_list:
                    if self.dependencies(seq, api_info):
                        base_seq = copy.deepcopy(seq)
                        base_seq.append(api_info)
                        new_seqset.append(base_seq)
        self.success_api_sequence = new_seqset

    def render(self):
        new_seq_set = []
        for seq in self.success_api_sequence:
            api_info = seq.pop(-1)
            compose_request = ComposeRequest(api_info,seq)
            new_request = compose_request.compose_required_request()
            seq.append(new_request)
            new_seq_set.append(seq)
            for new_seq in new_seq_set:
                if not self.send_request(new_seq):
                    new_seq_set.remove(new_seq)
        self.success_api_sequence = new_seq_set

    def send_request(self, seqs):
        for request in seqs:
            self.api_info = self.api_list[request.api_id]
            request.send_request()
            status_code = self.testing_evaluate(request)
            if status_code == 4:
                return False
        return True

    def dependencies(self, seqs, api_info):
        api_id_list = []
        for seq in seqs:
            api_id_list.append(seq.api_id)
        for field_info in api_info.req_param:
            if field_info.require:
                depend_list=[]
                for path in field_info.depend_list[0]:
                    depend_list.append(path[0])
                lst3 = list(set(api_id_list)&set(depend_list))
                if not lst3:
                    return False
        return True

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
        requests_log.warning(self.request_message + response_message)
        requests_log.warning(self.success_pool)
        response_status = 0
        if re.match('2..', str(response.status_code)):
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
        summery_log.debug(str(summery_count))
        return response_status





