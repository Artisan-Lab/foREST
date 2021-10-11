import json
import requests
from tool.tools import Tool
request_timeout = Tool.readconfig('request', 'timeout')


class Request:

    def __init__(self, base_url, method):
        self.base_url = base_url
        self.url = base_url
        self.method = method
        self.data = {}
        self.header = {}
        self.timeout = request_timeout
        self.path_parameter_list = {}
        self.query_parameter_list = {}
        self.data_parameter_list = {}
        self.header_parameter_list = {}
        self.response = None

    def send_request(self):
        if self.method == "post":
            self.response = requests.post(url=self.url, data=self.data, headers=self.header, timeout=self.timeout)
        if self.method == 'get':
            self.response = requests.get(url=self.url, data=self.data, headers=self.header, timeout=self.timeout)
        if self.method == "delete":
            self.response = requests.delete(url=self.url, data=self.data, headers=self.header, timeout=self.timeout)
        if self.method == "put":
            self.response = requests.put(url=self.url, data=self.data, headers=self.header, timeout=self.timeout)

    @property
    def get_response(self):
        return self.response

    def compose_request(self):
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
            self.data += self.data_parameter_list
        if self.header_parameter_list:
            self.header += self.header_parameter_list

    def add_parameter(self, location, key, value):
        if location == 0:
            self.path_parameter_list[key] = value
        elif location == 1:
            self.query_parameter_list[key] = value
        elif location == 2:
            self.header_parameter_list[key] = value
        elif location == 3:
            self.data_parameter_list[key] = value
