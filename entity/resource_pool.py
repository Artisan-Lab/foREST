from entity.api_info import *
import copy
from module.utils.utils import *
# Stemming algorithm


class Resource:

    def __init__(self, resource_id, api_info: APIInfo, resource_data, resource_request):
        self.__resource_id = resource_id
        self.__resource_identifier = api_info.identifier
        self.__api_info = api_info
        self.resource_data = resource_data
        self.__request = resource_request
        self.__parent_resource = []
        self.__children_resource = []

    @property
    def request(self):
        return self.__request

    @property
    def id(self):
        return self.__resource_id

    @property
    def api_info(self):
        return self.__api_info

    @property
    def parent_resource(self):
        return self.__parent_resource

    @parent_resource.setter
    def parent_resource(self, parent_resource):
        self.__parent_resource.append(parent_resource)
        parent_resource.children_resource.append(self)

    @property
    def children_resource(self):
        return self.__children_resource

    @children_resource.setter
    def children_resource(self, children_resource):
        self.__children_resource.append(children_resource)
        children_resource.parent_resource.append(self)

    def get_value_by_path(self, field_path):
        return DictHandle.find_by_path(self.resource_data, field_path)


class ResourcePool:
    __instance = None

    @staticmethod
    def instance():
        if ResourcePool.__instance is None:
            raise Exception("Resource Pool not yet initialized.")
        return ResourcePool.__instance
    """
        this class define the Resource pool
    """
    def __init__(self, api_list):
        self.resource_identifier_dict = {}
        self.resource_tree_dict = {}
        self.resource_id = 0
        self.build_resource_pool(api_list)
        self.origin_resource_pool = None
        ResourcePool.__instance = self

    def build_resource_pool(self, api_list: List[APIInfo]):
        for api_info in api_list:
            self.resource_identifier_dict[api_info.identifier] = []
            method, path = api_info.http_method, api_info.path
            if path not in self.resource_tree_dict:
                self.resource_tree_dict[path] = {}
            self.resource_tree_dict[path][method] = self.resource_identifier_dict[api_info.identifier]
        self.origin_resource_pool = copy.deepcopy(self.resource_identifier_dict)

    def reset_resource_pool(self):
        self.resource_identifier_dict = copy.deepcopy(self.resource_identifier_dict)

    def get_special_value_from_resource(self, api_identifier, field_path):
        resource = self.get_resource(api_identifier)
        if resource:
            return resource.get_value_by_path(field_path)

    def add_resource_to_identifier_dict(self, resource, identifier):
        if len(self.resource_identifier_dict[identifier]) > 100:
            self.resource_identifier_dict[identifier].pop(0)
        self.resource_identifier_dict[identifier].append(resource)

    def create_resource(self, api_info: APIInfo, resource_data, resource_request, parent_resource=None):
        resource = Resource(self.resource_id, api_info, resource_data, resource_request)
        identifier = api_info.identifier
        self.add_resource_to_identifier_dict(resource, identifier)
        self.resource_id += 1
        if parent_resource:
            resource.parent_resource = parent_resource

    def get_resource(self, resource_identifier):
        if resource_identifier in self.resource_identifier_dict and self.resource_identifier_dict[resource_identifier]:
            return random.choice(self.resource_identifier_dict[resource_identifier])
        return None

    def find_parent_resource(self, path):
        path_list = path.split("/")[1:]
        length = len(path_list)
        for i in range(1, length):
            new_path = "/"+"/".join(path_list[:length-i])
            if new_path in self.resource_tree_dict and self.resource_tree_dict[new_path]:
                method_list = list(self.resource_tree_dict[new_path].keys())
                random.shuffle(method_list)
                for method in method_list:
                    if method == "delete":
                        continue
                    if self.resource_tree_dict[new_path][method]:
                        return random.choice(self.resource_tree_dict[new_path][method])


def resource_pool() -> ResourcePool:
    """ Accessor for the Resource Pool singleton """
    return ResourcePool.instance()
