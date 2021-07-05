import random
import re
import traceback

import requests as http_requests

import sequence
from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from commons.utils import Utils
from jsonMutation import JsonMutation
from model.requestEntity import RequestEntity
from parser.apacheLogParser import ApacheLogParser
from parser.proxyLogParser import ProxyLogParser
from queryStringMutation import QueryStringMutation
from tree import Tree

QUERY_STRING_PATTERN = r'[^(=|&)]+='


def get_mutated_requests(requests):
    """
    mutate these requests from log
    """
    ret = []
    iteration_num = 1
    for request in requests:  # type: RequestEntity
        print(
            f"================================mutation phrase,process {iteration_num}/{len(requests)}========================================")
        if len(request.body) > 0:
            print(
                f'{request.method} {request.url} mutating ....')
        if Utils.is_json(request.body):
            request_to_be_mutated = request.clone()
            print(request.body)
            tree = Tree(request_to_be_mutated.body)
            # tree.export_img("original.png")
            tree.print()
            print('muating value!')
            JsonMutation.mutate_value(tree)
            tree.print()
            JsonMutation.drop(tree)
            tree.print()
            JsonMutation.select(tree)
            tree.print()
            JsonMutation.duplicate(tree)
            tree.print()
            request_to_be_mutated.body = tree.dump()
            print(f'mutated body:{request_to_be_mutated.body}')
            sequence.Sequence.seq_num = 0
            ret.append(request_to_be_mutated)
            # tree.export_img("mutated.png")


        elif re.match(QUERY_STRING_PATTERN, request.body) and 'WebKitFormBoundary' not in request.body:
            print('QUERY_STRING MUTATING')
            request_to_be_mutated = request.clone()
            print(
                f'{request_to_be_mutated.method} {request_to_be_mutated.url} mutating {request_to_be_mutated.body}....')
            query_string_mutation = QueryStringMutation(request.body)
            query_string_mutation.mutate_value()
            if 0 == random.randint(0, 1):
                query_string_mutation.select()
            else:
                query_string_mutation.drop()
            request_to_be_mutated.body = query_string_mutation.dump()
            print(f'mutated body:{request_to_be_mutated.body}')
            ret.append(request_to_be_mutated)
        elif 'WebKitFormBoundary' in request.body:
            request_to_be_mutated = request.clone()
            import os
            with open('random.png', 'wb') as fout:
                fout.write(os.urandom(1024))  # replace 1024 with size_kb if not unreasonably large
            request_to_be_mutated.files = {'file': open('random.png', 'rb')}
            ret.append(request_to_be_mutated)

        elif len(request.body) > 0:
            request_to_be_mutated = request.clone()
            print(
                f'{request_to_be_mutated.method} {request_to_be_mutated.url} mutating {request_to_be_mutated.body}....')
            # TODO: here code is awful
            request_to_be_mutated.body = ''.join(
                i if random.randint(0, 1) else '\\' for i in request_to_be_mutated.body)
            print(f'mutated body:{request_to_be_mutated.body}')
            ret.append(request_to_be_mutated)
        iteration_num += 1
    return ret


def get_requests_from_apache_log(log_src):
    """
    requests parsed from apache error.log
    """
    log_parser = ApacheLogParser(log_src)
    log_parser.read_logs()
    return log_parser.parse()


def get_requests_from_proxy_log(log_src):
    """
        requests parsed from proxy.log
        """
    log_parser = ProxyLogParser(log_src)
    log_parser.read_logs()
    return log_parser.parse()


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
            print("mutation phrase start...")
            # requests = get_requests_from_apache_log(FUZZ_FROM_DATA_CONFIG.log_path)
            requests = get_requests_from_proxy_log(
                ['/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625407119.9178529-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625407979.8544893-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625408541.4782267-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409134.9770634-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409454.4674275-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625409738.8814836-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625410012.0339994-log.json',
                 '/home/yang/PycharmProjects/Restful-api-testing/fuzz_from_data/capture/1625410369.94529-log.json'])
            mutated_requests = get_mutated_requests(requests)
            print("mutation phrase finished,and execution phrase start...")
            # total_requests = requests + mutated_requests
            total_requests = mutated_requests
            for i in range(len(total_requests)):
                try:
                    print(
                        f"executing {i + 1}/{len(total_requests)}/{iteration_num}, status_code_2xx_5xx_all {status_code_2xx_num}/{status_code_5xx_num}/{status_code_all}")
                    request = total_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)

                    if request.files is not None:
                        response = http_requests.post(request.url, files=request.files)
                        print("send file!!!!")
                    else:
                        response = http_requests.request(method=request.method,
                                                         # url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                         url=request.url,
                                                         data=request.body,
                                                         headers=request.headers)
                    print(response)
                    if 500 <= response.status_code <= 599:
                        status_code_5xx_num += 1
                        f = open("mutation_testing_5xx.log", "a")
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
            print("execution phrase finished. next iteration start...")

            # debug
            # total_requests = mutated_requests
            # for i in range(len(total_requests)):
            #     try:
            #         print(
            #             "===================================================exec mutation=======================================")
            #         print(f"executing {i + 1}/{len(total_requests)}/{iteration_num}")
            #         request = total_requests[i]  # type: RequestEntity
            #         if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
            #             print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
            #             request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
            #         print(request)
            #         response = http_requests.request(method=request.method,
            #                                          url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
            #                                          data=request.body,
            #                                          headers=request.headers)
            #         print(response)
            #         if response.status_code == 503:
            #             print("Server error,please check the log!")
            #         print('\n\n\n')
            #     except Exception as e:
            #         print(e)
            #         pass
            # print("execution phrase finished. next iteration start...")



        except Exception as e:
            print(traceback.format_exc())
        finally:
            iteration_num += 1


if __name__ == "__main__":
    main()
