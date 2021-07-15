class field_info:
    def __init__(self, field_name, type_, require,location,default=None,fuzz=None,description=None,enum=None,object=None,array=None,max=None,min=None,format=None):
        self.field_name = field_name
        self.field_type = type_
        self.require = require
        self.default = default
        self.fuzz = fuzz
        self.location = location
        self.enum = enum
        self.description = description
        self.object = object
        self.array = array
        self.max = max
        self.min = min
        self.format = format
        self.depend_list = []

    def add_depend_api(self, depend_api_id):
        self.depend_list += depend_api_id
