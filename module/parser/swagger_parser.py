import os

from entity.api_info import *
from foREST_setting import foRESTSettings
import random


class SwaggerParser:

    def __init__(self, data):
        self.paths = data.get('paths')
        if data.get('basePath') == "/":
            base_path = ""
        else:
            base_path = data.get("basePath")
        if foRESTSettings().target_ip:
            self.base_url = foRESTSettings().target_ip + base_path
        else:
            self.base_url = random.choice(data.get('schemes')) + '://' + data.get('host') + base_path
        self.api_id = 0
        self.api_list = []
        self.current_field = []
        self.location = ''
        self.required = False
        self.produces = data.get("produces")
        self.consumes = data.get("consumes")

    def swagger_parser(self):
        for path in self.paths:
            api_path = self.paths[path]
            for method in api_path:
                api = self.paths[path][method]
                api_parameters = api.get('parameters')
                api_responses = api.get('responses')
                api_produces = api.get('produces')
                if api_produces is None:
                    api_produces = self.produces
                api_consumes = api.get("consumes")
                if api_consumes is None:
                    api_consumes = self.consumes
                api = APIInfo(self.api_id, self.base_url, path,
                              self.parameters_handle(api_parameters),
                              self.responses_handle(api_responses), method, api_produces, api_consumes)
                self.api_list.append(api)
                self.api_id += 1
        return self.api_list

    def create_filed_info(self, api_parameter):
        if not api_parameter:
            return None
        if 'allOf' in api_parameter:
            return FieldInfo(field_name=api_parameter.get('name'),
                             type_='dict',
                             location=self.location,
                             require=True if api_parameter.get('required') else False,
                             object=self.allOf_handle(api_parameter.get('allOf')))
        if api_parameter.get("in") == 'path':
            self.location = 0
        elif api_parameter.get("in") == 'query':
            self.location = 1
        elif api_parameter.get("in") == 'header':
            self.location = 2
        elif api_parameter.get("in") == 'body' or api_parameter.get('in') == 'formData':
            self.location = 3
        parameter_schema = api_parameter.get('schema')
        if parameter_schema:
            return FieldInfo(field_name=api_parameter.get('name'),
                             type_=self.yaml_type_switch(parameter_schema.get('type')),
                             require=True if api_parameter.get('required') else False,
                             location=self.location,
                             max_lenth=parameter_schema.get('maxLength'),
                             min_lenth=parameter_schema.get('minLength'),
                             default=parameter_schema.get('default'),
                             description=api_parameter.get('description'),
                             enum=parameter_schema.get('enum'),
                             object=self.object_handle(parameter_schema.get('properties'),
                                                        parameter_schema.get('required')
                                                        if parameter_schema.get('required') else []),
                             array=self.create_filed_info(parameter_schema.get('items')),
                             max=parameter_schema.get('maximum'),
                             min=parameter_schema.get('minimum'),
                             format=parameter_schema.get('format'),
                             pattern=parameter_schema.get('pattern'))
        else:
            return FieldInfo(field_name=api_parameter.get('name'),
                             type_=self.yaml_type_switch(api_parameter.get('type')),
                             require=True if api_parameter.get('required') else False,
                             location=self.location,
                             max_lenth=api_parameter.get('maxLength'),
                             min_lenth=api_parameter.get('minLength'),
                             default=api_parameter.get('default'),
                             description=api_parameter.get('description'),
                             enum=api_parameter.get('enum'),
                             object=self.object_handle(api_parameter.get('properties'),
                                                        api_parameter.get('required')
                                                        if api_parameter.get('required') else []),
                             array=self.create_filed_info(api_parameter.get('items')),
                             max=api_parameter.get('maximum'),
                             min=api_parameter.get('minimum'),
                             format=api_parameter.get('format'),
                             pattern=api_parameter.get('pattern')
                             )

    def object_handle(self, objects, required_list):
        if not required_list:
            required_list = []
        objects_list = []
        if not objects:
            return None
        if objects.get('allOf'):
            return self.allOf_handle(objects['allOf'])
        for object_name in objects:
            required = True if object_name in required_list else False
            single_object = objects[object_name]
            objects_list.append(FieldInfo(
                field_name=object_name,
                type_=self.yaml_type_switch(single_object.get('type')),
                require=required,
                location=self.location,
                max_lenth=single_object.get('maxLength'),
                min_lenth=single_object.get('minLength'),
                default=single_object.get('default'),
                description=single_object.get('description'),
                enum=single_object.get('enum'),
                object=self.object_handle(single_object.get('properties'), single_object.get('required') if single_object.get('required') else []),
                array=self.create_filed_info(single_object.get('items')),
                max=single_object.get('maximum'),
                min=single_object.get('minimum'),
                format=single_object.get('format'),
                pattern=single_object.get('pattern')
                )
            )
        return objects_list

    def parameters_handle(self, api_parameters):
        parameter_list = []
        if api_parameters:
            for api_parameter in api_parameters:
                if api_parameter.get("in") == "body":
                    self.location = 3
                    if api_parameter.get("schema").get("type") == "object":
                        field_info = self.object_handle(api_parameter.get("schema").get("properties"), api_parameter.get("schema").get("required"))
                        if field_info:
                            parameter_list.extend(field_info)
                    elif api_parameter.get("schema").get("type") == "array":
                        parameter_list.append(self.create_filed_info(api_parameter.get("schema")))
                    else:
                        parameter_list.append(self.create_filed_info(api_parameter))
                else:
                    parameter_list.append(self.create_filed_info(api_parameter))
        return parameter_list

    def responses_handle(self, api_responses):
        responses_list = []
        self.location = 5
        for response_code in api_responses:
            response = api_responses[response_code]
            response_schema = response.get('schema')
            if response_schema:
                if response_schema.get('properties'):
                    responses_list += self.object_handle(response_schema.get('properties'), [])
                elif response_schema.get('items'):
                    responses_list.append(self.create_filed_info(response_schema))
                elif response_schema.get('allOf'):
                    responses_list += self.allOf_handle(response_schema.get('allOf'))
        return responses_list

    def allOf_handle(self, all_off_item):
        parameter_list = []
        for member in all_off_item:
            if 'properties' in member:
                parameter_list += self.object_handle(member.get('properties'), [])
        return parameter_list

    @staticmethod
    def yaml_type_switch(type_):
        if type_ == 'object':
            return 'dict'
        if type_ == 'integer':
            return 'int'
        if type_ == 'string':
            return 'str'
        if type_ == 'boolean':
            return 'bool'
        if type_ == 'array':
            return 'list'
        if type_ == 'number':
            return 'number'

    @staticmethod
    def resolve_circular_references(spec):
        if "definitions" in spec:
            references = spec["definitions"]
            visited_references = {}
            for key in references:
                visited_references[key] = 0
            for key in references:
                if visited_references[key] == 0:
                    SwaggerParser.traverse(references, key, visited_references)
            spec["definitions"]= references

    @staticmethod
    def traverse(referencs, key, visited_references):
        visited_references[key] = 1
        if "properties" not in referencs[key]:
            return
        proerties_to_delete = []
        for property in referencs[key]["properties"]:
            if "$ref" in referencs[key]["properties"][property]:
                key_ = os.path.basename(referencs[key]["properties"][property]["$ref"])
            elif "items" in referencs[key]["properties"][property] and "$ref" in referencs[key]["properties"][property]["items"]:
                key_ = os.path.basename(referencs[key]["properties"][property]["items"]["$ref"])
            else:
                continue
            if key_ not in visited_references:
                continue
            if visited_references[key_] == 0:
                SwaggerParser.traverse(referencs, key_, visited_references)
            elif visited_references[key_] == 1:
                proerties_to_delete.append(property)
        for property in proerties_to_delete:
            referencs[key]["properties"].pop(property)
        visited_references[key] = 2
