import random
import sys
from module.Fuzz_value1 import traversal,fuzzgraph
from module.dep_analysis import get_dep_info
from module.parse import parse
import redis
from rest_framework.utils import json
import requests

###########################      连接redis-pool      ##############################

pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
# req = redis.StrictRedis(connection_pool=pool)
resp = redis.StrictRedis(connection_pool=pool)

post = redis.StrictRedis(connection_pool=pool)
post.lpush('api_id_p', '')
delete = redis.StrictRedis(connection_pool=pool)
delete.lpush('api_id_d', '')

fuzz_success = redis.StrictRedis(connection_pool=pool)
#################################     模糊处理    ##################################
def fuzz(type):
    if 'integer' == type:
        # sys.maxsize整数最大值9223372036854775807， 整数最小值为-sys.maxsize-1 -9223372036854775808
        # sys.float_info.max float最大值为2.2250738585072014e-308 ,sys.float_info.min float最大值为1.7976931348623157e+308
        list_integer = [1,2,0,3,-45,-51,-82,
                        sys.maxsize,-sys.maxsize-1,sys.float_info.max,sys.float_info.min]

        return random.choice(list_integer)
    elif 'string' == type:
        # 我就随便写写，我也不知道写啥。。。
        list_string = ['3171261@qq.com','CommonLisp','Concrete5','John Doe',
                       'https://gitlab.example.com/api/v4/templates/gitignores/Ruby',
                       '# This file is a template, and might need editing',
                       '!@@#$$%%%^^^',
                       '(^&%GBH#T$G"""""""""""DFHBD"BDGVDFVWEF$$53346542@##@$#@%$##',
                       '2012-10-22T14:13:35Z',
                       'PRIVATE-TOKEN: <your_access_token>" "https://gitlab.example.com/api/v4/groups/:id/access_requests',
                       '/uploads/-/system/appearance/logo/1/logo.png',
                       '#e75e40','#ffffff','logo=@/path/to/logo.png','5832fc6e14300a0d962240a8144466eef4ee93ef0d218477e55f11cf12fc3737'
                       'ee1dd64b6adc89cf7e2c23099301ccc2c61b441064e9324d963c46902a85ec34',
                       '127.0.0.1','hello@flightjs.com']

        return random.choice(list_string)

########################   遍历json文件所有的key以及对应的value  #######################

def json_txt(dic_json):
    if isinstance(dic_json, list):
        for dic in dic_json:
            if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic:
                    if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                        json_txt(dic[key])
                        resp.lpush(str(key), str(dic[key]))
                    else:
                        resp.lpush(str(key), str(dic[key]))
    else:
        if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
            for key in dic_json:
                if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                    json_txt(dic_json[key])
                    resp.lpush(str(key), str(dic_json[key]))
                else:
                    resp.lpush(str(key), str(dic_json[key]))


api_info_list = parse(1.0)
matrix, weight_info_list = get_dep_info(api_info_list)
print(matrix)
graph = matrix.tolist()
post_api_list = []

def post_first(api_info_list):
    for api_info in api_info_list:
        if api_info.http_method == 'post':
            post_api_list.append(api_info)

post_first(api_info_list)

def run_fivetimes_post_api(post_api_list):
    method = 'post'
    for post_api in post_api_list:
        for i in range(1):
            url = post_api.path
            val = 0
            headers = {'Cookie':'experimentation_subject_id=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkltTTFObVF4TVdJM0xUUmpZVFl0TkdJME1pMDVPV1kxTFRSaFpEWTFZemRtTkdOaE1TST0iLCJleHAiOm51bGwsInB1ciI6ImNvb2tpZS5leHBlcmltZW50YXRpb25fc3ViamVjdF9pZCJ9fQ==--7e1889f3f6917b34deee402018db2004cd57a385; known_sign_in=WUVwYkUzbWo4ZWMrM0krWXV4KytRZCtYWnhDVXVXRy9vN1BBVnZkMEJnMmxtNlgrQktZT0VMUzJxeUNVc2w2Y29VbUxmbkw3eE5yKzd3SkR1NVlLbE9Wemp5SDliZjNzTXNwV2tyc1RxMFg5T3dNUGhFRStjOEVpYzFNeW1ZWGItLVEyMXEyMzRaekFFeGFwQnFhSy9EeGc9PQ==--f3f5474baafa15eb17fe16ed07c5ed0e79e1566c; _gitlab_session=ff9da167218b4e43e2a036f346637011; event_filter=all; sidebar_collapsed=false; wordpress_test_cookie=WP+Cookie+check; wordpress_logged_in_5a49a2df89d0cacb829057261d919dc3=username|1616557256|XBmAXCpRawXqTezo8FIO6yVx3ZnArdDNTiDR5877clR|a5d6e3170e9b9a2f51438e474d146ed3180f14f6823a4c12f13269a1984dddea; wp-settings-time-1=1616384466'
                        }
            data = []
            for field_info in post_api.req_param:
                # if field_info.require:
                flag = '0'
                location = field_info.location
                field_type = field_info.field_type
                value_fuzz = fuzz(field_type)
                enum = field_info.enum
                if enum != None:
                    value_enum = random.choice(enum)
                    value = value_enum
                else:
                    value = value_fuzz
                val = value
                '''
                不同的in对应不同的数据   location：0-path,1-query,2-header,3-body
                path和query 用url直接请求
                header和body用request.post(url, headers=headers)或requests.post(url, data)
                '''
                if location == 0:
                    url = url.replace('{' + field_info.field_name + '}', str(value))
                elif location == 1:
                    # url追加key1=value1&key2=value2到url后,即查询字符串
                    if flag == 0:
                        flag = 1
                        url = url + "?" + str(field_info.field_name) + "=" + str(value)
                    else:
                        url = url + "&" + str(field_info.field_name) + "=" + str(value)
                elif location == 2:
                    headers[str(field_info.field_name)] = str(value)
                elif location == 3:
                    # 参数组成json字符串 ==> data
                    data.append(value)
                    pass
            '''Redis存储post过的api_id'''
            post.lpush('api_id_p', post_api.api_id)
            '''配置token'''
            if '?' in url:
                url = url + "&private_token=vE9ggmw9HjEwuisyH2eF"
            else:
                url = url + "?private_token=vE9ggmw9HjEwuisyH2eF"


            print("fuzz " + str(post_api.api_id) + " " + method + " " + url)
            print(headers)

            response = requests.post(url, headers = headers).text
            repon = str(response)
            if len(repon) > 0:
                reponses = json.loads(repon)
                json_txt(reponses)
                if isinstance(reponses, dict):
                    # 如果fuzz成功，将fuzz内容保存到fuzz_success连接池中
                    if reponses.keys() != 'error' and reponses.keys() != 'message':
                        fuzz_success.lpush(str(field_info.field_name), str(val))
            else:
                pass
            print(response)


run_fivetimes_post_api(post_api_list)