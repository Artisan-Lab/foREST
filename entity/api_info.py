from common.common_utils import comutil
from .field_info import *
from common import *

class api_info:
    def __init__(self,api_id,path,req_param,resp_param,http_method):
        self.api_id = api_id
        self.path = path
        self.req_param = req_param         # type: list[field_info]
        self.resp_param = resp_param       # type: list[field_info]
        self.http_method = http_method
        self.req_field_names = []
        for i in list(self.req_param):
            name = i.field_name
            self.req_field_names.append(name)

    # 判断是否存在依赖关系，从消费者角度
    def has_dep(self,api_info):
        if(comutil.has_intersec(self.req_field_names,api_info.req_field_names)):
            return True
        else:
            return False
