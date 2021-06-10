
class response_parse:

    def json_txt(self, params_pool, dic_json):
        if isinstance(dic_json, list):
            for dic in dic_json:
                if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                    for key in dic:
                        if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                            response_parse().json_txt(params_pool, dic[key])
                            params_pool.lpush(str(key), str(dic[key]))
                        else:
                            params_pool.lpush(str(key), str(dic[key]))
        else:
            if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic_json:
                    if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                        response_parse().json_txt(params_pool, dic_json[key])
                        params_pool.lpush(str(key), str(dic_json[key]))
                    else:
                        params_pool.lpush(str(key), str(dic_json[key]))