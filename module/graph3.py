from module.parse import parse
import os
from prance import ResolvingParser

'''
静态分析：机器学习NLP，匹配两段文字的语义
count记录相似程度：
    0 代表不相关
    非0 代表request和response的需求parameter的相近程度
'''
def dependency2(req_field_info, resp_field_info):
    count = 0
    if req_field_info.field_name == resp_field_info.field_name:
        count = 1
        req_de = req_field_info.description
        req_na = req_field_info.field_name
        resp_de = resp_field_info.description
        resp_na = resp_field_info.field_name

        return count
    else:
        return count