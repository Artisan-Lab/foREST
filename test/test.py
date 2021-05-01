# from multiprocessing import Queue,Process
# import os,time,random
#
# #添加数据函数
# def proc_write(queue,urls):
#     print("进程(%s)正在写入..."%(os.getpid()))
#     for url in urls:
#         queue.put(url)
#         print("%s被写入到队列中"%(url))
#         time.sleep(random.random()*3)
#
# #读取数据函数
# def proc_read(queue):
#     print("进程(%s)正在读取..."%(os.getpid()))
#
#     while True:
#         url = queue.get();
#         print("从队列中提取到:%s"%(url))
#
# if __name__ =="__main__":
#     queue = Queue()
#     proc_writer1 = Process(target=proc_write,args=(queue,["ur1","ur2","ur3","ur4"]))
#     proc_writer2 = Process(target=proc_write,args=(queue,["ur5","ur6","ur7","ur8"]))
#     proc_reader = Process(target=proc_read,args=(queue,))
#     proc_writer1.start()
#     proc_writer2.start()
#     proc_reader.start()
#     proc_writer1.join()
#     proc_writer2.join()
#     proc_reader.terminate()
# import time
#
# from module.Coverage_get_tool import GetCoverage
#
# a = time.time()
# print(GetCoverage.getCoverage_rate_executed_code('http://10.177.74.168:8000/'))
# b = time.time()
# print(b-a)
'''
{'/var/www/html/wp-load.php': '11% (1/9)',
'/var/www/html/wp-includes/load.php': '34% (190/564)',
'/var/www/html/wp-includes/pomo/entry.php': '5% (2/39)',
'/var/www/html/wp-includes/class-wp-dependency.php': '39% (9/23)',
'/var/www/html/wp-includes/sitemaps/class-wp-sitemaps.php': '45% (39/87)'}
'''
# a ='a'
# if a:
#     print(1)

# coding:utf-8

# import requests
#
# # 请求url
# url = "http://httpbin.org/post"
#
# # 请求头
# headers = {
#     "Accept": "*/*",
#     "Accept-Encoding": "gzip, deflate",
#     "User-Agent": "python-requests/2.9.1",
# }
#
# # 查询字符串
# params = {'name': 'Jack', 'age': '24'}
#
# r = requests.post(url=url, headers=headers, data=params)
#
# print (r.status_code)  # 获取响应状态码
# print (r.content)  # 获取响应消息
# print(r.json())
# if __name__ == "__main__":
#     pass
# a = 'dasfg'
# print(a[-1])
# print(a[:-1])
#

# from module.Combination import Combination
# a ={1:2}
# listt = a.keys()
# print(Combination.get_combine(Combination,listt))
# a = Combination.get_combine(Combination,listt)
import ast
import json

a = [{3:1},{2:3}]
# c = {}
# for b in a:
#     print(type(b))
#     c[list(b.keys())[0]] = list(b.values())[0]
# print(c)


# a = {3:'145'}
# b = a.keys()
# print(b)
# print(type(b))
# b = str(b)
# print(type(b))
# print(list(a[b])[-1])

# a = {3:2,2:5}
# for i in a.keys():
#     print(i)

def a():
    b = {}
    for i in range(5):
        b[i] = i+1
    c(b)

def c(b):
    for i in b.keys():
        print(i)
a()







# a = [1,2,3,4,5,6]
# b=[2,4,3]
# c =set(a)
# d = set(b)
# e = c^d
# print(type(e))
# f = list(e)
# print(f)
# print(type(f))
import urllib






# a ={1:2,3:4,5:6,7:8}
# a.keys()

