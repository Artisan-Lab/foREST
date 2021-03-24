from module.Fuzz_value import traversal,fuzzgraph
from module.dep_analysis import get_dep_info
from module.parse import parse
import os.path


# 获取依赖测试graph
# my_path = os.path.abspath(os.path.dirname(__file__))
# api_info_list = parse(1.0)
# matrix, weight_info_list = get_dep_info(api_info_list)
# graph = matrix.tolist()

# # g_list用来看遍历情况
# g_list = []
# for i in range(len(graph)):
#     g_list.append(0)

def run():
    while(1 == 1):
        my_path = os.path.abspath(os.path.dirname(__file__))
        api_info_list = parse(1.0)
        matrix, weight_info_list = get_dep_info(api_info_list)
        print(matrix)
        graph = matrix.tolist()
        # print(graph)
        # print(len(graph))
        # num = 0
        # listt = traversal(graph)
        # for i in range(len(graph)):
        #     g_list[i] = g_list[i] + listt[i]
        # for i in range(len(graph)):
        #     if g_list[i] == 0:
        #         num = num +1
        # print(num)
        visited = traversal(graph, api_info_list)
        api = api_info_list
        # 未测试的单独fuzz
        print(visited)
        for i,v in enumerate(visited):
            if v == 0:
                print(i)
                print(api)
                fuzzgraph(i, api)

run()