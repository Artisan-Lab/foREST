from prance import ResolvingParser
import requests
import re
#模糊处理
def fuzz(type):
    if 'integer' == type:
        return 21413040 #这里是project Id
    elif 'string' == type:
        return "master"

#测试单元
class testUnit:
    #初始化数据
    def __init__(self,method,url,data):
        self.method = method
        self.url = url
        self.data = data

    #执行测试
    def exec(self):
        if '?' in  self.url:
            # 配置token
            self.url = self.url + "&private_token=LP3AsYtjHF6sSoxsenAn"
        else:
            self.url = self.url + "?private_token=LP3AsYtjHF6sSoxsenAn"
        #请求API
        print("exec " + method + " " + self.url)
        if method == 'get':
            return requests.get(self.url)
        elif method == 'post':
            return requests.post(self.url)
        elif method == 'delete':
            return requests.delete(self.url)
        elif method == 'put':
            return requests.put(self.url)
        else:
            print("NOT SUPPORTED " + method)
            return None
        #错误处理
        #依赖处理
        pass



#解析规范
parser = ResolvingParser("C://Users//litianyu//Desktop//project.yaml")
spec = parser.specification

servers = spec.get("servers")
for server in servers:
    #获取根路径
    url = server.get("url")
    #解析API路径的其他部分和参数
    paths = spec.get("paths")
    for path in paths:
        #completeUrl:根目录加资源路径，但是需要进一步处理
        completeUrl = url[0:len(url) - 1] + path
        methods = paths.get(path)
        for method in methods:
            params = methods.get(method).get("parameters")
            data = ''
            flag = 0;
            for param in params:
                # 标识是不是第一次循环,query用来判断是否要加'?'
                inType = param.get('in')
                type = param.get('schema').get('type')
                name = param.get('name')
                value = fuzz(type)
                #不同的in对应不同的数据
                if inType == 'path':
                    completeUrl = completeUrl.replace('{' + name + '}',str(value))
                elif inType == 'query':
                    #url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        completeUrl = completeUrl + "?" + str(name) + "=" + str(value)
                    else:
                        completeUrl = completeUrl + "&" + str(name) + "=" + str(value)
                elif inType == 'body':
                    #参数组成json字符串 ==> data
                    pass

            unit = testUnit(method, completeUrl, data)
            response = unit.exec()
            print(response.text)
