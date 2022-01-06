import copy
import json
import numpy as np
from tool.tools import http_header, http_header_no_auth
from module.sendrequest import SendRequest


class Request(SendRequest):

    def __init__(self, base_url, method):
        super().__init__(base_url, method, header={}, data={})
        self.base_url = base_url
        self.method = method
        self.initialization()
        self.path_parameter_list = {}
        self.query_parameter_list = {}
        self.data_parameter_list = {}
        self.header_parameter_list = {}
        self.response = None
        self.genetic_algorithm_list = []

    def reset_base_request(self):
        self.url = self.base_url
        self.data = ''
        if np.random.choice([1, 0], replace=True, p=[0.95, 0.05]):
            self.base_header = copy.deepcopy(http_header)
        else:
            self.base_header = copy.deepcopy(http_header_no_auth)

    def initialization(self):
        self.reset_base_request()
        self.path_parameter_list = {}
        self.query_parameter_list = {}
        self.data_parameter_list = {}
        self.header_parameter_list = {}
        self.response = None
        self.genetic_algorithm_list = []

    def compose_request(self):
        self.reset_base_request()
        if self.path_parameter_list:
            for path_parameter in self.path_parameter_list:
                self.url = self.url.replace('{' + path_parameter + '}', str(self.path_parameter_list[path_parameter]))
        if self.query_parameter_list:
            for query_parameter in self.query_parameter_list:
                if '?' in self.url:
                    self.url = self.url + '&' + str(query_parameter) + '=' + str(self.query_parameter_list[query_parameter])
                else:
                    self.url = self.url + '?' + str(query_parameter) + '=' + str(self.query_parameter_list[query_parameter])
        if self.data_parameter_list:
            self.data = json.dumps(self.data_parameter_list)
        if self.header_parameter_list:
            self.base_header.update(self.header_parameter_list)

    def add_parameter(self, location, key, value):
        if location == 0 or location == 'path':
            self.path_parameter_list[key] = value
        elif location == 1 or location == 'query':
            self.query_parameter_list[key] = value
        elif location == 2 or location == 'header':
            self.header_parameter_list[key] = value
        elif location == 3 or location == 'body':
            self.data_parameter_list[key] = value

    def add_genetic_algorithm(self, genetic_algorithm):
        self.genetic_algorithm_list.append(genetic_algorithm)

    def genetic_algorithm_success(self):
        for genetic_algorithm in self.genetic_algorithm_list:
            genetic_algorithm.winner_success()

    def genetic_algorithm_fail(self):
        for genetic_algorithm in self.genetic_algorithm_list:
            genetic_algorithm.winner_failed()

    @staticmethod
    def copy_genetic_algorithm_list(request):
        algorithm_list = []
        for genetic_algorithm in request.genetic_algorithm_list:
            algorithm_list.append(genetic_algorithm)
        return algorithm_list
