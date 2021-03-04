import random

from module.dep_analysis import get_dep_info
from module.parse import parse
import os.path

# my_path = os.path.abspath(os.path.dirname(__file__))
# api_info_list = parse(os.path.join(my_path, "../openapi/project.yaml"), 1.0)
# matrix, weight_info_list = get_dep_info(api_info_list)
# graph = matrix.tolist()
# for n in range(len(graph)):
#     for m in range(len(graph)):
#         if graph[n][m] !=-1 and graph[m][n] != -1:
#             list = [graph[n][m], graph[m][n]]
#             k = random.choice(list)
#             if graph[n][m] == k:
#                 graph[n][m] = -1
#             else:
#                 graph[m][n] = -1


# 记录拓扑排序顺序
topology_order = []
# 记录出度为0的点
out_degree_zero = []
# 记录已经访问的点
visited = []
# 设计出度为0的点
end = []

# 拓扑，通过回溯insert到l中
def topology_visit(g, n):
    if n not in visited:
        visited.append(n)
    for m in range(len(g)):
        if g[m][n] != -1 and m not in visited:
            topology_visit(g, m)
    topology_order.insert(0, n)


def traversal(graph):
    for i in range(len(graph)):
        end.append(-1)
    # 收集出度为0的点的集合,即无依赖节点的集合
    for j in range(len(graph)):
        if graph[j] == end:
            out_degree_zero.append(j)

    for m in range(len(out_degree_zero)):
        k = random.choice(out_degree_zero)
        out_degree_zero.remove(k)
        topology_visit(graph, k)

    return topology_order


# print(traversal(graph))