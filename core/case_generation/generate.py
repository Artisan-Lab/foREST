import json
import random

from module.Combination import Combination
from module.type_fuzz import fuzz
from module.object_handle import fuzz_object


class case_generation():

    def fuzz_generation(self, api_info, fuzz_pool, params_pool):
        id = api_info.api_id
        parameter = {}
        for field_info in api_info.req_param:
            if field_info.require:
                if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                        or field_info.field_type == 'boolean':
                    if params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        value = fuzz(field_info.field_type)
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                elif field_info.field_type == 'object' and field_info.object is not None:
                    if params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        if field_info.object:
                            dic = fuzz_object().object_handle(field_info.object)
                            value = json.dumps(dic)
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                else:
                    if params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        if field_info.array == 'string' or field_info.array == 'integer' \
                                or field_info.array == 'boolean':
                            value = []
                            value.append(fuzz(field_info.array))
                        else:
                            value = [{"name": "linjiaxian", "type": "human", "age": 18}, {"id": 100, "cloud_id": 2}]
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)

        fuzz_pool.sadd(str(id), str(parameter))

    def fuzz_optional_generation(self, api_info, fuzz_pool, nums, params_pool):
        id = api_info.api_id
        parameters = []
        for field_info in api_info.req_param:
            if not field_info.require:
                parameters.append(field_info.field_name)


        if len(parameters) >= nums:
            optional_params = Combination().combine(parameters, nums)
        else:
            optional_params = Combination().combine(parameters, len(parameters))


        for optional_param in optional_params:
            optional_param = list(optional_param)
            parameter = {}
            for field_info in api_info.req_param:
                if not field_info.require:
                    if optional_param is not None and field_info.field_name in optional_param:
                        if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                                or field_info.field_type == 'boolean':
                            if params_pool.llen(str(field_info.field_name)) is not None:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                value = fuzz(field_info.field_type)
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                        elif field_info.field_type == 'object' and field_info.object is not None:
                            if params_pool.llen(str(field_info.field_name)) != 0:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                dic = fuzz_object().object_handle(field_info.object)
                                value = json.dumps(dic)
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)

                        else:
                            if params_pool.llen(str(field_info.field_name)) != 0:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                if field_info.array == 'string' or field_info.array == 'integer' \
                                        or field_info.array == 'boolean':
                                    value = []
                                    value.append(fuzz(field_info.array))
                                else:
                                    value = [{"name": "linjiaxian", "type": "human", "age": 18},
                                             {"id": 100, "cloud_id": 2}]
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
            fuzz_pool.sadd(str(id) + 'optional', str(parameter))
