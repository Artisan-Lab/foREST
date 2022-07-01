import re

pattern = re.compile(r'{.*}')


class LogEntity:

    def __init__(self, log_id, method:str, url, headers, body, path, response_code, response_data, user_id):
        self.log_id = log_id
        self.method = method.upper()
        self.url = url
        self.headers = headers
        self.body = body
        self.path = path
        self.identifier = self.method + '  ' + self.path # type: str
        self.response_code = response_code
        self.response_data = response_data
        self.user_id = user_id
        self.api_id = -1
        self.path_parameter = {}
        self.query_parameter = {}
        self.find_query_parameter()
        self.find_path_parameter()

    def find_query_parameter(self):
        if "?" in self.url:
            query_parameter = self.url.split('?')[-1]
            query_parameter_list = query_parameter.split('&')
            for parameter in query_parameter_list:
                parameter_pair = parameter.split('=')
                key = parameter_pair[0]
                value = parameter_pair[1]
                try:
                    value = int(value)
                except:
                    pass
                self.query_parameter[key] = value

    def find_path_parameter(self):
        path_list = self.path.split('?')[0]
        path_list = path_list.split('/')[1:]
        path_parameter_list = self.url.split("?")[0].split('/')[1:]
        for i in range(len(path_list)):
            if re.search(pattern, path_list[i]):
                key = path_list[i][1:-1]
                value = path_parameter_list[i]
                try:
                    value = int(value)
                except:
                    pass
                self.path_parameter[key] = value


def find_value(log_dic, data_path):
    if isinstance(data_path, str):
        return data_path
    elif not data_path or not log_dic:
        return None
    elif len(data_path) == 1:
        try:
            return log_dic[data_path[0]]
        except:
            return None
    else:
        if data_path[0] == '/':
            return find_value(log_dic[0], data_path[1:])
        else:
            return find_value(log_dic.get(data_path[0]), data_path[1:])


def get_all_value(log_dic, structure_entity):
    base_url = find_value(log_dic, structure_entity.get('base_URL'))
    path = find_value(log_dic, structure_entity.get('path'))
    http_method = find_value(log_dic, structure_entity.get('http_method'))
    headers = find_value(log_dic, structure_entity.get('headers'))
    body = find_value(log_dic, structure_entity.get('body'))
    response_code = find_value(log_dic, structure_entity.get('response_code'))
    response_data = find_value(log_dic, structure_entity.get('response_data'))
    user_id = find_value(log_dic, structure_entity.get('user_id'))
    return http_method, base_url, headers, body, path, response_code, response_data, user_id


class LogPool:
    __instance = None

    @staticmethod
    def Instance():
        """ Singleton's instance accessor

        @return FuzzingMonitor instance
        @rtype  FuzzingMonitor

        """
        if LogPool.__instance is None:
            raise Exception("foREST Monitor not yet initialized.")
        return LogPool.__instance

    def __init__(self):
        self.log_id = 0
        self.log_list = []
        self.user_dict = {}
        LogPool.__instance = self

    def save_foREST_log(self, method, url, headers, body, path, response_code, response_data, user_id):
        log_entity = LogEntity(self.log_id, method, url, headers, body, path, response_code, response_data, user_id)
        self.log_list.append(log_entity)
        self.log_id += 1

    def save_log(self, log_data, structure_entity):
        log_list = []
        for log in log_data:
            all_value = get_all_value(log, structure_entity)
            log_entity = LogEntity(self.log_id, *all_value)
            log_list.append(log_entity)
            self.log_id += 1
        self.log_list = log_list

    def user_classification(self):
        for log in self.log_list:
            if not log.user_id:
                log.user_id = "no user"
            if self.user_dict.get(log.user_id):
                self.user_dict[log.user_id].append(log)
            else:
                self.user_dict[log.user_id] = [log]



log_pool = LogPool()


