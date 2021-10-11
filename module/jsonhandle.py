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
            json_file = dic.json()
            return True
        except:
            return False

