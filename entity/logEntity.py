import re

pattern = re.compile(r'{.*}')


class LogEntity:

    def __init__(self, log_id, method, url, headers, body, path, response_code, response_data, user_id):
        self.log_id = log_id
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
        self.path = path
        self.response_code = response_code
        self.response_data = response_data
        self.user_id = user_id
        self.api_id = -1
        self.path_parameter = {}
        self.query_parameter = {}
        self.find_query_parameter()
        self.find_path_parameter()

    def set_api_id(self, api_id):
        self.api_id = api_id

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
        path_parameter_list = self.url.split("?")[0].split('/')[5:]
        for i in range(len(path_list)):
            if re.search(pattern, path_list[i]):
                key = path_list[i][1:-1]
                value = path_parameter_list[i]
                try:
                    value = int(value)
                except:
                    pass
                self.path_parameter[key] = value