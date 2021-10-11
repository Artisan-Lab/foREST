class TestCaseGeneration:

    def __init__(self, api_info, ):
        self.api_info = api_info



    def test_case_generation(self):
        parameter_list = self.api_info.req_param
        for parameter in parameter_list:

