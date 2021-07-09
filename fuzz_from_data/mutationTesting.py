import re
import traceback
import urllib

import requests as http_requests

from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from commons.utils import Utils
from model.requestEntity import RequestEntity
from mutation.binaryMutation import BinaryMutation
from mutation.jsonMutation import JsonMutation
from mutation.jsonTree.tree import Tree
from mutation.queryStringMutation import QueryStringMutation
from mutation.randomMutation import RandomMutation
from parser.apacheLogParser import ApacheLogParser
from parser.proxyLogParser import ProxyLogParser

QUERY_STRING_PATTERN = r'[^(=|&)]+='


def get_mutated_requests(requests):
    """
    mutate these requests from log
    """
    ret = []
    iteration_num = 1
    for request in requests:  # type: RequestEntity
        print(
            f"================================mutation phase,processing {iteration_num}/{len(requests)}========================================")
        # body mutation
        request_to_be_mutated = request.clone()
        print(f"mutating {request_to_be_mutated.__str__()}")
        if len(request_to_be_mutated.body) > 0:
            # json
            if Utils.is_json(request_to_be_mutated.body):
                mutation = JsonMutation(Tree(request_to_be_mutated.body))
            # query string
            elif re.match(QUERY_STRING_PATTERN, request_to_be_mutated.body) \
                    and 'WebKitFormBoundary' not in request_to_be_mutated.body:
                mutation = QueryStringMutation(request_to_be_mutated.body)
            # file or picture
            elif 'WebKitFormBoundary' in request_to_be_mutated.body:
                mutation = BinaryMutation()
            else:
                mutation = RandomMutation(request_to_be_mutated.body)

            mutation.start()
            request_to_be_mutated.body = mutation.result()


        elif "?" in request.url and "=" in request.url:
            query_string = urllib.parse.urlparse(request.url).query
            query_string_mutation = QueryStringMutation(query_string)
            query_string_mutation.start()
            request_to_be_mutated.url = request.url.split("?")[0] + "?" + query_string_mutation.result()
        ret.append(request_to_be_mutated)
        print(f"mutated result: {request_to_be_mutated.__str__()}")
        iteration_num += 1
    return ret


def get_requests_from_apache_log(log_src):
    """
    return an apache log parser
    """
    return ApacheLogParser(log_src)


def get_proxy_log_parser(log_src):
    """
    return a proxy log parser
    """
    return ProxyLogParser(log_src)


def main():
    """
    main function
    """
    iteration_num = 1
    status_code_5xx_num = 0
    status_code_2xx_num = 0
    status_code_all = 0
    while True:
        try:
            print("mutation phase start...")
            log_parser = get_proxy_log_parser(FUZZ_FROM_DATA_CONFIG.log_path)
            log_parser.read_logs()
            requests = log_parser.parse()
            mutated_requests = get_mutated_requests(requests)
            print("mutation phase finished,and execution phase start...")
            for i in range(len(mutated_requests)):
                try:
                    print(
                        f"executing {i + 1}/{len(mutated_requests)}/{iteration_num}, status_code_2xx_5xx_all {status_code_2xx_num}/{status_code_5xx_num}/{status_code_all}")
                    request = mutated_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)

                    if request.files is not None:
                        print("send file!!!!")
                        response = http_requests.post(request.url, files=request.files)
                    else:
                        response = http_requests.request(method=request.method,
                                                         url=request.url,
                                                         data=request.body,
                                                         headers=request.headers)
                    print(response)
                    if 500 <= response.status_code <= 599:
                        status_code_5xx_num += 1
                        f = open("bugsLog/mutation_testing_5xx.log", "a")
                        f.write(request.__str__())
                        f.close()
                        print("Server error,please check the log!")
                    elif 200 <= response.status_code <= 299:
                        status_code_2xx_num += 1
                    print('\n\n\n')
                except Exception as e:
                    print(traceback.format_exc())
                finally:
                    status_code_all += 1
            print("execution phase finished. next iteration start...")
        except Exception as e:
            print(traceback.format_exc())
        finally:
            iteration_num += 1


if __name__ == "__main__":
    main()
