from dependency.keyvaluedependency import SetKeyValueDependency
from dependency.semantictree import CreateSemanticTree


def Dependency(open_api_list):
    semantic_tree = CreateSemanticTree(open_api_list)
    tree_root = semantic_tree.create_tree
    key_value_parser = SetKeyValueDependency(open_api_list)
    key_value_parser.get_dependency()
    return tree_root