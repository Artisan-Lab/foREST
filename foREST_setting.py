import configparser
import os
import nltk
import datetime


class Argument(object):

    def __init__(self, name, arg_list, path: list):
        self._name = name
        self._value = Argument.set_arg(path, arg_list)

    @staticmethod
    def set_arg(path: list, arg_list):
        """ set argument

        @param path: the path to find the argument
        @type path: list
        @param arg_list: all argument
        @type arg_list: list or object
        @return: value
        @rtype: int or str
        """
        if not (isinstance(arg_list, object) or isinstance(arg_list, list)):
            raise Exception("Invalid value")
        if path[0] in arg_list:
            if len(path) == 1:
                return arg_list[path[0]]
            return Argument.set_arg(path[1:], arg_list[path[0]])
        else:
            return None

    def __getitem__(self):
        return self._value

    @property
    def value(self):
        """ get value

        @return: value
        @rtype: int or str
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """ reset value

        @param new_value:
        @type new_value:
        @return: None
        @rtype: None
        """
        self._value = new_value


def foRESTSettings():
    return foRESTSetting.Instance()


class foRESTSetting:
    __instance = None

    @staticmethod
    def Instance():
        return foRESTSetting.__instance

    def __init__(self, args_dicts: dict):
        # ip of service under testing
        self._target_ip = Argument('target_ip', args_dicts, ['target_ip'])
        # foREST work mode: pure testing or data based testing
        self._foREST_mode = Argument('foREST_mode', args_dicts, ['foREST_mode'])
        # testing time budget: minutes
        self._time_budget = Argument('time_budget', args_dicts, ['time_budget'])
        # user token
        self._token = Argument('token', args_dicts, ['token'])
        # api file absolute path
        self._api_file_path = Argument('api_file_path', args_dicts, ['api_file_path'])
        # is use external key: bool
        self._external_key = Argument('external_key', args_dicts, ['function', 'external_key'])
        # external key definition file absolute path
        self._external_key_file_path = Argument('external_key_file_path', args_dicts, ['external_key_file_path'])
        # is use annotation_table : bool
        self._annotation_table = Argument('annotation_table', args_dicts, ['function', 'annotation_table'])
        # annotation table definition file absolute path
        self._annotation_table_file_path = Argument('annotation_table_file_path', args_dicts, ['function', 'annotation_table_file_path'])
        # fuzz setting: dict
        self._fuzz_setting = Argument('fuzz_setting', args_dicts, ['fuzz'])
        # request setting: dict
        self._request_setting = Argument('request_setting', args_dicts, ['request'])

        foRESTSetting.__instance = self

    @property
    def target_ip(self):
        return self._target_ip.value

    @target_ip.setter
    def target_ip(self, target_ip):
        self._target_ip.value = target_ip

    @property
    def foREST_mode(self):
        return self._foREST_mode.value

    @property
    def time_budget(self):
        return self._time_budget.value

    @property
    def token(self):
        return self._token.value
    
    @property
    def api_file_path(self):
        return self._api_file_path.value

    @property
    def external_key(self):
        return self._external_key.value

    @property
    def external_key_file_path(self):
        return self._external_key_file_path.value

    @property
    def annotation_table(self):
        return self._annotation_table.value

    @property
    def annotation_table_file_path(self):
        return self._annotation_table_file_path.value

    @property
    def fuzz_setting(self):
        return self._fuzz_setting.value

    @property
    def request_setting(self):
        return self._request_setting
