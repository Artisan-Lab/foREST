
class response_parse:

    def json_txt(self, params_pool, dic_json):
        if isinstance(dic_json, list):
            for dic in dic_json:
                if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                    for key in dic:
                        if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                            response_parse().json_txt(params_pool, dic[key])
                            if dic[key] is not None:
                                params_pool.lpush(str(key), str(dic[key]))
                        elif isinstance(dic[key], list):
                            response_parse().json_txt(params_pool, dic[key])
                        else:
                            if dic[key] is not None and dic[key] != 0:
                                params_pool.lpush(str(key), str(dic[key]))
                elif isinstance(dic, list):
                    response_parse().json_txt(params_pool, dic)
                else:
                    pass
        else:
            if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic_json:
                    if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                        response_parse().json_txt(params_pool, dic_json[key])
                        if dic_json[key] is not None:
                            params_pool.lpush(str(key), str(dic_json[key]))
                    else:
                        if isinstance(dic_json[key], list):
                            response_parse().json_txt(params_pool, dic_json[key])
                        elif dic_json[key] is not None and dic_json[key] != 0:
                            params_pool.lpush(str(key), str(dic_json[key]))