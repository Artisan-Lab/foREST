import json
import random

from commons import constants


class Utils:
    """
    some commons methods
    """

    @staticmethod
    def json_type(obj):
        """
        given an obj,return its type defined in json
        """
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
        """
        return true if obj's type is object or array,otherwise return false
        """
        return True if Utils.json_type(obj) in [constants.OBJECT, constants.ARRAY] else False

    @staticmethod
    def is_primitive_type(obj):
        """
         return true if obj's type is bool/int/str,otherwise return false
        """
        return not Utils.is_complex_type(obj)

    @staticmethod
    def in_primitive_type(obj_type):
        """
        return true if obj_type is one of primitive types,otherwise return false
        """
        return True if obj_type in [constants.STRING, constants.NUMBER, constants.BOOLEAN] else False

    @staticmethod
    def is_json(s):
        """
        conclude whether a string is json format
        """
        try:
            json.loads(s)
        except:
            return False
        return True

    @staticmethod
    def decision(probability):
        """
        return True/False according to probability settings
        """
        return random.random() < probability
