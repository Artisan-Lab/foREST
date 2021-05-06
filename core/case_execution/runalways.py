from core.case_execution.test import traversal,fuzzgraph
from dependec_matrix.graph2 import get_dep_info
from parse.parse import get_api_info
import os.path


def run(cov_url,k):
    while(1 == 1):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../openapi/wordpress.yaml")
        api_info_list = get_api_info(1.0, path)
        matrix, weight_info_list = get_dep_info(api_info_list)
        print(matrix)
        graph = matrix.tolist()
        for i in range(k):
            visited = traversal(graph, api_info_list, cov_url,i)
            api = api_info_list
            # 未测试的单独fuzz
            print(visited)
            for i,v in enumerate(visited):
                if v == 0:
                    print(i)
                    print(api)
                    fuzzgraph(i, api)

run('http://10.177.74.168:8000/',10)



