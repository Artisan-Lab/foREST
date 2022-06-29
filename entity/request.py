import copy
import json
import numpy as np
import requests
from entity.api_info import *
from foREST_setting import foRESTSettings


class Request:

    def __init__(self, base_url, method):
        self.header = {}
        self.data = {}
        self.url = base_url
        self.method = method

        self.base_url = base_url

        self.path_parameter_list = {}
        self.query_parameter_list = {}
        self.data_parameter_list = {}
        self.header_parameter_list = {}

        self.response_code = 0
        self.response = None
        self.depend_point_list = []  # type:[DependPoint]

    def reset_base_request(self):
        self.url = self.base_url
        self.data = ''
        if np.random.choice([1, 0], replace=True, p=[0.95, 0.05]):
            self.header = foRESTSettings().header
        else:
            self.header = {}

    def initialization(self):
        self.reset_base_request()
        self.path_parameter_list = {}
        self.query_parameter_list = {}
        self.data_parameter_list = {}
        self.header_parameter_list = {}
        self.response = None
        self.depend_point_list = []  # type: [DependPoint]

    def compose_request(self):
        self.reset_base_request()
        if self.path_parameter_list:
            for path_parameter in self.path_parameter_list:
                self.url = self.url.replace('{' + path_parameter + '}', str(self.path_parameter_list[path_parameter]))
        if self.query_parameter_list:
            for query_parameter in self.query_parameter_list:
                if '?' in self.url:
                    self.url = self.url + '&' + str(query_parameter) + '=' \
                               + str(self.query_parameter_list[query_parameter])
                else:
                    self.url = self.url + '?' + str(query_parameter) + '=' \
                               + str(self.query_parameter_list[query_parameter])
        if self.data_parameter_list:
            self.data = json.dumps(self.data_parameter_list)
        if self.header_parameter_list:
            self.header.update(self.header_parameter_list)

    def add_parameter(self, location, key, value):
        if location == 0 or location == 'path':
            self.path_parameter_list[key] = value
        elif location == 1 or location == 'query':
            self.query_parameter_list[key] = value
        elif location == 2 or location == 'header':
            self.header_parameter_list[key] = value
        elif location == 3 or location == 'body':
            self.data_parameter_list[key] = value

    def add_genetic_algorithm(self, dependency_point):
        self.depend_point_list.append(dependency_point)

    def genetic_algorithm_success(self):
        for genetic_algorithm in self.depend_point_list:
            genetic_algorithm.winner_success()

    def genetic_algorithm_fail(self):
        for genetic_algorithm in self.depend_point_list:
            genetic_algorithm

    @staticmethod
    def copy_genetic_algorithm_list(request):
        algorithm_list = []
        for genetic_algorithm in request.depend_point_list:
            algorithm_list.append(genetic_algorithm)
        return algorithm_list

    def send_request(self):
        kwargs = dict()
        kwargs["url"] = self.url
        kwargs["headers"] = self.header
        if len(self.data):
            kwargs["data"] = self.data
        try:
            response = getattr(requests, self.method.lower())(**kwargs, timeout=foRESTSettings().request_timeout) # type: requests.Response
        except TypeError:
            raise Exception("request type error: {}".format(self.method))
        except requests.exceptions.Timeout:
            response = None
        except requests.exceptions.TooManyRedirects:
            raise Exception("bad url, try a different one\n url: {}".format(self.url))
        except requests.exceptions.RequestException:
            response = None
        if response is None:
            self.response_code = 0
        else:
            self.response_code = response.status_code
        self.response = response

