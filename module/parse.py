from prance import ResolvingParser
from entity.api_info import api_info
from entity.field_info import field_info
import os.path



def parse(path,version):
    # path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/openapi.yaml")
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
                    for param in params:
                        field_name = param.get("name")
                        if 'oneOf' in param['schema']:
                            type_ = 'integer or string'
                        elif 'type' in param['schema']:
                            type_ = param['schema'].get("type")
                        else:
                            type_ = 'string'
                        require = param.get("required")
                        in_ = param.get("in")
                        if in_ == 'path':
                            in_ = 0
                        elif in_ == 'query':
                            in_ = 1
                        req_param = field_info(field_name, type_, require, "No", False, in_)
                        req_param_list.append(req_param)
                if requestBody:
                    properties = requestBody['content']['application/json']['schema']['properties']
                    for property_ in properties:
                        if "oneOf" in properties[property_]:
                            type_ = 'integer or string'
                        elif 'type_' in properties[property_]:
                            type_ = properties[property_]['type']
                        else:
                            type_ = 'string'
                        req_param = field_info(property_, type_,'false', "No", False, 3)
                        req_param_list.append(req_param)
                responses = methods.get(method).get("responses")
                resp_param_list = []
                for respond in responses:
                    if "content" in responses.get(respond):
                        schema = responses.get(respond).get("content").get("application/json").get("schema")
                        if schema['type'] == 'array':
                            array = schema['items']
                            if array['type'] == 'object':
                                for object_ in array['properties']:
                                    if "oneOf" in array['properties'][object_]:
                                        type_ = 'integer or string'
                                    elif 'type' in array['properties'][object_]:
                                        type_ = array['properties'][object_]['type']
                                    else:
                                        type_ = 'string'
                                    resp_param = field_info(object_, type_, "No", "No", False, "No")
                                    resp_param_list.append(resp_param)
                        elif schema['type'] == 'object':
                            for object_ in schema['properties']:
                                if "oneOf" in schema['properties'][object_]:
                                    type_ = 'integer or string'
                                elif 'type' in schema['properties'][object_]:
                                    type_ = schema['properties'][object_]['type']
                                else:
                                    type_ = 'string'
                                resp_param = field_info(object_, type_, "No", "No", False, "No")
                                resp_param_list.append(resp_param)
                api = api_info(api_id, complete_api_path, req_param_list, resp_param_list, method)
                api_list.append(api)
    return api_list

