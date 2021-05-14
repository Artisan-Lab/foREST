import requests
from metamorphic.fuzz_and_judge import FuzzAndJudgeUnit
import json
from metamorphic.metamorphic_compare import MetamorphicCompare
from metamorphic.fuzz_MR_parameter import FuzzMRParameter


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
        for i in range(10):
            # 先得到第一个参数满足subset的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_sub_unit()
            if fuzz.fuzz_state == 0:
                return
            # 再得到第二个参数满足subset的值
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_sub_unit()
            if fuzz.fuzz_state == 0:
                return
            # 将这两个参数组成新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            # 比较新的url是否满足subset
            compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3.request_response)
            compare_unit_3.subset_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '   not satisfy sub_subset')
                return
        print('%s  %s  %s  satisfy sub_sub'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def sub_equality_test(self):
        for i in range(10):
            # 得到一个满足subset 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_sub_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到一个满足equality 的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_equality_unit()
            if fuzz.fuzz_state == 0:
                return
            # 将这两个参数组合得到一个新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            # 比较该响应与第一个响应是否满足equality
            compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
            compare_unit_3.equality_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_1.new_url + '\n' + fuzz_unit_2.new_url + '    not satisfy sub_equality')
        print('%s  %s  %s  satisfy sub_equality'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))

        return

    def sub_equivalence_test(self):
        for i in range(10):
            # 得到一个满足subset 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_sub_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到一个满足equivalence 的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_equivalence_unit()
            if fuzz.fuzz_state == 0:
                return
            # 将这个两个参数得到一个新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            # 比较该响应与第一个响应是否满足equivalence
            compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
            compare_unit_3.equivalence_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '    not satisfy sub_equivalence')
                return
            # 比较该相应与源响应是否满足subset
            compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3.request_response)
            compare_unit_3.subset_compare()
            if not compare_unit_3.compare_result:
                print(self.base_url + '\n' + fuzz_unit_3.new_url + '    not satisfy subset_equivalence')
                return
            # 比较该响应与第二个响应是否满足subset
            compare_unit_3 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_3.request_response)
            compare_unit_3.subset_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_2.new_url + '\n' + fuzz_unit_3 + '    not satisfy subset_equivalence')
                return
        print('%s  %s  %s  satisfy sub_equivalence'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def sub_disjoint_test(self):
        for i in range(10):
            # 得到满足一个subset的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_sub_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到两个满足disjoint的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_disjoint_unit()
            fuzz_unit_3 = fuzz.fuzz_unit
            if not fuzz.fuzz_state:
                return
            # 将这两个参数得到两个新的url
            fuzz_unit_4 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_4.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_4.judge_effective()
            if fuzz_unit_4.responses_status == 0:
                print(fuzz_unit_4.new_url + ' is invalid')
                return
            fuzz_unit_5 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_5.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_3.parameter
            fuzz_unit_5.judge_effective()
            if fuzz_unit_5.responses_status == 0:
                print(fuzz_unit_5.new_url + ' is invalid')
                return
            compare_unit_1 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_4.request_response)
            compare_unit_1.subset_compare()
            compare_unit_2 = MetamorphicCompare(fuzz_unit_3.request_response, fuzz_unit_5.request_response)
            compare_unit_2.subset_compare()
            if not compare_unit_1.compare_result or compare_unit_2.compare_result:
                print(fuzz_unit_4.new_url + '\n' + fuzz_unit_5.new_url + ' not satisfy sub_disjoint')
                return
        print('%s  %s  %s  satisfy sub_disjoint'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def equality_equality_test(self):
        for i in range(10):
            # 得到一个满足equality 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_equality_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到另一个满足equality的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_equality_unit()
            if fuzz.fuzz_state == 0:
                return
            # 组合成新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
            compare_unit_3.equality_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '    not satisfy equality_equality')
                return
        print('%s  %s  %s  satisfy equality_equality'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def equality_equivalence_test(self):
        for i in range(10):
            # 得到一个满足equality 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_equality_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到一个满足equivalence的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_equivalence_unit()
            if fuzz.fuzz_state == 0:
                return
            # 组合成一个新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
            compare_unit_3.equivalence_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '    not satisfy equality_equivalence')
                return
        print('%s  %s  %s  satisfy equality_equivalence'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def equality_disjoint_test(self):
        for i in range(10):
            # 得到一个满足equality 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_equality_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到两个满足disjoint 的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_disjoint_unit()
            fuzz_unit_3 = fuzz.fuzz_unit
            if not fuzz.fuzz_state:
                return
            # 将这两个参数得到两个新的url
            fuzz_unit_4 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_4.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_4.judge_effective()
            if fuzz_unit_4.responses_status == 0:
                print(fuzz_unit_4.new_url + ' is invalid')
                return
            fuzz_unit_5 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_5.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_3.parameter
            fuzz_unit_5.judge_effective()
            if fuzz_unit_5.responses_status == 0:
                print(fuzz_unit_5.new_url + ' is invalid')
                return
            compare_unit_1 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_4.request_response)
            compare_unit_1.equality_compare()
            compare_unit_2 = MetamorphicCompare(fuzz_unit_3.request_response, fuzz_unit_5.request_response)
            compare_unit_2.equality_compare()
            if not compare_unit_1.compare_result or compare_unit_2.compare_result:
                print(fuzz_unit_4.new_url + '\n' + fuzz_unit_5.new_url + ' not satisfy equality_disjoint')
                return
        print('%s  %s  %s  satisfy equality_disjoint'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def equivalence_equivalence_test(self):
        for i in range(10):
            # 得到一个满足equivalence的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_equivalence_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到一个满足equivalence的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_equivalence_unit()
            if fuzz.fuzz_state == 0:
                return
            # 组合成一个新的url
            fuzz_unit_3 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_3.judge_effective()
            if fuzz_unit_3.responses_status == 0:
                print(fuzz_unit_3.new_url + ' is invalid')
                return
            compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
            compare_unit_3.equivalence_compare()
            if not compare_unit_3.compare_result:
                print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url + '    not satisfy equivalenc_equivalence')
                return
        print('%s  %s  %s  satisfy equivalence_equivalence'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def equivalence_disjoint_test(self):
        for i in range(10):
            # 得到一个满足equivalence的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_equivalence_unit()
            if fuzz.fuzz_state == 0:
                return
            # 得到两个满足disjoint 的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_2 = fuzz.get_disjoint_unit()
            fuzz_unit_3 = fuzz.fuzz_unit
            if not fuzz.fuzz_state:
                return
            # 将这两个参数得到两个新的url
            fuzz_unit_4 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_4.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
            fuzz_unit_4.judge_effective()
            if fuzz_unit_4.responses_status == 0:
                print(fuzz_unit_4.new_url + ' is invalid')
                return
            fuzz_unit_5 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_5.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_3.parameter
            fuzz_unit_5.judge_effective()
            if fuzz_unit_5.responses_status == 0:
                print(fuzz_unit_5.new_url + ' is invalid')
                return
            compare_unit_1 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_4.request_response)
            compare_unit_1.equivalence_compare()
            compare_unit_2 = MetamorphicCompare(fuzz_unit_3.request_response, fuzz_unit_5.request_response)
            compare_unit_2.equivalence_compare()
            if not compare_unit_1.compare_result or compare_unit_2.compare_result:
                print(fuzz_unit_4.new_url + '\n' + fuzz_unit_5.new_url + ' not satisfy equivalence_disjoint')
                return
        print('%s  %s  %s  satisfy equivalence_disjoint'
              % (self.base_url, self.parameter_1_field.field_name, self.parameter_2_field.field_name))
        return

    def disjoint_disjoint_test(self):
        for i in range(10):
            # 得到两个满足disjoint 的参数
            fuzz = FuzzMRParameter(self.parameter_1_field, self.base_url, self.source_response)
            fuzz_unit_1 = fuzz.get_disjoint_unit()
            fuzz_unit_2 = fuzz.fuzz_unit
            if not fuzz.fuzz_state:
                return
            # 得到另外两个满足disjoint 的参数
            fuzz = FuzzMRParameter(self.parameter_2_field, self.base_url, self.source_response)
            fuzz_unit_3 = fuzz.get_disjoint_unit()
            fuzz_unit_4 = fuzz.fuzz_unit
            if not fuzz.fuzz_state:
                return
            fuzz_unit_5 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_5.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_3.parameter
            fuzz_unit_5.judge_effective()
            if fuzz_unit_5.responses_status == 0:
                print(fuzz_unit_5.new_url + ' is invalid')
                return
            fuzz_unit_6 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_6.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_4.parameter
            fuzz_unit_6.judge_effective()
            if fuzz_unit_6.responses_status == 0:
                print(fuzz_unit_6.new_url + ' is invalid')
                return
            fuzz_unit_7 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_7.new_url = fuzz_unit_2.new_url + '&' + fuzz_unit_3.parameter
            fuzz_unit_7.judge_effective()
            if fuzz_unit_7.responses_status == 0:
                print(fuzz_unit_7.new_url + ' is invalid')
                return
            fuzz_unit_8 = FuzzAndJudgeUnit(self.parameter_2_field, fuzz_unit_1.new_url)
            fuzz_unit_8.new_url = fuzz_unit_2.new_url + '&' + fuzz_unit_4.parameter
            fuzz_unit_8.judge_effective()
            if fuzz_unit_8.responses_status == 0:
                print(fuzz_unit_8.new_url + ' is invalid')
                return
            compare_unit_1 = MetamorphicCompare(fuzz_unit_5.request_response, fuzz_unit_6.request_response)
            compare_unit_1.disjoint_compare()
            compare_unit_2 = MetamorphicCompare(fuzz_unit_7.request_response, fuzz_unit_8.request_response)
            compare_unit_2.disjoint_compare()
            compare_unit_3 = MetamorphicCompare(fuzz_unit_5.request_response, fuzz_unit_7.request_response)
            compare_unit_3.disjoint_compare()
            compare_unit_4 = MetamorphicCompare(fuzz_unit_6.request_response, fuzz_unit_8.request_response)
            compare_unit_4.disjoint_compare()
            if not compare_unit_1.compare_result:
                print(fuzz_unit_5.new_url + '\n' + fuzz_unit_6.new_url + ' not satisfy disjoint_disjoint')
                return
            if not compare_unit_2.compare_result:
                print(fuzz_unit_7.new_url + '\n' + fuzz_unit_8.new_url + ' not satisfy disjoint_disjoint')
                return
            if not compare_unit_3.compare_result:
                print(fuzz_unit_5.new_url + '\n' + fuzz_unit_7.new_url + ' not satisfy disjoint_disjoint')
                return
            if not compare_unit_4.compare_result:
                print(fuzz_unit_6.new_url + '\n' + fuzz_unit_8.new_url + ' not satisfy disjoint_disjoint')
                return


    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                self.find_field_info(parameter_1, parameter_2)
                if self.mr_dic[parameter_1][0] == 1:
                    if self.mr_dic[parameter_2][0] == 1:
                        self.sub_sub_test()
                    if self.mr_dic[parameter_2][1]:
                        self.sub_equality_test()
                    if self.mr_dic[parameter_2][2] == 1:
                        self.sub_equivalence_test()
                    if self.mr_dic[parameter_2][3] == 1:
                        self.sub_disjoint_test()
                if self.mr_dic[parameter_1][1] == 1:
                    if self.mr_dic[parameter_2][1] == 1:
                        self.equality_equality_test()
                    if self.mr_dic[parameter_2][2] == 1:
                        self.equality_equivalence_test()
                    if self.mr_dic[parameter_2][3] == 1:
                        self.equality_disjoint_test()
                if self.mr_dic[parameter_1][2] == 1:
                    if self.mr_dic[parameter_2][2] == 1:
                        self.equivalence_equivalence_test()
                    if self.mr_dic[parameter_2][3] == 1:
                        self.equivalence_disjoint_test()
                if self.mr_dic[parameter_1][3] == 1:
                    if self.mr_dic[parameter_2][3] == 1:
                        self.disjoint_disjoint_test()
