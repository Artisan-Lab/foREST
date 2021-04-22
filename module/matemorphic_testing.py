import requests
from entity.testUnit import FuzzAndJudgeUnit
import json
from module.metamorphic_compare import MetamorphicCompare


class MetamorphicTesting:

    sorce_response = None
    problem_url = None

    def __init__(self, base_url, api_info, mr_dic):
        self.base_url = base_url
        self.api_info = api_info
        self.mr_dic = mr_dic
        self.source_response = json.loads(requests.get(self.base_url).text)

    def find_field_info(self,parameter):
        for field_info in self.api_info.req_param:
            if field_info.field_name == parameter:
                return field_info

    def sub_sub_test(self, parameter_1, parameter_2):
        fuzz_unit_1 = FuzzAndJudgeUnit(self.find_field_info(parameter_1), self.base_url)
        for i in range(1, 10):
            fuzz_unit_1.fuzz_and_add_parameter()
            if fuzz_unit_1.judge_effective():
                response_1 = json.loads(requests.get(fuzz_unit_1.new_url).text)
                break
        if not fuzz_unit_1.judge_effective():
            print(fuzz_unit_1.base_url + '  ' + fuzz_unit_1.field_info.field_name + 'may has problem')
            return 0
        compare_unit_1 = MetamorphicCompare(self.source_response, response_1)
        compare_unit_1.subset_compare()
        if not compare_unit_1.compare_result:
            print(fuzz_unit_1.new_url + '\n' + self.source_response)
            return 0
        fuzz_unit_2 = FuzzAndJudgeUnit(self.find_field_info(parameter_2), fuzz_unit_1.new_url)
        for i in range(1, 10):
            fuzz_unit_2.fuzz_and_add_parameter()
            if fuzz_unit_2.judge_effective():
                response_2 = json.loads(requests.get(fuzz_unit_2.new_url).text)
                break
        if not fuzz_unit_2.judge_effective():
            print(fuzz_unit_2.base_url + '  ' + fuzz_unit_1.field_info.field_name +
                  fuzz_unit_2.field_info.field_name + 'may has problem')
            return 0
        compare_unit_2 = MetamorphicCompare(self.source_response, response_2)
        compare_unit_2.subset_compare()
        if not compare_unit_2.compare_result:
            print(fuzz_unit_2.new_url + '\n' + fuzz_unit_1.new_url)
            return 0
        return 1

    def sub_sort_test(self, parameter_1, parameter_2):


    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][0] == 1:
                    self.sub_sub_test(parameter_1, parameter_2)
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][2] == 1:
                    self.sub_sort_test(parameter_1, parameter_2)






