import requests
from entity.testUnit import FuzzAndJudgeUnit


class MetamorphicTesting:

    def __init__(self, base_url, api_info, mr_dic):
        self.base_url = base_url
        self.api_info = api_info
        self.mr_dic = mr_dic

    def find_field_info(self,parameter):
        for field_info in self.api_info.req_param:
            if field_info.field_name == parameter:
                return field_info

    def sub_sub_test(self, parameter_1, parameter_2):
        for i in range(1,10):
            fuzz_unit_1 = FuzzAndJudgeUnit(self.base_url, self.find_field_info(parameter_1))
            fuzz_unit_1.fuzz_and_add_parameter()
            if fuzz_unit_1.judge_effective():
                url_1 = fuzz_unit_1.base_url
                response_1 = requests.get(url_1)
                break
        for i in range(1,10)
        url_1 = self.base_url + '&' + parameter_1
        url_1_response = requests.get(url_1)
        url_test = self.base_url + '&' + deparameter_1 + '&' + parameter_2

    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                if parameter_1[0] == 1 and parameter_2[0] == 1:
                    MetamorphicJudge.sub_sub_test(parameter_1, parameter_2)






