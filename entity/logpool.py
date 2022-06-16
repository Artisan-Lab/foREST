from entity.logEntity import LogEntity


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

    def __init__(self):
        self.log_id = 0
        self.log_list = []
        self.user_dict = {}

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
            if self.user_dict.get(log.user_id):
                self.user_dict[log.user_id].append(log)
            else:
                self.user_dict[log.user_id] = [log]



log_pool = LogPool()


