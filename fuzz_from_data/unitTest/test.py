# from jsonMutation import JsonMutation
# from jsonTree import Tree
#
# jsonTree = Tree(
#     '{"id": 244, "excerpt": "04o0zplIvuOGRBL7Eqy6K1lG9WgHdZTd", "status": "publish", "content": "restfulAPITesting"}')
# jsonTree.export_img("original.png")
# jsonTree.print()
# print('muating value!')
# JsonMutation.mutate_value(jsonTree)
# jsonTree.print()
# JsonMutation.drop(jsonTree)
# jsonTree.print()
# # JsonMutation.select(jsonTree)
# jsonTree.print()
# JsonMutation.duplicate(jsonTree)
# jsonTree.print()
# jsonTree.export_img("mutated.png")
# print(jsonTree.dump())


# from queryStringMutation import QueryStringMutation
#
# queryStringMutation = QueryStringMutation("a=1&b=2")
# a = queryStringMutation.mutate_value()
# print()
# proxyDict = {
#               "http": 'http://cwx1038422:OStem@00@openproxy.huawei.com:8080',
#               "https": 'https://cwx1038422:OStem@00@openproxy.huawei.com:8080'
#             }
# import requests as http_requests
# # resp = http_requests.request(method='get',url='http://fuxi.huawei.com:443/pipelineserv/api/v2/pipelineinstance/pkginfo/476251568624128',proxies=proxyDict)
# resp = http_requests.request(method='get',url='https://100.94.16.180:443/deploy/api/v1/ping',proxies=proxyDict)
# print(resp)


# import requests as http_requests
# # resp = http_requests.request(method='get',url='http://fuxi.huawei.com:443/pipelineserv/api/v2/pipelineinstance/pkginfo/476251568624128',proxies=proxyDict)
# resp = http_requests.request(method='get', url='http://fuxi-beta.inhuawei.com/deploy/api/v1/ping')
# print(resp)


"""
it works
"""
# import json
# content = []
# with open('luffy_restapi_testcase_1.json',encoding='UTF-8') as f:
#     temp = json.load(f)
#     item_list = temp['RECORDS']
#     for item in item_list:
#         request_field = item['request'] # this is a string
#         request_obj = json.loads(request_field)[0]
#         headers = request_obj['headers']
#         paramsMap = request_obj['paramsMap']
#         method = request_obj['method']
#         url = request_obj['requestURL']
#         body = request_obj['body'] # this is a string
#
#
#         print(item)
#         print(item)

# import  json
# import requests
# total_dict = {
# "request": "[{\"headers\":{\"content-length\":\"0\",\"sec-fetch-site\":\"same-origin\",\"x-forwarded-port\":\"443\",\"userid\":\"swx646733\",\"authorization\":null,\"x-envoy-external-address\":\"100.79.64.165\",\"sec-ch-ua-mobile\":\"?0\",\"x-forwarded-host\":\"fuxi.huawei.com\",\"host\":\"fuxi.huawei.com\",\"x-titan-userid\":\"swx646733\",\"systemuser\":\"283\",\"sec-fetch-mode\":\"cors\",\"x-request-id\":\"60df52c5-7bd7-4597-a584-43a8f52d8e3f\",\"x-forwarded-proto\":\"http\",\"accept-language\":\"zh-CN,zh;q=0.9\",\"cookie\":null,\"x-forwarded-for\":\"10.190.114.252\",\"accept\":\"application/json, text/plain, */*\",\"x-real-ip\":\"10.190.114.252\",\"sec-ch-ua\":\"\\\" Not;A Brand\\\";v=\\\"99\\\", \\\"Google Chrome\\\";v=\\\"91\\\", \\\"Chromium\\\";v=\\\"91\\\"\",\"x-envoy-expected-rq-timeout-ms\":\"499000\",\"accept-encoding\":\"gzip, deflate, br\",\"username\":\"sunweiqiang WX646733\",\"user-agent\":\"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36\",\"sec-fetch-dest\":\"empty\"},\"paramsMap\":{\"appCompId\":[\"10064985\"],\"meregedTag\":[\"0709\"]},\"responseHeaders\":{\"Vary\":[\"Origin\",\"Access-Control-Request-Method\",\"Access-Control-Request-Headers\"],\"Set-Cookie\":\"rememberMe=deleteMe; Path=/pipelineserv; Max-Age=0; Expires=Sat, 10-Jul-2021 14:59:20 GMT; SameSite=lax\"},\"method\":\"GET\",\"port\":8888,\"requestURL\":\"http://fuxi-pipeline-api-mutation.pipeline-beta.dev.titan.huawei.com\",\"requestURI\":\"/pipelineserv/api/v1/change/mergednopub\",\"body\":\"\",\"contentType\":null}]",
# }
#
# request_str = total_dict['request']
# obj = json.loads(request_str)
#
#
# print(obj[0]['headers'])
# headers = obj[0]['headers']
# request_url = obj[0]['requestURL']
# resp = requests.request(method='get',url=request_url,headers=headers)
# print(resp)

# print(request)
# print(request['headers'])
# print(request['requestURL'])


import requests
import os
os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
#print(requests.get(url='http://fuxi-pipeline-api-mutation.pipeline-beta.dev.titan.huawei.com/pipelineserv/api/v2/pipelineinstance/comp_name/476105945625536?',headers={'x-request-id': '41c69b8e-ead0-4e0a-a533-128c902c2308', 'content-length': '0', 'x-forwarded-proto': 'http', 'x-forwarded-port': '80', 'x-forwarded-for': '100.94.0.186', 'x-real-ip': '100.94.0.186', 'authorization': None, 'x-envoy-external-address': '100.79.64.164', 'x-forwarded-host': 'fuxi.huawei.com', 'host': 'fuxi.huawei.com', 'content-type': 'application/json', 'x-envoy-expected-rq-timeout-ms': '499000', 'accept-encoding': 'gzip', 'user-agent': 'unirest-java/1.3.11'}))
print(requests.get(url='http://fuxi-pipeline-api-mutation.pipeline-beta.dev.titan.huawei.com/pipelineserv/api/v2/pipelineinstance/comp_name/476105945625536?',headers={  'x-real-ip': '100.94.0.186', 'authorization': None, 'x-envoy-external-address': '100.79.64.164', 'x-forwarded-host': 'fuxi.huawei.com', 'host': 'fuxi.huawei.com', 'content-type': 'application/json', 'x-envoy-expected-rq-timeout-ms': '499000', 'accept-encoding': 'gzip', 'user-agent': 'unirest-java/1.3.11'}))