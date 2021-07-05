import json

from model.requestEntity import RequestEntity
from parser.logParser import LogParser

EXCLUDE_DOMAIN = 'gravatar.com'


class ProxyLogParser(LogParser):
    """
    log parser for captured requests by proxy
    """

    def __init__(self, log_path):
        LogParser.__init__(self, log_path)

    def read_logs(self):
        # Opening JSON file
        if isinstance(self.log_path, str):
            f = open(self.log_path, )
            self.content = json.load(f)
            f.close()
        elif isinstance(self.log_path, list):
            for item in self.log_path:
                f = open(item, )
                self.content += json.load(f)
                f.close()

    def parse(self) -> list:
        request_entity_list = []
        for item in self.content:
            if EXCLUDE_DOMAIN in item['url']:
                continue
            request_entity_list.append(RequestEntity(item['method'], item['url'], item['headers'], item['body']))
        return request_entity_list

# parser = ProxyLogParser(
#     '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625410012.0339994-log.json')
#
# parser.read_logs()
# a = parser.parse()
# print(a)
