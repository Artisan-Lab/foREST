class field_info:
    def __init__(self,field_name,type_,require,default,fuzz,location,description,enum):
        self.field_name = field_name
        self.field_type = type_
        self.require = require
        self.default = default
        self.fuzz = fuzz
        self.location = location
        self.enum = enum
        self.description = description
