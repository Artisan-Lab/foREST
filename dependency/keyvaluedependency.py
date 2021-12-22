from tool.tools import Tool
import copy



class SetKeyValueDependency:
    """
        find the parameter dependency and save it in field_info.depend_list
    """

    def __init__(self, api_info_list):
        self.api_info_list = api_info_list
        self.api_numbers = len(api_info_list)
        self.current_field_info = None
        self.current_api_info = None
        self.not_reference_field = []
        self.key_depend_api_list = []
        self.depended_field_list = []
        self.depended_field_path = []

    def find_depend_API(self):
        depend_field_dict = {}
        for api_info in self.api_info_list:
            self.depended_field_list = []
            if not api_info.resp_param or api_info.http_method != 'post':
                continue
            for field_info in api_info.resp_param:
                self.depended_field_path = [api_info.api_id]
                if self.find_depend_field(field_info) and \
                        self.current_field_info.require and \
                        api_info.api_id not in self.key_depend_api_list:
                    self.key_depend_api_list.append(api_info.api_id)

    def find_depend_field(self, compare_field, parent_name=''):
        if parent_name is None:
            parent_name = ''
        self.depended_field_path.append(compare_field.field_name)
        compare_method = Compare(self.current_field_info.field_name, self.current_field_info.field_type,
                                 compare_field.field_name, parent_name, compare_field.field_type)
        point = compare_method.smart_match()
        if point:
            if self.depended_field_path[0] in self.current_api_info.close_api:
                point += 1
            self.current_field_info.depend_list[0].append(copy.deepcopy(self.depended_field_path))
            self.current_field_info.depend_list[1].extend([point, point])
            self.depended_field_path.pop(-1)
            return True
        elif compare_field.field_type == 'dict':
            if compare_field.object:
                for object_info in compare_field.object:
                    if object_info.field_name:
                        if self.find_depend_field(object_info, compare_field.field_name):
                            self.depended_field_path.pop(-1)
                            return True
        elif compare_field.field_type == 'list':
            if self.find_depend_field(compare_field.array, compare_field.field_name):
                self.depended_field_path.pop(-1)
                return True
        self.depended_field_path.pop(-1)
        return False

    def get_field_dependency(self, field_info):
        self.current_field_info = field_info
        if field_info.field_name:
            self.find_depend_API()
        if not field_info.depend_list[0]:
            if field_info.field_name not in self.not_reference_field:
                self.not_reference_field.append(field_info.field_name)
        if field_info.field_type == 'list':
            self.get_field_dependency(field_info.array)
        if field_info.field_type == 'dict':
            if field_info.object:
                for object_info in field_info.object:
                    self.get_field_dependency(object_info)

    def get_dependency(self):
        """get every field dependency reference"""
        for api_info in self.api_info_list:
            self.current_api_info = api_info
            self.key_depend_api_list = []
            if api_info.req_param:
                # traverse every parameter
                for req_field_info in api_info.req_param:
                    if req_field_info.field_type == 'bool':
                        continue
                    self.get_field_dependency(req_field_info)
            api_info.key_depend_api_list = self.key_depend_api_list
        Tool.save_no_reference(self.not_reference_field)
        return self.api_info_list


class Compare:

    def __init__(self, compare_field_name, compare_field_type, compared_field_name,
                 compared_field_parent_name, compared_field_type):
        self.compare_field_name = compare_field_name
        self.compare_field_type = compare_field_type
        self.compared_field_name = compared_field_name
        self.compared_field_type = compared_field_type
        self.compared_field_parent_name = compared_field_parent_name

    def simple_match(self):
        if self.compared_field_name is None:
            return None
        self.compared_field_name.lower()
        self.compare_field_name.lower()
        if self.compared_field_name == self.compare_field_name and self.compared_field_type == self.compare_field_name:
            return self.compared_field_name
        else:
            return None

    def smart_match(self):
        if self.compared_field_name is None:
            return None
        if self.compared_field_name.lower() == self.compare_field_name.lower() and \
                self.compared_field_type == self.compare_field_type:
            return 7.5
        compared_field_name_list = self.compared_field_parent_name.split('_') + self.compared_field_name.split('_')
        compare_field_name_list = self.compare_field_name.split('_')[-1]
        compared_field_name = ''.join(compared_field_name_list).lower()
        compare_field_name = ''.join(compare_field_name_list).lower()
        if compared_field_name == compare_field_name:
            return 5
        if compared_field_name.endswith(compare_field_name):
            return 2.5
        else:
            return None
