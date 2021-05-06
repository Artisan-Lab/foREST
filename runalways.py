from core.case_execution.test import traversal,fuzzgraph
from dependec_matrix.graph2 import get_dep_info
from parse.parse import get_api_info
import os.path
from configparser import ConfigParser


def run(cov_url,k,test_yaml):
    while(1 == 1):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./openapi/%s" %test_yaml)
        api_info_list = get_api_info(1.0, path)
        matrix, weight_info_list = get_dep_info(api_info_list)
        print(matrix)
        graph = matrix.tolist()
        for conf_k in range(k):
            visited = traversal(graph, api_info_list, cov_url,conf_k)
            api = api_info_list
            # 未测试的单独fuzz
            print(visited)
            for i,v in enumerate(visited):
                if v == 0:
                    print(i)
                    print(api)
                    fuzzgraph(i, api,cov_url,conf_k)

config = ConfigParser()
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "./restfultest_config.ini")
config.read(path)

test_yaml = config.get("test_config", "test_yaml")
optional_params_execute_num = int(config.get("test_config", "optional_params_execute_num"))
cov_url = config.get("coverage_config", "cov_url")

run(cov_url,optional_params_execute_num,test_yaml)



