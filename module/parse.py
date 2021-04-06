from prance import ResolvingParser
from entity.api_info import api_info
from entity.field_info import field_info
from entity.object_info import object_info
import os.path


def array_handle(items):
    if 'type' in items:
        type = items['type']
    else:
        type = 'object'
    if 'properties' in items:
        return object_handle(items['properties'])
    elif type == 'array':
        return array_handle(items['items'])
    else:
        return items['type']

def object_handle(objects):
    object_list = []
    for object in objects:
        if 'type' in objects[object]:
            type = objects[object]['type']
        else:
            type = 'object'
        if type == 'object':
            if 'properties' in objects[object]:
                object_feild = object_info(object,type,object_handle(objects[object]['properties']))
            else:
                object_feild = object_info(object,type,None)
        elif type == 'array':
            object_feild = object_info(object,type,array_handle(objects[object]['items']))
        else:
            object_feild = object_info(object,type,None)
        object_list.append(object_feild)
    return object_list


def properties_handle(properties,required_list,properties_list):
    if required_list == None and properties_list == None:
        required_list = []
        properties_list = []
    for property in properties:
        if property in required_list:
            request_required = true
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
        if request_type == 'object' and 'properties' in properties[property]:
            object_list = object_handle(properties[property]['properties'])
            array_type = None
        elif request_type == 'array' and 'items' in properties[property]:
            array_type = array_handle(properties[property]['items'])
            object_list = None
        else:
            object_list = None
            array_type = None
        if 'maxLength' in properties[property]:
            max = properties[property]['maxLength']
        else:
            max = None
        if 'minLength' in properties[property]:
            min = properties[property]['minLength']
        else:
            min = None
        request_property = field_info(property, request_type, request_required, request_default,
                                      None, 3, request_description, request_enum,object_list,array_type,max,min)
        properties_list.append(request_property)
    return properties_list


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
        if 'maxLength' in parameter['schema']:
            max = parameter['schema']['maxLength']
        else:
            max = None
        if 'minLength' in parameter['schema']:
            min = parameter['schema']['minLength']
        else:
            min = None
        if parameter['in'] == 'path':
            parameter_location = 0
        elif parameter['in'] == 'query':
            parameter_location = 1
        elif parameter['in'] == 'header':
            parameter_location = 2
        elif parameter['in'] == 'body':
            parameter_location = 3
        if 'required' in parameter:
            parameter_required = parameter['required']
        else:
            parameter_required = False
        if parameter_type == 'array':
            array_type = array_handle(parameter['schema']['items'])
        else:
            array_type = None
        req_param = field_info(parameter_name, parameter_type, parameter_required, parameter_default,
                               "No", parameter_location, parameter_description, parameter_enum,None,array_type,max,min)
        req_param_list.append(req_param)
    return req_param_list


def parameter_swagger_handle(parameter_list,req_param_list):
    for parameter in parameter_list:
        parameter_name = parameter['name']
        if 'type' in parameter:
            parameter_type = parameter['type']
        else:
            if 'type' in parameter['schema']:
                parameter_type = parameter['schema']['type']
            else:
                parameter_type = 'object'
        if 'description' in parameter:
            parameter_description = parameter['description']
        else:
            parameter_description = None
        if 'default' in parameter:
            parameter_default = parameter['default']
        else:
            parameter_default = None
        if 'enum' in parameter:
            parameter_enum = parameter['enum']
        else:
            parameter_enum = None
        if parameter['in'] == 'path':
            parameter_location = 0
        elif parameter['in'] == 'query':
            parameter_location = 1
        elif parameter['in'] == 'header':
            parameter_location = 2
        elif parameter['in'] == 'body':
            parameter_location = 3
        else:
            parameter_location = 5
        if 'required' in parameter:
            parameter_required = parameter['required']
        else:
            parameter_required = False
        if parameter_type == 'array':
            if 'items' in parameter:
                array_type = array_handle(parameter['schema']['items'])
            else:
                array_type = None
        else:
            array_type = None
        if parameter_type == 'object':
            object_type = object_handle(parameter['schema']['properties'])
        else:
            object_type = None
        if 'maxLength' in parameter:
            max = parameter['maxLength']
        else:
            max = None
        if 'minLength' in parameter:
            min = parameter['minLength']
        else:
            min = None
        req_param = field_info(parameter_name, parameter_type, parameter_required, parameter_default,
                               "No", parameter_location, parameter_description, parameter_enum, object_type, array_type, max,
                               min)
        req_param_list.append(req_param)
    return req_param_list


