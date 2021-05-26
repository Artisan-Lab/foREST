
from module.Combination import Combination
from module.type_fuzz import fuzz


class case_generation():

    def fuzz_generation(self,api_info,fuzz_pool):
        id = api_info.api_id
        parameter = {}
        for field_info in api_info.req_param:
            if field_info.require:
                if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                        or field_info.field_type == 'boolean':
                    value = fuzz(field_info.field_type)
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
        fuzz_pool.sadd(str(id),str(parameter))

    def fuzz_optional_generation(self, api_info, fuzz_pool, nums):
        id = api_info.api_id
        parameters = []
        for field_info in api_info.req_param:
            if not field_info.require:
                if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                        or field_info.field_type == 'boolean':
                    parameters.append(field_info.field_name)
        if len(parameters) >= nums:
            optional_params = Combination().get_combine(parameters, nums)
        else:
            optional_params = Combination().get_combine(parameters, len(parameters))


        for optional_param in optional_params:
            optional_param = list(optional_param)
            parameter = {}
            for field_info in api_info.req_param:
                if not field_info.require:
                    if optional_param != None and field_info.field_name in optional_param:
                        value = fuzz(field_info.field_type)
                        parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                        fuzz_pool.sadd(str(id) + 'optional', str(parameter))


