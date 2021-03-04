import random
import redis
import json

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
qwe = redis.StrictRedis(connection_pool=pool)

strl = '''
[{
    "name": "Tom",
    "gender": "male"
}, {
    "name": "Jack",
    "gender": "male"
}]
'''
# 将字符串转为json格式
print(type(strl))
data = json.loads(strl)
print(type(data))
print(data)


def json_txt(dic_json):
    if isinstance(dic_json, list):
        for dic in dic_json:
            if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic:
                    if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                        json_txt(dic[key])
                        qwe.lpush(str(key), str(dic[key]))
                    else:
                        qwe.lpush(str(key), str(dic[key]))
    else:
        if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
            for key in dic_json:
                if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                    json_txt(dic_json[key])
                    qwe.set(str(key), str(dic_json[key]))
                else:
                    qwe.set(str(key), str(dic_json[key]))

json_txt(data)

list = []
for i in range(qwe.llen('name')): list.append(i+1)
index = random.choice(list)
value = qwe.lindex('name',index)   # 从response的redis中根据name取对应value

print(list)
print(str(value, encoding="utf-8"))
print(qwe.ttl('name'))

# m = 5
# list = []
# for i in range(m):
#     list.append(i+1)
# print(list)
#
#        for i in range(qwe.llen('name')+1): list=[].append(i+1)

# list = [1, 2, 3, 5, 9]
# print ("choice([1, 2, 3, 5, 9]) : ", random.choice(list))