def response_swagger_handle(responses):
    resp_params_list = []
    for response in responses:
        if 'schema' in responses[response]:
            if 'properties' in responses[response]['schema']:
                    properties = responses[response]['schema']['properties']
                    resp_params_list = properties_handle(properties,None,None)
            elif 'array' == responses[response]['schema']['type']:
                items = responses[response]['schema']['items']
                resp_params_list = array_handle(items)
        return resp_params_list


def response_handle(responses):
    resp_params_list = []
    for response in responses:
        if 'content' in responses[response]:
            for key in responses[response]['content']:
                properties_alls = key
            properties = responses[response]['content'][properties_alls]['schema']['properties']
        else:
            return resp_params_list
        resp_params_list = properties_handle(properties,None,None)
        return resp_params_list


def requestBody_handle(requestBody, req_params_list):
    required_list = []
    for key in requestBody['content'].keys():
        properties_alls = key
    if 'type' not in requestBody['content'][properties_alls]['schema']:
        properties = requestBody['content'][properties_alls]['schema']['properties']
    elif requestBody['content'][properties_alls]['schema']['type'] == 'object':
        properties = requestBody['content'][properties_alls]['schema']['properties']
    elif requestBody['content'][properties_alls]['schema']['type'] == 'array':
        properties = requestBody['content'][properties_alls]['schema']['items']
    if 'required' in requestBody['content'][properties_alls]['schema']:
        required_list = requestBody['content'][properties_alls]['schema']['required']
    return properties_handle(properties, required_list,req_params_list)


def swagger_handle(spec):
    url = spec.get('host') + spec.get('basePath')
    return url


def open_api_handle(spec):
    servers = spec.get('servers')
    for server in servers:
        url = server.get('url').replace('https','http')
    return url


def paths_handle(spec):
    if 'swagger' in spec:
        url = swagger_handle(spec)
    else:
        url = swagger_handle(spec)
    api_id = 0
    api_list = []
    paths = spec.get('paths')
    for api_path in paths:
        methods = paths.get(api_path)
        for method in methods:
            api_id = api_id + 1
            complete_api_path = url + api_path
            params = methods.get(method).get("parameters")
            requestBody = methods.get(method).get("requestBody")
            req_param_list = []
            if params:
                if 'swagger' in spec:
                    req_param_list = parameter_swagger_handle(params, req_param_list)
                else:
                    req_param_list = parameter_handle(params, req_param_list)
            if requestBody:
                req_param_list = requestBody_handle(requestBody, req_param_list)
            if 'swagger' in spec:
                resp_param_list = response_swagger_handle(methods.get(method).get("responses"))
            else:
                resp_param_list = response_handle(methods.get(method).get("responses"))
            api = api_info(api_id, complete_api_path, req_param_list, resp_param_list, method)
            api_list.append(api)
    return  api_list

def parse(version,path):

    parser = ResolvingParser(path)
    spec = parser.specification
    api_list = paths_handle(spec)
    return api_list
    pass

path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/sdms.yaml")
parse(1,path)


#
# dictionary = {
#     79: {"id + sha +responses", "short_id + sha + responses"},
#     80: {"id + sha +responses", "short_id + sha + responses"},
#     81: {"id + sha +responses", "short_id + sha + responses"},
#     83: {"id + sha +responses", "short_id + sha + responses"},
#     84: {"id + sha +responses", "short_id + sha + responses"},
#     88: {"id + sha +responses"},
#     624: {"id + group_id + responses", "name + group_name + responses"},
#     625: {"name + group_name + responses", "name + group_name + parameters"},
#     626: {"id + group_id + responses", "name + group_name + responses"},
#     627: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
#     628: {"id + group_id + parameters", "id + group_id + responses"},
#     629: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
#     630: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + responses"},
#     631: {"id + group_id + parameters", "id + group_id + responses", "name + group_name + parameters", "name + group_name + responses"},
#     632: {"id + group_id + parameters"},
#     633: {"id + group_id + parameters", "id + group_id + responses"},
#     634: {"id + group_id + parameters"},
#     635: {"id + group_id + parameters"},
#     636: {"id + group_id + parameters", "id + group_id + responses"},
#     637: {"id + group_id + parameters"},
#     638: {"id + group_id + parameters"},
#     639: {"id + group_id + parameters"},
#     640: {"id + group_id + parameters"},
#     641: {"id + group_id + parameters"},
#     642: {"id + group_id + parameters"},
#     643: {"id + group_id + parameters"},
#     644: {"id + group_id + parameters"},
#     645: {"id + group_id + parameters"},
#     646: {"id + group_id + parameters"},
#     647: {"id + group_id + parameters", "id + group_id + responses"},
#     648: {"id + group_id + parameters", "id + group_id + responses"},
#     649: {"id + group_id + parameters", "id + group_id + responses"},
#     640: {"id + group_id + parameters"},
# }