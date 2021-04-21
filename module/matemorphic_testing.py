import requests

from module.MR_testing import fuzz_parameter


class MetamorphicJudge:

    def __init__(self,base_url, api_info, mr_dic):
        self.base_url = base_url
        self.api_info = api_info
        self.mr_dic = mr_dic

    def sub_sub_test(self,parameter_1, parameter_2):
        parameter_1 = fuzz_parameter(parameter_1)
        parameter_2 = fuzz_parameter(parameter_2)
        url_1 = self.base_url + '&' + parameter_1
        url_1_response = requests.get(url_1)
        url_test = self.base_url + '&' + parameter_1 + '&'

    def metamorphic_testing(self):
        for parameter_1 in self.mr_dic:
            for parameter_2 in self.mr_dic:
                if parameter_1[0] == 1 and parameter_2[0] == 1:
                    MetamorphicJudge.sub_sub_test(parameter_1,parameter_2)






