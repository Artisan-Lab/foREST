import json
import os
import requests
import random
from module import parse
from entity.testUnit import FuzzAndJudgeUnit


class MRTesting:
    url = None
    field_info = None
    responses = []

    def __init__(self, parameter_list, api_info):
        self.parameter_list = parameter_list
        self.api_info = api_info

    def precondition(self):
        if self.api_info.http_method == 'get':
            self.url = self.api_info.path + '?private_token=n19y6WJgSgjyDuFSHMx9'
            if self.api_info.req_field_names:
                for req_parameter in self.api_info.req_param:
                    if req_parameter.field_name in self.api_info.req_field_names:
                        parameter = str(self.parameter_list[req_parameter.field_name])
                        if req_parameter.location == 0:
                            self.url = self.url.replace('{'+req_parameter.field_name+'}', parameter)
                        else:
                            self.url = self.url + '&' + parameter
            source_response = requests.get(self.url)
            if source_response.status_code > 300:
                print(self.url + 'dependency default')
                return
            self.responses = [json.loads(requests.get(self.url).text)]

    def get_responses(self):
        for req_parameter in api_info.req_param:
            # 测API的每个参数
            if req_parameter.field_name in api_info.req_field_names:
                continue
            for i in range(1, 11):
                for j in range(1, 10):
                    test_unit = FuzzAndJudgeUnit(req_parameter, url, api_info.req_field_names)
                    test_unit.fuzz_parameter()
                    test_unit.add_parameter()
                    if test_unit.judge_effective() == 1:
                        response = test_unit.get_response()
                        self.responses.append(json.loads(response.text))
                        break
            if len(self.responses) < 10:
                print('lack %s' % req_parameter.field_name)
                continue

    def MR_testing(self, response_text, response_text1, response_text2, MR_matrix):
        # MR_matrix 的 含义分别为 subset  equality equivalence disjoint complete diffirence
        response_text3 = response_text1 + response_text2
        if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) or \
                all([response_text1[i] in response_text for i in range(0, len(response_text1))])):
            # judge subset
            MR_matrix[0] = MR_matrix[0] + 1
        if response_text == response_text1:
            MR_matrix[1] = MR_matrix[1] + 1
        if (all([response_text[i] in response_text1 for i in range(0,len(response_text))]) and
                all([response_text1[i] in response_text for i in range(0,len(response_text1))])) and \
                response_text1 != response_text:
            MR_matrix[2] = MR_matrix[2] + 1
        if (all([response_text2[i] not in response_text1 for i in range(0,len(response_text2))]) and
                all([response_text1[i] not in response_text2 for i in range(0,len(response_text1))])):
            MR_matrix[3] = MR_matrix[3] + 1
        if (all([response_text[i] in response_text3 for i in range(0,len(response_text))]) and
                all([response_text3[i] in response_text for i in range(0,len(response_text3))])) and \
                response_text1 != response_text2:
            MR_matrix[4] = MR_matrix[4] + 1
        return MR_matrix

    def exec(self):
        if api_info.http_method == 'get':
            MR_dic = {}
            MR_matrix_count = [0, 0, 0, 0, 0, 0]
            # 前三个为源输出与加参数输出之间的关系 subset equality equivalence
            # 不同参数输出之间的关系 disjoint
            # 不同参数输出与源输出之间的关系 complete
            # 多次相同请求之间的关系difference
            MR_matrix = [0, 0, 0, 0, 0, 0]
            # 记录测得的MR
            for i in range(1, 11):
                response_text = responses[0]
                response_text1 = random.choice(responses[1:11])
                response_text2 = random.choice(responses[1:11])
                for i in range(10):
                    if response_text1 == response_text2:
                        response_text2 = random.choice(responses[1:11])
                MR_matrix_count = MR_testing(response_text, response_text1, response_text2, MR_matrix_count)
            if MR_matrix_count[0] == max(MR_matrix_count): #and MR_matrix_count[1] + MR_matrix_count[2] <MR_matrix_count[0]:
                MR_matrix[0] = 1
            if MR_matrix_count[1] == max(MR_matrix_count):
                MR_matrix[1] = 1
            if MR_matrix_count[1] + MR_matrix_count[2] == MR_matrix_count[0] and MR_matrix_count[1] != 0 and MR_matrix_count[2] !=0:
                MR_matrix[2] = 1
            if MR_matrix_count[3] == max(MR_matrix_count):
                MR_matrix[3] = 1
            if MR_matrix_count[4] == 10 and MR_matrix_count[2] != 1:
                MR_matrix[4] = 1
            MR_dic[str(req_parameter.field_name)] = MR_matrix
            print(str(MR_dic))


path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    Pretreatment(api_info, {'user_id': 34})





