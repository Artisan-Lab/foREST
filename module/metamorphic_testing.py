import requests
from entity.fuzz_and_judge import FuzzAndJudgeUnit
import json
from module.metamorphic_compare import MetamorphicCompare
from module.fuzz_MR_parameter import FuzzMRParameter

class MetamorphicTesting:

    problem_url = None
    parameter_1_field = None
    parameter_2_field = None

    def __init__(self, base_url, api_info, mr_dic):
        self.base_url = base_url
        self.api_info = api_info
        self.mr_dic = mr_dic
        self.source_response = json.loads(requests.get(self.base_url).text)
        self.fuzz_unit_1 = None

    def find_field_info(self, parameter_1, parameter_2):
        for field_info in self.api_info.req_param:
            if field_info.field_name == parameter_1:
                self.parameter_1_field = field_info
            if field_info.field_name == parameter_2:
                self.parameter_2_field = field_info

    def sub_sub_test(self):
        # 先得到第一个参数满足subset的参数
        fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
        if fuzz.fuzz_state == 0:
            return
        fuzz_unit_1 = fuzz.get_sub_unit()
        # 再得到第二个参数满足subset的值
        fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
        if fuzz.fuzz_state == 0:
            return
        fuzz_unit_2 = fuzz.get_sub_unit()
        # 将这两个参数组成新的url
        fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
        fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
        fuzz_unit_3.judge_effective()
        if fuzz_unit_3.responses_status == 0:
            return
        # 比较新的url是否满足subset
        compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3.request_response)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + 'subset')
            return
        print('%s  %s  %s  satisfy sub_sub'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def sub_equivalence_test(self):
        # 得到一个满足subset 的参数
        fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
        if fuzz.fuzz_state == 0:
            return
        fuzz_unit_1 = fuzz.get_sub_unit()
        # 得到一个满足equivalence 的参数
        fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
        if fuzz.fuzz_state == 0:
            return
        fuzz_unit_2 = fuzz.get_equivalence_unit()
        # 将这个两个参数得到一个新的url
        fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
        fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
        fuzz_unit_3.judge_effective()
        if fuzz_unit_3.responses_status == 0:
            return
        # 比较该响应是否满足与第一个响应是否满足equivalence
        compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
        compare_unit_3.equivalence_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '    equivalence')
            return
        # 比较该相应与源响应是否满足subset
        compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3.request_response)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(self.base_url + '\n' + fuzz_unit_3.new_url + '    subset')
            return
        # 比较该响应与第二个响应是否满足subset
        compare_unit_3 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_3.request_response)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_2.new_url + '\n' + fuzz_unit_3 + '    subset')
            return
        print('%s  %s  %s  satisfy sub_sort'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def sub_disjoint_testing(self):
        # 得到满足一个subset的参数
        fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
        if fuzz.fuzz_state == 0:
            return
        fuzz_unit_1 = fuzz.get_sub_unit()

    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][0] == 1:
                    self.find_field_info(parameter_1, parameter_2)
                    self.sub_sub_test()
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][2] == 1:
                    self.find_field_info(parameter_1, parameter_2)
                    self.sub_equivalence_test()






