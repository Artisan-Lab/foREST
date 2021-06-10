import random
from configparser import ConfigParser

import numpy as np
from core.case_execution.process_test import test
from module.get_next_apis import get_next_apis
from core.case_generation.generate import case_generation
from dependec_matrix.graph2 import get_dep_info
from parse.parse import get_api_info
import os.path

import redis
from multiprocessing import Process

def wait_process():
    print("等待执行完成...")

if __name__ == '__main__':
    config = ConfigParser()
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../restfultest_config.ini")
    config.read(path, encoding='UTF-8')
    process_num = int(config.get("process_num", "process_num"))
    test_yaml = config.get('test_config', 'test_yaml')
    optional_params_execute_nums = int(config.get('test_config', 'optional_params_nums'))
    cov_url = config.get('coverage_config', 'cov_url')
    Authorization = config.get('Authorization', 'Authorization')
    username = config.get('Authorization', 'username')
    password = config.get('Authorization', 'password')
    fuzz_test_times = int(config.get('test_config', 'fuzz_test_times'))
    operation_mode = int(config.get('operation_mode', 'operation_mode'))
    run_time = eval(config.get('run_time', 'run_time'))
    restart = config.get('restart', 'restart')

    db_success = int(config.get('redis', 'db_success'))
    db_params = int(config.get('redis', 'db_params'))
    db_serial = int(config.get('redis', 'db_serial'))
    db_parallelism = int(config.get('redis', 'db_parallelism'))
    db_fuzz_pool = int(config.get('redis', 'db_fuzz_pool'))
    db_o = int(config.get('redis', 'db_o'))
    redis_host = config.get('redis', 'host')
    redis_port = config.get('redis', 'port')

    params_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_params, decode_responses=True)
    success_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_success, decode_responses=True)
    fuzz_pool = redis.StrictRedis(host=redis_host, port=redis_port, db=db_fuzz_pool, decode_responses=True)
    '''flag作用:保证一个进程只生成一遍模糊用例，即重启仅是重启测试，不会影响测试用例生成'''
    flag = redis.StrictRedis(host=redis_host, port=redis_port, db=db_o, decode_responses=True)
    if not flag.scard('over'):
        flag.sadd('over', 0)
    if operation_mode == 0:
        print("现在是串行测试！")
        db_select = db_serial
    else:
        print("现在是并行测试！")
        db_select = db_parallelism
    matr = redis.StrictRedis(host=redis_host, port=redis_port, db=db_select, decode_responses=True)

    ''' 主进程负责生成测试用例，根据可选参数个数，逐渐从k+0，k+1，k+2...进行用例生成和测试 '''
    for nums in range(optional_params_execute_nums):
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../openapi/%s" % test_yaml)
        api_info_list = get_api_info(1.0, path)
        matrix, weight_info_list = get_dep_info(api_info_list)
        print(matrix)
        graph = matrix.tolist()

        if matr.lindex("matrix", 1) == None:
            matr.lpush("matrix", str(graph))
            matr.lpush("matrix", "*")

        num = len(api_info_list)
        ma = np.zeros([num, num], dtype=int)
        m = np.ones([num, num], dtype=int)
        ma -= m
        maa = ma.tolist()

        # 此时是程序crash掉了
        if matr.lindex("matrix", 0) and eval(matr.lindex("matrix", 1)) != maa \
                and eval(matr.lindex("matrix", 1)) != graph:
            print("测试程序重启！")

        if matr.lindex("end", 0) == None:
            end = []
            for i in range(len(graph)):
                end.append(-1)
            matr.lpush("end", str(end))

        if matr.lindex("visited", 0) == None:
            visited = np.zeros(len(graph)).astype(dtype=int).tolist()
            matr.lpush("visited", str(visited))

        # if matr.lindex("out_degree_zero", 0) == None:
        #     # 记录出度为0的点 收集出度为0的点的集合,即无依赖节点的集合
        #     out_degree_zero = []
        #     for j in range(len(graph)):
        #         if graph[j] == eval(matr.lindex("end", 0)):
        #             out_degree_zero.append(j)
        #     matr.lpush("out_degree_zero", str(out_degree_zero))
        #
        # ''' 1.执行所有入度为0的点  list '''
        # out_degree_zeros = eval(matr.lindex("out_degree_zero", 0))
        #
        # '''生成测试用例'''
        # if flag.sismember('over', 0):
        #     for api_id in out_degree_zeros:
        #         if nums == 0:
        #             ''' 因为必选参数较少，生成测试用例可以尽可能多的包含fuzz的字典，不需太担心组合爆炸，故*5 '''
        #             for time in range(fuzz_test_times * 5):
        #                 case_generation().fuzz_generation(api_info_list[api_id], fuzz_pool)
        #         else:
        #             for time in range(fuzz_test_times):
        #                 case_generation().fuzz_optional_generation(api_info_list[api_id], fuzz_pool, nums)
        # flag.srem('over', 0)
        # flag.sadd('over', 1)
        #
        # ''' 2.分摊case，多进程进行测试 '''
        # if nums == 0:
        #     fuzz_cases = fuzz_pool.sscan(str(id))[1]
        # else:
        #     fuzz_cases = fuzz_pool.sscan(str(id) + 'optional')[1]
        #
        # '''其中一个要多加几个case'''
        # process = []
        # each_process_exc_case_num = len(fuzz_cases)/process_num
        # ll = len(fuzz_cases)%process_num
        # for i in range(process_num):
        #     p = Process(target=test, args=())
        #     process.append(p)
        # for i in range(process_num):
        #     process[i].start()
        # for i in range(process_num):
        #     process[i].join()

        while 0 in eval(matr.lindex("visited", 0)):
            next_apis = get_next_apis(matr)
            # next_api当前测试api的id
            next_api = random.choice(next_apis)
            '''生成测试用例'''
            if flag.sismember('over', 0):
                if nums == 0:
                    ''' 因为必选参数较少，生成测试用例可以尽可能多的包含fuzz的字典，不需太担心组合爆炸，故*5 '''
                    for time in range(fuzz_test_times * 5):
                        case_generation().fuzz_generation(api_info_list[next_api], fuzz_pool)
                else:
                    for time in range(fuzz_test_times):
                        case_generation().fuzz_optional_generation(api_info_list[next_api], fuzz_pool, nums)
            flag.srem('over', 0)
            flag.sadd('over', 1)

            if nums == 0:
                fuzz_cases = fuzz_pool.sscan(str(next_api))[1]
            else:
                fuzz_cases = fuzz_pool.sscan(str(next_api) + 'optional')[1]

            each_process_exc_case_num = len(fuzz_cases) / process_num-1

            process = []
            for i in range(process_num):
                p = Process(target=test, args=(each_process_exc_case_num,))
                process.append(p)
            for i in range(process_num):
                process[i].start()
            for i in range(process_num):
                process[i].join()

            print(f"测完第{next_api}个api,并发进程数是{process_num},当前可选参数个数为{nums}个")







































