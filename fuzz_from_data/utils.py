import constants


class Utils:
    @staticmethod
    def json_type(obj):
        if obj is None:
            return constants.NULL
        elif isinstance(obj, dict):
            return constants.OBJECT
        elif isinstance(obj, list):
            return constants.ARRAY
        elif isinstance(obj, bool):
            return constants.BOOLEAN
        elif isinstance(obj, int) or isinstance(obj, float) or isinstance(obj, complex):
            return constants.NUMBER
        elif isinstance(obj, str):
            return constants.STRING

    @staticmethod
    def is_complex_type(obj):
        return True if Utils.json_type(obj) in [constants.OBJECT, constants.ARRAY] else False

    @staticmethod
    def is_primitive_type(obj):
        return not Utils.is_complex_type(obj)

    @staticmethod
    def in_primitive_type(obj_type):
        return True if obj_type in [constants.STRING, constants.NUMBER, constants.BOOLEAN] else False
