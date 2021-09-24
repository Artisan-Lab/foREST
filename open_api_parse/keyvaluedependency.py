class SetKeyValueDependency:

    def __init__(self, api_info_list):
        self.api_info_list = api_info_list
        self.api_numbers = len(api_info_list)
        self.current_field_info = None

    def find_depend_API(self):
        depend_field_list = []
        for api_info in self.api_info_list:
            if not api_info.resp_param:
                continue
            for field_info in api_info.resp_param:
                if self.find_depend_field(field_info):
                    depend_field_list.append(api_info.api_id)
                    break
        return depend_field_list

    def find_depend_field(self, compare_field):
        if self.current_field_info.field_name == compare_field.field_name and \
                self.current_field_info.field_type == compare_field.field_type and compare_field.field_name:
            return True
        elif compare_field.field_name == 'object':
            if compare_field.object:
                for object_info in compare_field.object:
                    if self.find_depend_field(object_info):
                        return True
        elif compare_field.field_type == 'array':
            if self.find_depend_field(compare_field.array):
                return True
        return False

    def get_field_dependency(self, field_info):
        self.current_field_info = field_info
        field_info.add_depend_api(self.find_depend_API())
        if field_info.field_type == 'array':
            self.get_field_dependency(field_info.array)
        if field_info.field_type == 'object':
            if field_info.object:
                for object_info in field_info.object:
                    self.get_field_dependency(object_info)

    def get_dependency(self):
        for api_info in self.api_info_list:
            if api_info.req_param:
                for req_field_info in api_info.req_param:
                    self.get_field_dependency(req_field_info)
        return self.api_info_list
