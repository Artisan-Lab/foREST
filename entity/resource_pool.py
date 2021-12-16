from entity.resource import Resource
import random
import nltk
sno = nltk.stem.SnowballStemmer('english')
# Stemming algorithm


class ResourcePool:
    '''
        this class define the Resource pool
    '''
    def __init__(self):
        self.__resource_name_dict = {}
        self.__resource_list = []
        self.__resource_api_id_dict = {}
        self.resource_id = 0

    def save_response(self, api_info, request, response):
        base_url_list = api_info.base_url.split('/')
        if not(base_url_list[-1][0] == '{' and base_url_list[-1][-1] == '}'):
            resource_name = '/'.join(api_info.base_url.split('/')[-2:-1])
            resource_name = sno.stem(resource_name)
            self.create_resource(api_info.api_id, resource_name, response, request)

    def create_resource(self, resource_name, api_id, resource_data, resource_request):
        resource = Resource(self.resource_id, resource_name, api_id, resource_data, resource_request)
        self.__resource_list.append(resource)
        if resource_name in self.__resource_name_dict:
            self.__resource_name_dict[resource_name].append(resource)
        else:
            self.__resource_name_dict[resource_name] = [resource]
        self.resource_id += 1

    def find_resource_from_id(self, resource_id):
        for resource in self.__resource_list:
            if resource.resource_id == resource_id:
                return resource
        return None

    def find_resource_from_api_id(self, resource_api_id):
        if resource_api_id in self.__resource_name_dict:
            return random.choice(self.__resource_name_dict[resource_api_id])
        return None

    def find_resource_from_resource_name(self, resource_name):
        resource_name = sno.stem(resource_name)
        if resource_name in self.__resource_name_dict:
            return random.choice(self.__resource_name_dict[resource_name])
        return None

    def __delete_resource(self, resource):
        if resource.children_resource:
            for child_resource in resource.children_resource:
                self.delete_resource(resource=child_resource)
            self.__resource_list.remove(resource)
            self.__resource_name_dict[resource.resource_api_id].remove(resource)
        if resource.parent_resource:
            for single_parent_resource in resource.parent_resource:
                single_parent_resource.children_resource.remove(resource)

    def delete_resource(self, resource=None, resource_id=None):
        if not (resource or resource_id):
            return None
        if resource_id:
            resource = self.find_resource_from_id(resource_id)
        self.__delete_resource(resource)


foREST_resource_pool = ResourcePool()


