import random
import numpy as np
from core.case_execution.case_test import fuzz

#####################      fuzz处理graph（x）位置的api      #######################
#  fuzzgraph(matr, tag, i, api_info_list, cov_url, Authorization)
def fuzzgraph(param_pool, success_pool, fuzz_pool, username, password, matr, tag, x, api_info_list, cov_url, Authorization, operation_mode,
              restart, length):
    api_info = api_info_list[x]
    if length == 0:
        optional = 0
        fuzz(param_pool, success_pool, fuzz_pool, username, password, optional, matr, tag, api_info, cov_url,
             Authorization, operation_mode, restart, length)
    else:
        optional = 1
        fuzz(param_pool, success_pool, fuzz_pool, username, password, optional, matr, tag, api_info, cov_url,
             Authorization, operation_mode, restart, length)

def topology_visit(param_pool, success_pool, fuzz_pool, username, password, matr, tag, rn_matrix, rn_end, rn_visited, n,
                   api_info_list, cov_url, Authorization, operation_mode, restart, length):
    # 第一个开始节点api是没有依赖的，其中需要的参数可通过fuzz来获取（也可人工赋值）
    g = eval(matr.lindex(str(rn_matrix),1))
    visited = eval(matr.lindex(str(rn_visited), 0))
    visited[n] = 1
    fuzzgraph(param_pool, success_pool, fuzz_pool, username, password, matr, tag, n, api_info_list, cov_url,
              Authorization, operation_mode, restart, length)
    matr.lpush(str(rn_visited), str(visited))
    matr.lpush(str(rn_matrix), str(g))
    matr.lpush(str(rn_matrix), n)

    while visited[n] == 1:
        # 创建遍历的存储队列
        dep_list = []
        for i in range(len(g)):
            if g[i][n] != -1:
                dep_list.append(i)
        if len(dep_list) == 0:
            break
        '''略过正常测试用例'''
        if len(dep_list) != 0:  # 说明queue里面所有api都无法test,并且资源池中也没有资源
            k = random.choice(dep_list)
            if visited[k] == 0:
                for a in dep_list:
                    g[a][n] = -1
                dep_list.clear()
                fuzzgraph(param_pool, success_pool, fuzz_pool, username, password, matr, tag, k, api_info_list, cov_url,
                          Authorization, operation_mode, restart, length)
                visited = eval(matr.lindex(str(rn_visited), 0))
                visited[k] = 1
                g[k] = eval(matr.lindex(str(rn_end), 0))
                n = k
                matr.lpush(str(rn_matrix), str(g))
                matr.lpush(str(rn_matrix), k)
                matr.lpush(str(rn_visited), str(visited))

def traversal(param_pool, success_pool, fuzz_pool, username, password, matr, tag, rn_matrix, api_info_lis, cov_url, Authorization, operation_mode, restart, length):

    graph = eval(str(matr.lindex(str(rn_matrix), 1)))
    api_info_list = api_info_lis

    # 设计出度为0的点
    rn_end = "end" + tag
    if matr.lindex(str(rn_end), 0) == None:
        end = []
        for i in range(len(graph)):
            end.append(-1)
        matr.lpush(str(rn_end), str(end))


    # 创建visited，用来停止遍历，即一旦遇到visited，即刻退出递归 #0代表没被访问
    rn_visited = "visited" + tag
    if matr.lindex(str(rn_visited), 0) == None:
        visited = np.zeros(len(graph)).astype(dtype=int).tolist()
        matr.lpush(str(rn_visited), str(visited))
    # print(visited)

    # 保留中间状态 出度为0的点 的list
    rn_out_degree_zero = "out_degree_zero" + tag
    if matr.lindex(str(rn_out_degree_zero), 0) == None:
        # 记录出度为0的点 收集出度为0的点的集合,即无依赖节点的集合
        out_degree_zero = []
        for j in range(len(graph)):
            if graph[j] == eval(matr.lindex(str(rn_end), 0)):
                out_degree_zero.append(j)
        matr.lpush(str(rn_out_degree_zero), str(out_degree_zero))

    out_degree_zero = eval(matr.lindex(str(rn_out_degree_zero), 0))
    for m in range(len(out_degree_zero)):
        k = random.choice(out_degree_zero)
        out_degree_zero.remove(k)
        matr.lpush(str(rn_out_degree_zero), str(out_degree_zero))
        print(k)
        topology_visit(param_pool, success_pool, fuzz_pool, username, password, matr, tag, rn_matrix, rn_end,
                       rn_visited, k, api_info_list, cov_url, Authorization, operation_mode, restart, length)




