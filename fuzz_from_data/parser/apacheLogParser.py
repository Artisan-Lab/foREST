import codecs
import re

from model.requestEntity import RequestEntity
from parser.logParser import LogParser

FRAGMENT_LENGTH_PATTERN = r'[0-9]+\sbytes$'
REQUEST_1ST_LINE_PATTERN = r'(GET|POST|PUT|PATCH).*HTTP/(1\.1|2\.0)'
RESPONSE_1ST_LINE_PATTERN = r'HTTP/(1\.1|2\.0)\s[0-9]{3}'
HEADER_PATTERN = r'([-]|[A-Z]|[a-z])+:\s[^\s]'
# use for replace '\\r\\n' in message fragment
NEXT_LINE_PATTERN = r'(\\r\\n)+'


class ApacheLogParser(LogParser):
    """
    log parser for apache server
    """

    def __init__(self, log_path):
        LogParser.__init__(self, log_path)
        self.token = "(data-HEAP):"

    def pretty_print(self):
        """
        print the extract message
        """
        message = ''
        for line in self.content:
            if self.token in line:
                http_message_fragment = line[line.rfind(self.token) + len(self.token):].strip()
                if not re.match(FRAGMENT_LENGTH_PATTERN, http_message_fragment):
                    message += http_message_fragment
        message = codecs.decode(message, "unicode_escape")
        print(message)

    def parse(self) -> list:
        """
        parse apache log file
        """
        # ignore response message
        request_flag = False
        request_headers = {}
        request_body = ''
        request_entity_list = []

        for line in self.content:
            if self.token in line:
                http_message_fragment = line[line.rfind(self.token) + len(self.token):].strip()
                # ignore bytes length info. e.g. 40 bytes
                if not re.match(FRAGMENT_LENGTH_PATTERN, http_message_fragment):
                    http_message_fragment = re.sub(NEXT_LINE_PATTERN, "", http_message_fragment)
                    if request_flag and re.match(RESPONSE_1ST_LINE_PATTERN, http_message_fragment):
                        request_entity = RequestEntity(request_method, request_url, request_headers, request_body)
                        request_entity_list.append(request_entity)
                        request_entity, request_flag, request_headers, request_body = None, False, {}, ''
                        request_flag = False
                        continue

                    # request first line . e.g GET / HTTP/1.1
                    elif re.match(REQUEST_1ST_LINE_PATTERN, http_message_fragment):
                        request_flag = True
                        first_line_arr = http_message_fragment.split()
                        request_method = first_line_arr[0]
                        request_url = first_line_arr[1]

                    # header.  e.g User-Agent: Firefox
                    elif request_flag and re.match(HEADER_PATTERN, http_message_fragment):
                        splitted_header_arr = http_message_fragment.split(": ")
                        request_headers[splitted_header_arr[0]] = splitted_header_arr[1]

                    # request body part
                    elif request_flag:
                        request_body += http_message_fragment
        return request_entity_list
