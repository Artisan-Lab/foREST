import requests
from utils.foREST_setting import foRESTSetting


class SendRequest:

    def __init__(self, url, method, header, data):
        self.url = url
        self.method = method
        self.base_header = header
        self.data = data
        self.timeout = (10, 10)
        self.response = None

    @staticmethod
    def send_post_request(url, header, data, timeout):
        response = requests.post(url=url, headers=header, data=data, timeout=timeout)
        return response

    @staticmethod
    def send_get_request(url, header, data, timeout):
        response = requests.get(url=url, headers=header, data=data, timeout=timeout)
        return response

    @staticmethod
    def send_delete_request(url, header, data, timeout):
        response = requests.delete(url=url, headers=header, data=data, timeout=timeout)
        return response

    @staticmethod
    def send_put_request(url, header, data, timeout):
        response = requests.put(url=url, headers=header, data=data, timeout=timeout)
        return response

    @staticmethod
    def send_patch_request(url, header, data, timeout):
        response = requests.patch(url=url, headers=header, data=data, timeout=timeout)
        return response

    def get_response(self):
        return self.response

    def send_request(self):
        if self.method == 'post':
            self.response = SendRequest.send_post_request(self.url, self.base_header, self.data, self.timeout)
        if self.method == 'get':
            self.response = SendRequest.send_get_request(self.url, self.base_header, self.data, self.timeout)
        if self.method == 'delete':
            self.response = SendRequest.send_delete_request(self.url, self.base_header, self.data, self.timeout)
        if self.method == 'put':
            self.response = SendRequest.send_put_request(self.url, self.base_header, self.data, self.timeout)
        if self.method == 'patch':
            self.response = SendRequest.send_patch_request(self.url, self.base_header, self.data, self.timeout)

