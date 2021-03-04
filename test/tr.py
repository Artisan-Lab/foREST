import random

graph = [[-1,0,1,-1,-1,-1,-1],
         [-1,-1,-1,2,-1,-1,-1],
         [-1,3,-1,-1,4,-1,5],
         [-1,-1,-1,-1,-1,6,-1],
         [-1,-1,-1,7,-1,8,-1],
         [-1,-1,-1,-1,-1,-1,-1],
         [-1,-1,-1,-1,-1,-1,-1]]

# 记录拓扑排序顺序
topology_order = []
# 记录出度为0的点
out_degree_zero = []
# 记录已经访问的点
visited = []
# 设计出度为0的点
end = []
for i in range(0, len(graph)):
    end.append(-1)
# 收集出度为0的点的集合,即无依赖节点的集合
for j in range(0, len(graph)):
    if graph[j]==end:
        out_degree_zero.append(j)

# 拓扑，通过回溯insert到l中
def topology_visit(g, n):
    if n not in visited:
        visited.append(n)
    for m in range(0, len(g)):
        if g[m][n] != -1 and m not in visited:
            topology_visit(g, m)
    topology_order.insert(0, n)

# for n in out_degree_zero:
#     topology_visit(graph, n)

for m in range(len(out_degree_zero)):
    k = random.choice(out_degree_zero)
    out_degree_zero.remove(k)
    topology_visit(graph, k)

print(topology_order)

