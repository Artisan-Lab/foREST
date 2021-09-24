class field_info:
    def __init__(self, field_name, type_, require,location,max_lenth=None, min_lenth=None,default=None,description=None,enum=None,object=None,array=None,max=None,min=None,format=None):
        self.field_name = field_name
        self.field_type = type_
        self.require = require
        self.default = default
        self.location = location
        self.max_lenth = max_lenth
        self.min_lenth = min_lenth
        self.enum = enum
        self.description = description
        self.object = object
        self.array = array
        self.maximum = max
        self.minimum = min
        self.format = format
        self.depend_list = []

    def add_depend_api(self, depend_api_id):
        self.depend_list += depend_api_id