import requests
from entity.testUnit import FuzzAndJudgeUnit
import json
from module.metamorphic_compare import MetamorphicCompare


class MetamorphicTesting:

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
        fuzz_unit_1.exec()
        if fuzz_unit_1.responses_status == 0:
            return
        compare_unit_1 = MetamorphicCompare(self.source_response, fuzz_unit_1.request_response)
        compare_unit_1.subset_compare()
        if not compare_unit_1.compare_result:
            print(fuzz_unit_1.new_url + 'Does not satisfy subset with source response')
            return
        fuzz_unit_2 = FuzzAndJudgeUnit(self.find_field_info(parameter_2), self.base_url)
        fuzz_unit_2.exec()
        if fuzz_unit_1.responses_status == 0:
            return
        compare_unit_2 = MetamorphicCompare(self.source_response, fuzz_unit_1.request_response)
        compare_unit_2.subset_compare()
        if not compare_unit_2.compare_result:
            print(fuzz_unit_2.new_url + 'Does not satisfy subset with source response')
            return
        fuzz_unit_3 = FuzzAndJudgeUnit(self.find_field_info(parameter_2), fuzz_unit_1.new_url)
        fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
        fuzz_unit_3.judge_effective()
        if fuzz_unit_3.responses_status == 0:
            return
        compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3.request_response)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_3.new_url + '\n' + fuzz_unit_1.new_url)
            return
        return

    def sub_sort_test(self, parameter_1, parameter_2):
        fuzz_unit_1 = FuzzAndJudgeUnit(self.find_field_info(parameter_1), self.base_url)
        fuzz_unit_1.exec()
        if fuzz_unit_1.responses_status == 0:
            return
        compare_unit_1 = MetamorphicCompare(self.source_response, fuzz_unit_1.request_response)
        compare_unit_1.subset_compare()
        if not compare_unit_1.compare_result:
            print(fuzz_unit_1.new_url + 'Does not satisfy subset with source response')
            return
        fuzz_unit_2 = FuzzAndJudgeUnit(self.find_field_info(parameter_2), self.base_url)
        fuzz_unit_2.exec()
        if fuzz_unit_1.responses_status == 0:
            return
        compare_unit_2 = MetamorphicCompare(self.source_response, fuzz_unit_1.request_response)
        compare_unit_2.equivalence_compare()
        if not compare_unit_2.compare_result:
            print(fuzz_unit_2.new_url + 'Does not satisfy subset with source response')
            return
        fuzz_unit_3 = FuzzAndJudgeUnit(self.find_field_info(parameter_2), fuzz_unit_1.new_url)
        fuzz_unit_3.new_url = fuzz_unit_1.new_url + '&' + fuzz_unit_2.parameter
        fuzz_unit_3.judge_effective()
        if fuzz_unit_3.responses_status == 0:
            return
        compare_unit_3 = MetamorphicCompare(fuzz_unit_1.request_response, fuzz_unit_3.request_response)
        compare_unit_3.equivalence_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_3.new_url + fuzz_unit_1.new_url + 'equivalence')
            return
        compare_unit_3 = MetamorphicCompare(self.source_response, fuzz_unit_3)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(self.base_url + fuzz_unit_3.new_url + 'subset')
            return
        compare_unit_3 = MetamorphicCompare(fuzz_unit_2.request_response, fuzz_unit_3.request_response)
        compare_unit_3.subset_compare()
        if not compare_unit_3.compare_result:
            print(fuzz_unit_2.new_url + fuzz_unit_3 + 'subset')

        return

    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][0] == 1:
                    self.sub_sub_test(parameter_1, parameter_2)
                if self.mr_dic[parameter_1][0] == 1 and self.mr_dic[parameter_2][2] == 1:
                    self.sub_sort_test(parameter_1, parameter_2)






