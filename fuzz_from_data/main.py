from model.requestEntity import RequestEntity
from mutation import Mutation
from parser.apacheLogParser import ApacheLogParser
from tree import *


def get_mutated_requests_from_log(log_src):
    """
    API for other module
    """
    log_parser = ApacheLogParser(log_src)
    log_parser.read_logs()
    requests = log_parser.parse()
    for request in requests:  # type: RequestEntity
        if Utils.is_json(request.body):
            tree = Tree(request.body)
            tree.print()
            Mutation.drop(tree)
            tree.print()
            Mutation.select(tree)
            tree.print()
            Mutation.two_nodes_manipulated_using_random(tree)
            Mutation.duplicate(tree)
            request.body = tree.dump()
    return requests


def main():
    """
    main function
    """
    log_parser = ApacheLogParser("/home/yang/error.log")
    log_parser.read_logs()
    requests = log_parser.parse()
    for request in requests:  # type: RequestEntity
        if Utils.is_json(request.body):
            tree = Tree(request.body)
            tree.export_img("output/original_tree.png")
            tree.print()
            Mutation.drop(tree)
            tree.export_img("output/dropped_tree.png")
            tree.print()
            Mutation.select(tree)
            tree.export_img("output/selected_tree.png")
            tree.print()
            Mutation.two_nodes_manipulated_using_random(tree)
            Mutation.duplicate(tree)
            tree.export_img("output/duplicated_tree.png")
            request.body = tree.dump()

    print(requests)


if __name__ == "__main__":
    main()
