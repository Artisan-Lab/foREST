from module.Fuzz_value import traversal,fuzzgraph
from module.dep_analysis import get_dep_info
from module.parse import parse
import os.path


# 获取依赖测试graph
my_path = os.path.abspath(os.path.dirname(__file__))
api_info_list = parse(os.path.join(my_path, "../openapi/openapi.yaml"), 1.0)
matrix, weight_info_list = get_dep_info(api_info_list)
graph = matrix.tolist()

# # g_list用来看遍历情况
# g_list = []
# for i in range(len(graph)):
#     g_list.append(0)

def run():
    while(1 == 1):
        # num = 0
        # listt = traversal(graph)
        # for i in range(len(graph)):
        #     g_list[i] = g_list[i] + listt[i]
        # for i in range(len(graph)):
        #     if g_list[i] == 0:
        #         num = num +1
        # print(num)
        visited = traversal(graph)
        # 未测试的单独fuzz
        for i,v in enumerate(visited):
            if v == 0:
                fuzzgraph(i)

run()