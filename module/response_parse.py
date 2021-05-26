
class response_parse:

    def json_txt(self, matr, tag, dic_json):
        if isinstance(dic_json, list):
            for dic in dic_json:
                if isinstance(dic, dict):  # 判断是否是字典类型isinstance 返回True false
                    for key in dic:
                        if isinstance(dic[key], dict):  # 如果dic_json[key]依旧是字典类型
                            response_parse().json_txt(matr, tag, dic[key])
                            matr.lpush(str(key) + tag, str(dic[key]))
                        else:
                            matr.lpush(str(key) + tag, str(dic[key]))
        else:
            if isinstance(dic_json, dict):  # 判断是否是字典类型isinstance 返回True false
                for key in dic_json:
                    if isinstance(dic_json[key], dict):  # 如果dic_json[key]依旧是字典类型
                        response_parse().json_txt(matr, tag, dic_json[key])
                        matr.lpush(str(key) + tag, str(dic_json[key]))
                    else:
                        matr.lpush(str(key) + tag, str(dic_json[key]))