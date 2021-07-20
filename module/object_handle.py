from module.type_fuzz import fuzz

class fuzz_object:

    def array_handle(self, array):
        array_list = []
        value = None
        if isinstance(array, str):
            if array == 'integer' or array == 'boolean' or array == 'string':
                value = fuzz(array)
        elif isinstance(array, list):
            value = fuzz_object().object_handle(array)
        array_list.append(value)
        return array_list

    def object_handle(self, objects):
        object_list = {}
        for object_ in objects:
            value = None
            if object_.type == 'object':
                if object_.object:
                    value = fuzz_object().object_handle(object_.object)
                else:
                    value = 'None'
            elif object_.type == 'string' or object_.type == 'boolean' or object_.type == 'integer':
                value = fuzz(object_.type)
            elif object_.type == 'array':
                value = fuzz_object().array_handle(object_.object)
            object_list[object_.name] = value
        return object_list