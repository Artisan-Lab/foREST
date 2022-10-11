import copy
import json
import random
import numpy as np
import requests
from entity.api_info import *
from foREST_setting import foRESTSettings


class Request:

    def __init__(self, api_info):
        self.header = {}
        self.data = {}
        self.url = api_info.base_url + api_info.path
        self.method = api_info.http_method
        self.api_info = api_info
        self.base_url = api_info.base_url + api_info.path

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
        self.header = {}
        if np.random.choice([1, 0], replace=True, p=[0.95, 0.05]):
            if self.api_info.consumes:
                self.header["Content-Type"] = random.choice(self.api_info.consumes)
            else:
                self.header["Content_Type"] = "application/json"
            if self.api_info.produces:
                self.header["Accept"] = random.choice(self.api_info.produces)
            if foRESTSettings().header:
                self.header.update(foRESTSettings().header)
        elif random.choice([0,1]):
            self.header["Content_Length"] = random.randint(0,50)

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
        if self.header_parameter_list:
            for key in self.header_parameter_list:
                if isinstance(self.header_parameter_list[key], dict) or isinstance(self.header_parameter_list[key], list):
                    self.header[key] = json.dumps(self.header_parameter_list[key])
                else:
                    self.header[key] = self.header_parameter_list[key]

        if self.data_parameter_list:
            if np.random.choice([1, 0], replace=True, p=[0.05, 0.95]):
                self.data = random.choice([{},"{}"])
                self.depend_point_list = []
                return
            if self.header.get("Content-Type") and self.header["Content-Type"] == "application/x-www-form-urlencoded":
                if None in self.data_parameter_list and len(self.data_parameter_list) == 1:
                    self.data = self.data_parameter_list[None]
                else:
                    self.data = self.data_parameter_list
            elif self.header.get("Content-Type") and self.header["Content-Type"] == "text/plain":
                if len(self.data_parameter_list) == 1:
                    for value in self.data_parameter_list.values():
                        self.data = value
            else:
                if None in self.data_parameter_list and len(self.data_parameter_list) == 1:
                    self.data = json.dumps(self.data_parameter_list[None])
                else:
                    self.data = json.dumps(self.data_parameter_list)


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
        for genetic_algorithm in self.depend_point_list: # type: DependPoint
            genetic_algorithm.add_score()

    def genetic_algorithm_fail(self):
        for genetic_algorithm in self.depend_point_list: # type: DependPoint
            genetic_algorithm.minus_score()

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

