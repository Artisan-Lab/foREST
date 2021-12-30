from .field_info import *


class api_info:

    def __init__(self, api_id, base_url, path, req_param, resp_param, http_method):
        self.api_id = api_id
        self.base_url = base_url
        self.path = path
        self.close_api = []
        self.key_depend_api_list = []
        self.req_param = req_param         # type: list[field_info]
        self.resp_param = resp_param       # type: list[field_info]
        self.http_method = http_method




