from prance import ResolvingParser
from entity.api_info import api_info
from entity.field_info import field_info
import os.path


def array_handle(items, location):
    if 'type' in items:
        type = items['type']
    else:
        type = 'object'
    if 'properties' in items:
        return object_handle(items['properties'], location)
    elif type == 'array':
        return array_handle(items['items'], location)
    else:
        return items['type']


def object_handle(objects, location, required=False):
    object_list = []
    for object in objects:
        if 'type' in objects[object]:
            type = objects[object]['type']
        else:
            type = 'object'
        if type == 'object':
            if 'properties' in objects[object]:
                object_field = field_info(field_name=object, type_=type,
                                          object=object_handle(objects[object]['properties'], location),
                                          location=location, require=required)
            else:
                object_field = field_info(field_name=object, type_=type,location=location, require=required)
        elif type == 'array':
            object_field = field_info(field_name=object, type_=type,
                                      array=array_handle(objects[object]['items'], location=location),
                                      location=location, require=required)
        else:
            object_field = field_info(field_name=object, type_=type, location=location, require=required)
        object_list.append(object_field)
    return object_list


def properties_handle(properties,location,required_list=[]):
    properties_list = []
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
        if request_type == 'object' and 'properties' in properties[property]:
            object_list = object_handle(properties[property]['properties'], location=location)
            array_type = None
        elif request_type == 'array' and 'items' in properties[property]:
            array_type = array_handle(properties[property]['items'], location=location)
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
        if 'format' in properties[property]:
            format = properties[property]['format']
        else:
            format = None
        request_property = field_info(field_name=property, type_=request_type, require=request_required, default=request_default,
                                    location=3, description=request_description, enum=request_enum, object=object_list,
                                      array=array_type, max=max, min=min, format=format)
        properties_list.append(request_property)
    return properties_list


def parameter_handle(parameter_list, req_param_list):
    for parameter in parameter_list:
        parameter_name = parameter['name']
        if 'type' in parameter['schema']:
            parameter_type = parameter['schema']['type']
        elif 'oneOf' in parameter['schema']:
            parameter_type = 'string'
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
        if 'format' in parameter['schema']:
            format = parameter['schema']['format']
        else:
            format = None
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
        else:
            parameter_location = 5
        if 'required' in parameter:
            parameter_required = parameter['required']
        else:
            parameter_required = False
        if parameter_type == 'array':
            array_type = array_handle(parameter['schema']['items'], parameter_location)
        else:
            array_type = None
        if parameter_type == 'object':
            try:
                object_type = object_handle(parameter['properties'], location=parameter_location, required=parameter_required)
            except:
                object_type = None
        else:
            object_type = None
        req_param = field_info(field_name=parameter_name, type_=parameter_type, require=parameter_required, default=parameter_default,
                                location=parameter_location,  description=parameter_description, enum=parameter_enum,
                               object=object_type, array=array_type, max=max, min=min, format=format)
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
                array_type = array_handle(parameter['items'],location=parameter_location)
            else:
                array_type = None
        else:
            array_type = None
        if parameter_type == 'object':
            object_type = object_handle(parameter['schema']['properties'],location=parameter_location)
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
        if 'format' in parameter:
            format = parameter['format']
        else:
            format = None
        req_param = field_info(parameter_name, parameter_type, parameter_required, parameter_default,
                               "No", parameter_location, parameter_description,parameter_enum,  object_type, array_type, max,
                               min,format)
        req_param_list.append(req_param)
    return req_param_list


def response_swagger_handle(responses):
    resp_params_list = []
    for response in responses:
        if 'schema' in responses[response]:
            if 'properties' in responses[response]['schema']:
                    properties = responses[response]['schema']['properties']
                    resp_params_list = properties_handle(properties, location=5)
            elif 'array' == responses[response]['schema']['type']:
                items = responses[response]['schema']['items']
                resp_params_list = array_handle(items, location=5)
        return resp_params_list


def response_handle(responses):
    resp_params_list = []
    for response in responses:
        if 'content' in responses[response]:
            for key in responses[response]['content']:
                properties_alls = key
            if 'object' in responses[response]['content'][properties_alls]['schema']['type']:
                properties = responses[response]['content'][properties_alls]['schema']['properties']
                resp_params_list = properties_handle(properties, location=5)
            elif 'array' == responses[response]['content'][properties_alls]['schema']['type']:
                properties = responses[response]['content'][properties_alls]['schema']['items']
                resp_params_list = properties_handle(properties, location=5)
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
    return properties_handle(properties, location=3,required_list=required_list)


def get_swagger_url(spec):
    url = spec.get('host') + spec.get('basePath')
    return url


def get_open_api_url(spec):
    servers = spec.get('servers')
    for server in servers:
        url = server.get('url').replace('https','http')
    return url


def paths_handle(spec):
    if 'swagger' in spec:
        host = get_swagger_url(spec)
    else:
        host = get_open_api_url(spec)
    '''Obtain the domain name from the document'''
    api_id = 0
    api_list = []
    paths = spec.get('paths')
    for api_path in paths:
        methods = paths.get(api_path)
        for method in methods:
            complete_api_path = host + api_path
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
            api_id = api_id + 1
    return api_list


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/openapi.yaml")
    a = get_api_info(1,path)
    print(1)


def get_api_info(version, path):
    spec = ''
    try:
        parser = ResolvingParser(path)
        spec = parser.specification
    except:
        print("open-api file can't parse")
    api_list = paths_handle(spec)
    return api_list


if __name__  == '__main__':
    main()
