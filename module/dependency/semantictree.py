from anytree import NodeMixin, RenderTree
import os
from module.utils.string_march import StringMatch
from module.utils.utils import Tool
from module.parser.open_api_parse.api_parser import APIList
from entity.resource_pool import foREST_POST_resource_pool
import nltk




def main():
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), Tool.read_config('api_file', 'file_path'))
    api_parser = APIList(path)
    api_list = api_parser.APIList()
    tree = CreateSemanticTree(api_list)
    root = tree.create_tree


if __name__ == '__main__':
    main()
