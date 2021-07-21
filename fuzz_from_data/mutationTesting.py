import io
import json
import os
import re
import sys
import traceback
import urllib

import requests as http_requests

from fuzz_from_data.commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from fuzz_from_data.commons.utils import Utils
from fuzz_from_data.model.requestEntity import RequestEntity
from fuzz_from_data.mutation.binaryMutation import BinaryMutation
from fuzz_from_data.mutation.jsonMutation import JsonMutation
from fuzz_from_data.mutation.jsonTree.tree import Tree
from fuzz_from_data.mutation.queryStringMutation import QueryStringMutation
from fuzz_from_data.mutation.randomMutation import RandomMutation
from fuzz_from_data.myParser.myParserFactory import MyParserFactory

os.environ['http_proxy'] = ''
os.environ['https_proxy'] = ''
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')

QUERY_STRING_PATTERN = r'[^(=|&)]+='


def mutate_a_request(request: RequestEntity):
    """
    mutate a request
    """
    request_to_be_mutated = request.clone()
    try:
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
    except Exception as e:
        print(traceback.format_exc())
    finally:
        return request_to_be_mutated


def get_mutated_requests(requests):
    """
    mutate these requests from log
    """

    ret = []
    iteration_num = 1
    for request in requests:  # type: RequestEntity
        ret.append(mutate_a_request(request))
        iteration_num += 1
    return ret


def main():
    """
    execute mutation testing
    """
    log_parser = MyParserFactory.product_parser(FUZZ_FROM_DATA_CONFIG.log_parser_name)
    log_parser.read_logs()
    requests = log_parser.parse()
    iteration_num = 1
    status_code_5xx_num = 0
    status_code_2xx_num = 0
    status_code_4xx_num = 0
    status_code_all = 0
    SUCCESS_num = 0
    FAILED_num = 0

    while True:
        try:
            print("mutation phase start...")
            mutated_requests = get_mutated_requests(requests)
            print("mutation phase finished,and execution phase start...")
            for i in range(len(mutated_requests)):
                try:
                    print(
                        f"executing {i + 1}/{len(mutated_requests)}/{iteration_num}, status_code_2xx_5xx_all {status_code_2xx_num}/{status_code_5xx_num}/{status_code_all}")
                    print(f'success_failed {SUCCESS_num}/{FAILED_num}')
                    request = mutated_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    request.headers.pop("x-forwarded-host", None)
                    request.headers.pop("host", None)
                    if request.files is not None:
                        print("sending file")
                        response = http_requests.post(request.url, files=request.files)
                    else:
                        response = http_requests.request(method=request.method,
                                                         url=request.url,
                                                         data=str(request.body).encode(),
                                                         headers=request.headers)
                    print(response.text)
                    if 500 <= response.status_code <= 599:
                        status_code_5xx_num += 1
                        f = open("bugsLog/mutation_testing_5xx.log", "a")
                        f.write(request.__str__())
                        f.close()
                        print("Server error,please check the log!")
                    elif 200 <= response.status_code <= 299:
                        status_code_2xx_num += 1
                        # parse response message
                        msg = json.loads(response.text)
                        if msg['status'] == 'FAILED':
                            FAILED_num += 1
                        if msg['status'] == 'SUCCESS':
                            SUCCESS_num += 1

                    elif 400 <= response.status_code <= 499:
                        status_code_4xx_num += 1
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
