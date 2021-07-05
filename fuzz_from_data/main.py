import random
import re

import requests as http_requests

import sequence
from commons.fuzzFromDataConfig import FUZZ_FROM_DATA_CONFIG
from commons.utils import Utils
from jsonMutation import JsonMutation
from model.requestEntity import RequestEntity
from parser.apacheLogParser import ApacheLogParser
from queryStringMutation import QueryStringMutation
from tree import Tree

QUERY_STRING_PATTERN = r'[^(=|&)]+=[^(=|&)]&[^(=|&)]+=[^(=|&)]'


def get_mutated_requests(requests):
    """
    mutate these requests from log
    """
    ret = []
    iteration_num = 1
    for request in requests:  # type: RequestEntity
        print(
            f"================================mutation phrase,process {iteration_num}/{len(requests)}========================================")
        if Utils.is_json(request.body):
            request_to_be_mutated = request.clone()
            print(
                f'{request_to_be_mutated.method} {request_to_be_mutated.url} mutating {request_to_be_mutated.body}....')
            tree = Tree(request_to_be_mutated.body)
            tree.print()
            JsonMutation.drop(tree)
            tree.print()
            JsonMutation.select(tree)
            tree.print()
            JsonMutation.duplicate(tree)
            request_to_be_mutated.body = tree.dump()
            print(f'mutated body:{request_to_be_mutated.body}')
            sequence.Sequence.seq_num = 0
            ret.append(request_to_be_mutated)
        elif re.match(QUERY_STRING_PATTERN, request.body):
            request_to_be_mutated = request.clone()
            print(
                f'{request_to_be_mutated.method} {request_to_be_mutated.url} mutating {request_to_be_mutated.body}....')
            query_string_mutation = QueryStringMutation(request.body)
            if 0 == random.randint(0, 1):
                query_string_mutation.select()
            else:
                query_string_mutation.drop()
            request_to_be_mutated.body = query_string_mutation.dump()
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


def main():
    """
    main function
    """
    # log_parser = ApacheLogParser("/home/yang/error.log")
    # log_parser.read_logs()
    # requests = log_parser.parse()
    # for request in requests:  # type: RequestEntity
    #     if Utils.is_json(request.body):
    #         tree = Tree(request.body)
    #         tree.export_img("output/original_tree.png")
    #         tree.print()
    #         Mutation.drop(tree)
    #         tree.export_img("output/dropped_tree.png")
    #         tree.print()
    #         Mutation.select(tree)
    #         tree.export_img("output/selected_tree.png")
    #         tree.print()
    #         Mutation.two_nodes_manipulated_using_random(tree)
    #         Mutation.duplicate(tree)
    #         tree.export_img("output/duplicated_tree.png")
    #         request.body = tree.dump()
    # print(requests)

    requests = get_requests_from_apache_log(FUZZ_FROM_DATA_CONFIG.log_path)
    iteration_num = 1
    while True:
        try:
            print("mutation phrase start...")
            mutated_requests = get_mutated_requests(requests)
            print("mutation phrase finished,and execution phrase start...")
            total_requests = requests + mutated_requests
            for i in range(len(total_requests)):
                try:
                    print(f"executing {i + 1}/{len(total_requests)}/{iteration_num}")
                    request = total_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    response = http_requests.request(method=request.method,
                                                     url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                     data=request.body,
                                                     headers=request.headers)
                    print(response)
                    if response.status_code == 503:
                        print("Server error,please check the log!")
                    print('\n\n\n')
                except Exception as e:
                    print(e)
                    pass
            print("execution phrase finished. next iteration start...")

            # debug
            total_requests = mutated_requests
            for i in range(len(total_requests)):
                try:
                    print(
                        "===================================================exec mutation=======================================")
                    print(f"executing {i + 1}/{len(total_requests)}/{iteration_num}")
                    request = total_requests[i]  # type: RequestEntity
                    if len(FUZZ_FROM_DATA_CONFIG.cookie) > 0:
                        print(f"using cookie {FUZZ_FROM_DATA_CONFIG.cookie}")
                        request.headers['Cookie'] = FUZZ_FROM_DATA_CONFIG.cookie
                    print(request)
                    response = http_requests.request(method=request.method,
                                                     url=FUZZ_FROM_DATA_CONFIG.base_url + request.url,
                                                     data=request.body,
                                                     headers=request.headers)
                    print(response)
                    if response.status_code == 503:
                        print("Server error,please check the log!")
                    print('\n\n\n')
                except Exception as e:
                    print(e)
                    pass
            print("execution phrase finished. next iteration start...")



        except Exception as e:
            print(e)
            pass
        finally:
            iteration_num += 1


if __name__ == "__main__":
    main()
