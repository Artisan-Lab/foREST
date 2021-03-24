from prance import ResolvingParser
from entity.api_info import api_info
from entity.field_info import field_info
import os.path



def parameter_handle(parameter_list, req_param_list):
    for parameter in parameter_list:
        parameter_name = parameter['name']
        parameter_type = parameter['schema']['type']
        if 'description' in parameter:
            parameter_description = parameter['description']
        else:
            parameter_description = None
        if 'default' in parameter['schema']:
            parameter_default = parameter['schema']['default']
        else:
            parameter_default = None
        if 'enum' in parameter['schema']:
            parameter_enum = parameter['schema']['enum']
        else:
            parameter_enum = None
        if parameter['in'] == 'path':
            parameter_location = 0
        else:
            parameter_location = 1
        if 'required' in parameter:
            parameter_required = parameter['required']
        else:
            parameter_required = False
        req_param = field_info(parameter_name, parameter_type, parameter_required, parameter_default,
                               "No", parameter_location, parameter_description, parameter_enum)
        req_param_list.append(req_param)
    return req_param_list


def response_handle(methods, method):
    responses = methods.get(method).get("responses")
    resp_params_list = []
    if 'content' in responses['200']:
        properties = responses['200']['content']['application/json']['schema']['properties']
    else:
        return resp_params_list
    for property in properties:
        response_name = property
        if 'type' in properties[response_name]:
            response_type = properties[response_name]['type']
        else:
            response_type = None
        if 'description' in properties[response_name]:
            response_description = properties[response_name]['description']
        else:
            response_description = None
        response_property = field_info(response_name, response_type, None, None, None, None,response_description,None)
        resp_params_list.append(response_property)
    return resp_params_list


def requestBody_handle(requestBody, resp_params_list):
    required_list = []
    properties = requestBody['content']['application/json']['schema']['properties']
    if 'required' in requestBody['content']['application/json']['schema']:
        required_list = requestBody['content']['application/json']['schema']['required']
    for property in properties:
        if property in required_list:
            request_required = True
        else:
            request_required = False
        if 'default' in properties[property]:
            request_default = properties[property]['default']
        else:
            request_default = None
        if 'enum' in properties[property]:
            request_enum = properties[property]['enum']
        else:
            request_enum = None
        if 'description' in properties[property]:
            request_description = properties[property]['description']
        else:
            request_description = None
        if 'type' in properties[property]:
            request_type = properties[property]['type']
        else:
            request_type = None
        request_property = field_info(property, request_type,request_required, request_default,
                                           None, 3, request_description, request_enum)
        resp_params_list.append(request_property)
    return resp_params_list


def parse(version):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/wordpress.yaml")
    parser = ResolvingParser(path)
    spec = parser.specification
    servers = spec.get("servers")
    api_id = 0
    api_list = []
    for server in servers:
        url = server.get("url")
        url = url.replace('https','http')
        paths = spec.get("paths")
        for api_path in paths:
            methods = paths.get(api_path)
            for method in methods:
                api_id = api_id + 1
                complete_api_path = url + api_path
                params = methods.get(method).get("parameters")
                requestBody = methods.get(method).get("requestBody")
                req_param_list = []
                if params:
                    req_param_list = parameter_handle(params, req_param_list)
                if requestBody:
                    req_param_list = requestBody_handle(requestBody, req_param_list)
                resp_param_list = response_handle(methods,method)
                api = api_info(api_id, complete_api_path, req_param_list, resp_param_list, method)
                api_list.append(api)
    return api_list
    pass


dictionary = {
    79: {"id + sha +responses", "short_id + sha + responses"},
    80: {"id + sha +responses", "short_id + sha + responses"},
    81: {"id + sha +responses", "short_id + sha + responses"},
    83: {"id + sha +responses", "short_id + sha + responses"},
    84: {"id + sha +responses", "short_id + sha + responses"},
    88: {"id + sha +responses"},
    624: {"id + group_id + responses", "name + group_name + responses"},
    625: {"name + group_name + responses", "name + group_name + parameters"},
    626: {"id + group_id + responses", "name + group_name + responses"},
    627: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
    628: {"id + group_id + parameters", "id + group_id + responses"},
    629: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
    630: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
    631: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + parameters", "name + group_name + responses"},
    632: {"id + group_id + parameters"},
    633: {"id + group_id + parameters", "id + group_id + responses"},
    634: {"id + group_id + parameters"},
    635: {"id + group_id + parameters"},
    636: {"id + group_id + parameters", "id + group_id + responses"},
    637: {"id + group_id + parameters"},
    638: {"id + group_id + parameters"},
    639: {"id + group_id + parameters"},
    640: {"id + group_id + parameters"},
    641: {"id + group_id + parameters"},
    642: {"id + group_id + parameters"},
    643: {"id + group_id + parameters"},
    644: {"id + group_id + parameters"},
    645: {"id + group_id + parameters"},
    646: {"id + group_id + parameters"},
    647: {"id + group_id + parameters", "id + group_id + responses"},
    648: {"id + group_id + parameters", "id + group_id + responses"},
    649: {"id + group_id + parameters", "id + group_id + responses"},
    640: {"id + group_id + parameters"},
}
