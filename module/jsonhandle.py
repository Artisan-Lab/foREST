import json


class JsonHandle:


    @staticmethod
    def dic2json(api_parameters_dic):
        return json.dumps(api_parameters_dic)

    @staticmethod
    def json2dic(json_string):
        return json.loads(json_string)

    @staticmethod
    def json_judge(dic):
        try:
            json_file = json.loads(dic)
            return True
        except:
            return False

    @staticmethod
    def find_field_in_dic(dic, field_info):
        if isinstance(dic, dict):
            for key in dic:
                if key == field_info.field_type and (isinstance(dic[key], int) and field_info.field_type == 'integer' or
                                                     isinstance(dic[key], str) and field_info.field_type == 'string' or
                                                     isinstance(dic[key], list) and field_info.field_type == 'array' or
                                                     isinstance(dic[key], dict) and field_info.field_type == 'object' or
                                                     isinstance(dic[key], bool) and field_info.field_type == 'boolean'):
                    value = dic[key]
                    return value
                else:
                    value = JsonHandle.find_field_in_dic(dic[key], field_info)
                    if value:
                        return value
        elif isinstance(dic, list):
            if (dic is not None) and (len(dic) > 0) and isinstance(dic[0], dict):
                for sub_dic in dic:
                    value = JsonHandle.find_field_in_dic(sub_dic, field_info)
                    if value:
                        return value
        return None

