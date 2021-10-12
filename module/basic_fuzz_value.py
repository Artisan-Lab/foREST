import sys


class BasicFuzzValue:


    def __init__(self, int_val=None, float_val=None, string_val=None, bool_val=None):
        if int_val is None:
            int_val = [-sys.maxsize - 1, sys.maxsize]
        if float_val is None:
            float_val = [sys.float_info.min, sys.float_info.max]
            if string_val is None:
                string_val = {"char_seed": "0123456789abcdefghijklmnopqrstuvwxyz!@#$%^&*()_=+-",
                              "string_dict": ["string", "long string", "email:1@gmail.com"]}
        if bool_val is None:
            bool_val = ['true', 'false']
        self._int_val = int_val
        self._float_val = float_val
        self._string_val = string_val
        self._bool_val = bool_val


    @property
    def int_val(self):
        return self._int_val

    @int_val.setter
    def int_val(self, new_int_val):
        self._int_val = new_int_val

    @property
    def float_val(self):
        return self.float_val

    @float_val.setter
    def float_val(self, new_float_val):
        self._float_val = new_float_val

    @property
    def bool_val(self):
        return self._bool_val

    @bool_val.setter
    def bool_val(self, new_bool_val):
        self._bool_val = new_bool_val

    @property
    def string_val(self):
        return self._string_val

    @string_val.setter
    def string_val(self, new_string_val):
        self._string_val = new_string_val
