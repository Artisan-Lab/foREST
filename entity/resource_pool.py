import copy

from entity.resource import Resource
import random
import nltk
from fuzzywuzzy import fuzz
from module.string_march import StringMatch
from tool.tools import Tool
sno = nltk.stem.SnowballStemmer('english')
# Stemming algorithm


class ResourcePool:
    """
        this class define the Resource pool
    """
    def __init__(self):
        self.resource_name_dict = {}
        self.resource_list = []
        self.resource_api_id_dict = {}
        self.resource_id = 0

    def get_special_value_from_resource(self, api_id, field_path):
        resource = self.find_resource_from_api_id(api_id)
        if resource:
            return resource.find_field_from_path(resource.resource_data, field_path)
        else:
            return None

    def save_response(self, api_info, request, response, parent_resource):
        base_url_list = api_info.path.split('/')
        if not StringMatch.is_path_variable(base_url_list[-1]):
            resource_name = base_url_list[-1]
            return self.create_resource(resource_name, api_info.api_id, response, request, api_info.path, parent_resource)

    def create_resource(self, resource_name, api_id, resource_data, resource_request, resource_path, parent_resource=None):
        resource_name = sno.stem(resource_name)
        resource = Resource(self.resource_id, api_id, resource_name, resource_data, resource_request, resource_path)
        self.resource_list.append(resource)
        if api_id == 34:
            print(1)
        if resource_name in self.resource_name_dict:
            if len(self.resource_name_dict[resource_name]) > 100:
                self.delete_resource(self.resource_name_dict[resource_name][0])
            self.resource_name_dict[resource_name].append(resource)
        else:
            self.resource_name_dict[resource_name] = [resource]
        if api_id in self.resource_api_id_dict:
            self.resource_api_id_dict[api_id].append(resource)
        else:
            self.resource_api_id_dict[api_id] = [resource]
        self.resource_id += 1
        if parent_resource:
            resource.parent_resource = parent_resource
            parent_resource.children_resource = resource
        return resource

    def find_resource_from_id(self, resource_id):
        for resource in self.resource_list:
            if resource.resource_id == resource_id:
                return resource
        return None

    def find_resource_from_api_id(self, resource_api_id):
        if resource_api_id in self.resource_api_id_dict and self.resource_api_id_dict[resource_api_id]:
            return random.choice(self.resource_api_id_dict[resource_api_id])
        return None

    def find_resource_from_resource_name(self, name):
        name = sno.stem(name)
        self.resource_name_dict = Tool.random_dic(self.resource_name_dict)
        for resource_name in self.resource_name_dict:
            if fuzz.partial_ratio(name, resource_name) >= 90:
                if self.resource_name_dict[resource_name]:
                    return random.choice(self.resource_name_dict[resource_name])
        return None

    def __delete_resource(self, resource):
        if resource.resource_api_id == 34:
            print(1)
        if resource.children_resource:
            for child_resource in resource.children_resource:
                self.delete_resource(resource=child_resource)
        if resource.parent_resource:
            for single_parent_resource in resource.parent_resource:
                single_parent_resource.children_resource.remove(resource)
        self.resource_list.remove(resource)
        self.resource_name_dict[sno.stem(resource.resource_name)].remove(resource)
        self.resource_api_id_dict[resource.resource_api_id].remove(resource)

    def delete_resource(self, resource=None, resource_id=None):
        if not (resource or resource_id):
            return None
        if resource_id:
            resource = self.find_resource_from_id(resource_id)
        self.__delete_resource(resource)

    def find_parent_resource_name(self, path_list):
        for path in path_list[::-1]:
            if StringMatch.is_path_variable(path):
                continue
            else:
                if path in self.resource_name_dict:
                    return path
        return ''


foREST_POST_resource_pool = ResourcePool()