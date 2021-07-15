import os
from parse import parse
from graph_test import CreateTree
from fuzz import FuzzAndJudgeUnit
from graph import GetDependency

class Render:

    def __init__(self, semantic_tree):
        self.semantic_tree = semantic_tree
        self.api_list = semantic_tree.api_list
        api_number = len(semantic_tree.api_list)
        self.visited_pool = [0 for x in range(0, api_number)]
        self.success_pool = [0 for x in range(0, api_number)]


    def render_fuzz(self):
        for semantic_tree_node in self.semantic_tree.semantic_tree.all_nodes():#深度优先搜索
            if semantic_tree_node.data.method:
                if semantic_tree_node.data.method:
                    pass


def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../openapi/sdms.yaml")
    api_list = parse.get_api_info(1, path)
    get_info_dependency = GetDependency(api_list)
    api_list = get_info_dependency.get_dependency()
    semantic_tree = CreateTree(api_list)
    semantic_tree.create_tree()
    for i in range(len(api_list)):
        for req_field_info in semantic_tree.api_list[i].resp_param:
            require_dictionary = {}
            require_dictionary[req_field_info.field_name] = FuzzAndJudgeUnit.fuzz_value(req_field_info)
            print(require_dictionary)

if __name__ == '__main__':
    main()