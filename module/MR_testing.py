import json
import os
import requests
import random
from module import parse
from entity.fuzz_and_judge import FuzzAndJudgeUnit
from module.metamorphic_compare import MetamorphicCompare
from module.metamorphic_testing import MetamorphicTesting


class MRTesting:
    url = None
    field_info = None
    url_status = 1
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
                            self.url = self.url.replace('{' + req_parameter.field_name + '}', parameter)
                        else:
                            self.url = self.url + '&' + parameter
            source_response = requests.get(self.url)
            if source_response.status_code > 300:
                print(self.url + 'dependency default')
                self.url_status = 0

    def get_responses(self):
        # 测API的每个参数
        if self.field_info.field_name in self.api_info.req_field_names:
            return
        self.responses = [json.loads(requests.get(self.url).text)]
        for i in range(1, 11):
            for j in range(1, 10):
                test_unit = FuzzAndJudgeUnit(self.field_info, self.url)
                test_unit.req_field_names = self.api_info.req_field_names
                test_unit.fuzz_and_add_parameter()
                if test_unit.judge_effective():
                    response = test_unit.request_response
                    self.responses.append(response)
                    break
        if self.field_info.default:
            test_unit = FuzzAndJudgeUnit(self.field_info,self.url)
            test_unit.parameter = self.field_info.default
            if test_unit.field_info.location == 0:
                test_unit.new_url = test_unit.base_url.replace('{' + test_unit.field_info.field_name + '}', test_unit.parameter)
            else:
                test_unit.new_url = test_unit.base_url + '&' + test_unit.parameter
            if test_unit.judge_effective():
                self.responses.append(test_unit.request_response)
            else:
                print('%s can\'t get response' % test_unit.new_url)

    def MR_testing(self):
        # MR_matrix_count 的 含义分别为 subset  equality equivalence disjoint complete diffirence
        MR_matrix_count = [0, 0, 0, 0, 0, 0]
        for i in range(1, 11):
            response_text = self.responses[0]
            response_text1 = random.choice(self.responses[1:11])
            response_text2 = random.choice(self.responses[1:11])
            for i in range(10):
                if response_text1 == response_text2:
                    response_text2 = random.choice(self.responses[1:11])
            response_text3 = response_text1 + response_text2
            if (all([response_text[i] in response_text1 for i in range(0, len(response_text))]) or
                    all([response_text1[i] in response_text for i in range(0, len(response_text1))])):
                # judge subset
                MR_matrix_count[0] = MR_matrix_count[0] + 1
            if response_text == response_text1:
                MR_matrix_count[1] = MR_matrix_count[1] + 1
            if (all([response_text[i] in response_text1 for i in range(0, len(response_text))]) and
                all([response_text1[i] in response_text for i in range(0, len(response_text1))])) and \
                    response_text1 != response_text:
                MR_matrix_count[2] = MR_matrix_count[2] + 1
            if (all([response_text2[i] not in response_text1 for i in range(0, len(response_text2))]) and
                    all([response_text1[i] not in response_text2 for i in range(0, len(response_text1))])):
                MR_matrix_count[3] = MR_matrix_count[3] + 1
            if (all([response_text[i] in response_text3 for i in range(0, len(response_text))]) and
                all([response_text3[i] in response_text for i in range(0, len(response_text3))])) and \
                    response_text1 != response_text2:
                MR_matrix_count[4] = MR_matrix_count[4] + 1
        return MR_matrix_count

    def exec(self):
        if api_info.http_method == 'get':
            self.precondition()
            if self.url_status:
                MR_dic = {}
                for self.field_info in self.api_info.req_param:
                    self.get_responses()
                    if len(self.responses) < 10:
                        print('fuzz %s fail' % self.field_info.field_name)
                        continue
                    # 前三个为源输出与加参数输出之间的关系 subset equality equivalence
                    # 不同参数输出之间的关系 disjoint
                    # 不同参数输出与源输出之间的关系 complete
                    # 多次相同请求之间的关系difference
                    MR_matrix = [0, 0, 0, 0, 0, 0]
                    # 记录测得的MR
                    MR_matrix_count = self.MR_testing()
                    if MR_matrix_count[0] == 10:  # and MR_matrix_count[1] + MR_matrix_count[2] <MR_matrix_count[0]:
                        MR_matrix[0] = 1
                    if MR_matrix_count[1] == 10:
                        MR_matrix[1] = 1
                    if MR_matrix_count[1] + MR_matrix_count[2] == MR_matrix_count[0] and MR_matrix_count[1] != 0 and \
                            MR_matrix_count[2] != 0:
                        MR_matrix[2] = 1
                    if MR_matrix_count[3] == max(MR_matrix_count):
                        MR_matrix[3] = 1
                    if MR_matrix_count[4] == 10 and MR_matrix_count[2] != 1:
                        MR_matrix[4] = 1
                    MR_dic[str(self.field_info.field_name)] = MR_matrix
                    print(self.field_info.field_name + '     ' + str(MR_matrix_count))
                for key, value in MR_dic.items():
                    print(key + ": " + str(value))
                b = MetamorphicTesting(self.url, self.api_info, MR_dic)
                b.metamorphic_testing()


path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/projects-api.yaml")
api_list = parse.get_api_info(1, path)
for api_info in api_list:
    a = MRTesting({'user_id': 34}, api_info)
    a.exec()