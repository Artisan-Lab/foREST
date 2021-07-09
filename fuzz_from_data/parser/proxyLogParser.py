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
        """
        read json
        """
        logs = self.log_path.split(',')
        for item in logs:
            print(f'reading log file: {item}')
            f = open(item, )
            self.content += json.load(f)
            f.close()

    def parse(self) -> list:
        """
        parse json data to our requestEntity
        """
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
