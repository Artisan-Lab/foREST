import requests


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


class foRESTSetting:
    __instance = None

    @staticmethod
    def Instance():
        return foRESTSetting.__instance

    def __init__(self, args_dicts: dict):
        # ip of service under testing
        self._out_put = Argument('out_put', args_dicts, ['out_put'])
        self._target_ip = Argument('target_ip', args_dicts, ['target_ip'])
        # testing time budget: minutes
        self._time_budget = Argument('time_budget', args_dicts, ['time_budget'])
        # user token
        self._header = Argument('header', args_dicts, ['header'])
        # api file absolute path
        self._api_file_path = Argument('api_file_path', args_dicts, ['api_file_path'])
        # is use external key: bool
        self._external_key = Argument('external_key', args_dicts, ['function', 'external_key'])
        # external key definition file absolute path
        self._external_key_file_path = Argument('external_key_file_path', args_dicts, ['external_key_file_path'])
        # is use annotation_table : bool
        self._annotation_table = Argument('annotation_table', args_dicts, ['function', 'annotation_table'])
        # annotation table definition file absolute path
        self._annotation_table_file_path = Argument('annotation_table_file_path', args_dicts,
                                                    ['function', 'annotation_table_file_path'])
        # fuzz setting: dict
        self._fuzz_setting = Argument('fuzz_setting', args_dicts, ['fuzz'])
        # request setting: dict
        self._request_timeout = Argument('request_setting', args_dicts, ['request', 'timeout'])
        # Similarity cardinality in dependency analysis
        self._similarity_cardinality = Argument('similarity_cardinality', args_dicts, ['similarity_cardinality'])

        # Verify the validity of parameters
        # self.__check_argument()

        foRESTSetting.__instance = self

    def __check_argument(self):
        try:
            requests.get(self.target_ip)
        except:
            raise Exception("ERROR target ip")
        if isinstance(self.time_budget, str):
            try:
                self._time_budget = int(self.time_budget)
            except:
                raise Exception("ERROR time budget type")
        if self.external_key and not self.external_key_file_path:
            raise Exception("use annotation key table need annotation_key_table path")
        if self.annotation_table and not self.annotation_table_file_path:
            raise Exception("use annotation table need annotation_table path")

    @property
    def out_put(self):
        return self._out_put.value

    @property
    def similarity_cardinality(self):
        return self._similarity_cardinality.value

    @property
    def target_ip(self):
        return self._target_ip.value

    @target_ip.setter
    def target_ip(self, target_ip):
        self._target_ip.value = target_ip

    @property
    def time_budget(self):
        return self._time_budget.value

    @property
    def header(self):
        return self._header.value

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
    def request_timeout(self):
        return self._request_timeout.value


def foRESTSettings() -> foRESTSetting:
    return foRESTSetting.Instance()
