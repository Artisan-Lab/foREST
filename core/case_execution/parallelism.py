import numpy as np

from core.case_execution.topology_test import traversal,fuzzgraph
from core.case_generation.generate import case_generation
from dependec_matrix.graph2 import get_dep_info
from parse.parse import get_api_info
import os.path
import redis

def parallelism(i, cov_url, optional_params_nums, test_yaml, Authorization, fuzz_test_times, operation_mode):

    fuzz_pool = redis.StrictRedis(host='127.0.0.1', port=6379, db=7, decode_responses=True)
    '''flag作用:保证一个进程只生成一遍模糊用例，即重启仅是重启测试，不会影响测试用例生成'''
    flag = redis.StrictRedis(host='127.0.0.1', port=6379, db=0, decode_responses=True)
    if not flag.scard('over'):
        flag.sadd('over', 0)
    if operation_mode == 0:
        print("现在是串行测试！")
        db_select = 5
    else:
        print("现在是并行测试！")
        db_select = 9
    tag = str(i)
    matr = redis.StrictRedis(host='127.0.0.1', port=6379, db=db_select, decode_responses=True)

    while True:
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../openapi/%s" %test_yaml)
        api_info_list = get_api_info(1.0, path)
        matrix, weight_info_list = get_dep_info(api_info_list)
        print(matrix)
        graph = matrix.tolist()
        # rn_matrix: 唯一标识当前进程单独在redis中存储对应的内容，保证多进程时，每个进程有自己独立的redis存储对应中间信息
        rn_matrix = "matrix" + tag
        if matr.lindex(str(rn_matrix), 1) == None:
            print(1)
            matr.lpush(str(rn_matrix), str(graph))
            matr.lpush(str(rn_matrix), "*")

        num = len(api_info_list)
        ma = np.zeros([num, num], dtype=int)
        m = np.ones([num, num], dtype=int)
        ma -= m
        maa = ma.tolist()

        # 此时是程序crash掉了
        if matr.lindex(str(rn_matrix), 0) and eval(matr.lindex(str(rn_matrix), 1)) != maa \
                and eval(matr.lindex(str(rn_matrix), 1)) != graph:
            print("测试程序重启！")

        '''生成测试用例'''
        if flag.sismember('over', 0):
            for api_info in api_info_list:
                for i in range(fuzz_test_times):
                    case_generation().fuzz_generation(api_info, fuzz_pool)
                    case_generation().fuzz_optional_generation(api_info, fuzz_pool, optional_params_nums)
        flag.srem('over', 0)
        flag.sadd('over', 1)

        '''开始测试'''
        traversal(matr, tag, rn_matrix, api_info_list, cov_url, Authorization, fuzz_test_times, operation_mode)

        # 未测试的单独fuzz
        rn_visited = "visited" + tag
        visited = eval(matr.lindex(str(rn_visited), 0))
        print(visited)
        for i, v in enumerate(visited):
            if v == 0:
                print(i)
                fuzzgraph(matr, tag, i, api_info_list, cov_url, Authorization, fuzz_test_times, operation_mode)



