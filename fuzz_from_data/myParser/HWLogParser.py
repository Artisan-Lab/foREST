import json

from fuzz_from_data.model.requestEntity import RequestEntity
from fuzz_from_data.myParser.logParser import LogParser
from urllib.parse import urlencode

BASE_URL = 'http://fuxi-pipeline-api-mutation.pipeline-beta.dev.titan.huawei.com'


class HWLogParser(LogParser):
    """
    log myParser for captured requests by huawei
    """

    def __init__(self, log_path):
        LogParser.__init__(self, log_path)
        self.content = []

    def read_logs(self):
        """
        read json
        """
        logs = self.log_path.split(',')
        for log_file_item in logs:
            print(f'reading log file: {log_file_item}')
            with open(log_file_item, encoding='UTF-8') as f:
                temp_list = []
                temp = json.load(f)
                item_list = temp['RECORDS']
                for item in item_list:
                    request_field = item['request']  # this is a string
                    request_obj = json.loads(request_field)[0]
                    headers = request_obj['headers']
                    param_map = request_obj['paramsMap'] # type: dict
                    tmp_map = {}
                    for k,v in param_map.items():
                        tmp_map[k] = v[0]
                    query_string = urlencode(tmp_map)
                    url = BASE_URL + request_obj['requestURI'] + "?" + query_string
                    method = request_obj['method']
                    body = request_obj['body']  # this is a string
                    adapter = {'headers': headers, 'method': method, 'url': url, 'body': body}
                    temp_list.append(adapter)
                self.content += temp_list

    def parse(self) -> list:
        """
        parse json data to our requestEntity
        """
        request_entity_list = []
        for item in self.content:
            request_entity_list.append(RequestEntity(item['method'], item['url'], item['headers'], item['body']))
        return request_entity_list

# myParser = HWLogParser(
#     'C:\\Users\\cwx1038422\\Desktop\\luffy_restapi_testcase_1.json,C:\\Users\\cwx1038422\\Desktop\\luffy_restapi_testcase_2.json,C:\\Users\\cwx1038422\\Desktop\\luffy_restapi_testcase_3.json')
# myParser.read_logs()
# a = myParser.parse()
# print(a)
