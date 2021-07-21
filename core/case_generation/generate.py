import json
import random
import urllib

from fuzz_from_data.mutationAPI import *
from module.Combination import Combination
from module.type_fuzz import fuzz
from module.object_handle import fuzz_object
from fuzz_from_data.commons.utils import *



class case_generation():

    def fuzz_generation(self, api_info, fuzz_pool, params_pool):
        id = api_info.api_id
        path = api_info.path
        method = api_info.http_method
        result = Mutation_API.get_matched_request(path + "," + method.upper())
        query_string = urllib.parse.urlparse(result.url).query
        url_dict = {}
        body_dict = {}
        if query_string:
            url_dict = {x[0]: x[1] for x in [x.split("=") for x in query_string.split("&")]}
        header_dict = result.headers
        if len(result.body) > 0:
            body_dict = json.loads(result.body)
        result_dict = {}
        if len(url_dict) > 0:
            result_dict.update(url_dict)
        if header_dict:
            result_dict.update(header_dict)
        if Utils.is_json(body_dict) and len(body_dict) > 0:
            if isinstance(body_dict, dict):
                result_dict.update(body_dict)
            elif isinstance(body_dict, list):
                for temp in body_dict:
                    if isinstance(temp, dict):
                        result_dict.update(temp)
                    else:
                        pass
        parameter = {}
        for field_info in api_info.req_param:
            if field_info.require:
                if field_info.field_type == 'string' or field_info.field_type == 'integer' \
                        or field_info.field_type == 'boolean':
                    if field_info.field_name in result_dict:
                        value = result_dict[field_info.field_name]
                    elif params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        value = fuzz(field_info.field_type)
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                elif field_info.field_type == 'object' and field_info.object is not None:
                    if field_info.field_name in result_dict:
                        value = result_dict[field_info.field_name]
                    elif params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        if field_info.object:
                            dic = fuzz_object().object_handle(field_info.object)
                            value = json.dumps(dic)
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                else:
                    if field_info.field_name in result_dict:
                        value = result_dict[field_info.field_name]
                    elif params_pool.llen(str(field_info.field_name)) != 0:
                        length = params_pool.llen(str(field_info.field_name))
                        index = random.randint(0, length)
                        value = params_pool.lindex(str(field_info.field_name), index)
                    else:
                        if field_info.array == 'string' or field_info.array == 'integer' \
                                or field_info.array == 'boolean':
                            value = []
                            value.append(fuzz(field_info.array))
                        else:
                            arr_dict = {}
                            for arr in field_info.array:
                                arr_dict[arr.name] = fuzz(arr.type)
                            value = [arr_dict]
                    parameter[str(field_info.field_name)] = str(value) + str(field_info.location)

        fuzz_pool.sadd(str(id), str(parameter))

    def fuzz_optional_generation(self, api_info, fuzz_pool, nums, params_pool):
        id = api_info.api_id
        path = api_info.path
        method = api_info.http_method
        result = Mutation_API.get_matched_request(path + "," + method.upper())
        query_string = urllib.parse.urlparse(result.url).query
        url_dict = {}
        body_dict = {}
        if query_string:
            url_dict = {x[0]: x[1] for x in [x.split("=") for x in query_string.split("&")]}
        header_dict = result.headers
        if len(result.body) > 0:
            body_dict = json.loads(result.body)
        result_dict = {}
        if len(url_dict) > 0:
            result_dict.update(url_dict)
        if header_dict:
            result_dict.update(header_dict)
        if Utils.is_json(body_dict) and len(body_dict) > 0:
            if isinstance(body_dict, dict):
                result_dict.update(body_dict)
            elif isinstance(body_dict, list):
                for temp in body_dict:
                    if isinstance(temp, dict):
                        result_dict.update(temp)
                    else:
                        pass

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
                            if field_info.field_name in result_dict:
                                value = result_dict[field_info.field_name]
                            elif params_pool.llen(str(field_info.field_name)) is not None:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                value = fuzz(field_info.field_type)
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
                        elif field_info.field_type == 'object' and field_info.object is not None:
                            if field_info.field_name in result_dict:
                                value = result_dict[field_info.field_name]
                            elif params_pool.llen(str(field_info.field_name)) != 0:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                dic = fuzz_object().object_handle(field_info.object)
                                value = json.dumps(dic)
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)

                        else:
                            if field_info.field_name in result_dict:
                                value = result_dict[field_info.field_name]
                            elif params_pool.llen(str(field_info.field_name)) != 0:
                                length = params_pool.llen(str(field_info.field_name))
                                index = random.randint(0, length)
                                value = params_pool.lindex(str(field_info.field_name), index)
                            else:
                                if field_info.array == 'string' or field_info.array == 'integer' \
                                        or field_info.array == 'boolean':
                                    value = []
                                    value.append(fuzz(field_info.array))
                                else:
                                    arr_dict = {}
                                    for arr in field_info.array:
                                        arr_dict[arr.name] = fuzz(arr.type)
                                    value = [arr_dict]
                            parameter[str(field_info.field_name)] = str(value) + str(field_info.location)
            fuzz_pool.sadd(str(id) + 'optional', str(parameter))
