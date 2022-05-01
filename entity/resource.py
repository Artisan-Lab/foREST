from module.string_march import StringMatch


class Resource:

    def __init__(self, resource_id, api_id, resource_name, resource_data, resource_request, resource_path):
        self.__resource_id = resource_id
        self.__resource_api_id = api_id
        self.__resource_name = resource_name
        self.__resource_path = resource_path
        self.resource_data = resource_data
        self.__resource_request = resource_request
        self.__parent_resource = []
        self.__children_resource = []

    @property
    def get_resource_request(self):
        return self.__resource_request

    @property
    def resource_id(self):
        return self.__resource_id

    @property
    def resource_name(self):
        return self.__resource_name

    @property
    def resource_api_id(self):
        return self.__resource_api_id

    @property
    def parent_resource(self):
        return self.__parent_resource

    @parent_resource.setter
    def parent_resource(self, parent_resource):
        self.__parent_resource.append(parent_resource)

    @property
    def children_resource(self):
        return self.__children_resource

    @children_resource.setter
    def children_resource(self, children_resource):
        self.__children_resource.append(children_resource)

    def find_field_from_name(self, field_name, field_type):
        value = StringMatch.find_field_in_dic(self.resource_data, field_name, field_type)
        if value:
            return value
        if '_' in field_name and '_' in self.resource_name:
            field_name_list = field_name.split('_')
            resource_name_list = self.resource_name.split('_')
            while resource_name_list:
                if field_name_list.pop(0) != resource_name_list.pop(0):
                    break
            value = StringMatch.find_field_in_dic(self.resource_data, field_name, field_type)
            if value:
                return value
        return None

    def find_field_from_path(self, resource_dict, field_path):
        if not resource_dict: return None
        if field_path[0] in resource_dict:
            if len(field_path) == 1:
                return resource_dict[field_path[0]]
            else:
                return self.find_field_from_path(resource_dict[field_path[0]], field_path[1:])
