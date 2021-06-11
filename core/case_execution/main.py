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


        while 0 in eval(matr.lindex("visited", 0)):
            next_apis = get_next_apis(matr)
            # next_api当前测试api的id
            next_api = random.choice(next_apis)
            print(next_api)
            api_info = api_info_list[next_api]
            '''生成测试用例'''
            if flag.sismember('over', 0):
                if nums == 0:
                    ''' 因为必选参数较少，生成测试用例可以尽可能多的包含fuzz的字典，不需太担心组合爆炸，故*5 '''
                    for time in range(fuzz_test_times * 10):
                        case_generation().fuzz_generation(api_info_list[next_api], fuzz_pool, params_pool)
                else:
                    for time in range(fuzz_test_times):
                        case_generation().fuzz_optional_generation(api_info_list[next_api], fuzz_pool, nums, params_pool)
            flag.srem('over', 0)
            flag.sadd('over', 1)
            print(f"第{next_api}个api的测试用例生成完成，可选参数有{nums}个")

            ''' 分别将测试用例划分给不同的进程 '''
            if nums == 0:
                fuzz_cases = fuzz_pool.sscan(str(next_api + 1))[1]
            else:
                fuzz_cases = fuzz_pool.sscan(str(next_api + 1) + 'optional')[1]

            print(f"fuzz_cases的总长度是{int(len(fuzz_cases))},fuzz_cases是{fuzz_cases}")
            each_process_exc_case_num = int(len(fuzz_cases) / (process_num - 1))
            print(f"每一个进程测试的case个数为{each_process_exc_case_num}")

            all_cases = []
            cases = []
            if fuzz_cases == ['{}']:
                pass
            else:
                if each_process_exc_case_num == 0:
                    if nums == 0:
                        print(list(fuzz_pool.smembers(str(next_api + 1))))
                        for j in list(fuzz_pool.smembers(str(next_api + 1))):
                            cases.append(j)
                            fuzz_pool.srem(str(next_api + 1), j)
                            c = str(cases)
                            all_cases.append(c)
                            cases.clear()
                    else:
                        for j in list(fuzz_pool.smembers(str(next_api + 1) + 'optional')):
                            cases.append(j)
                            fuzz_pool.srem(str(next_api + 1) + 'optional', j)
                            c = str(cases)
                            all_cases.append(c)
                            cases.clear()
                elif each_process_exc_case_num == 1 and (process_num - 1) == int(len(fuzz_cases)):
                    if nums == 0:
                        print(list(fuzz_pool.smembers(str(next_api + 1))))
                        for j in list(fuzz_pool.smembers(str(next_api + 1))):
                            cases.append(j)
                            fuzz_pool.srem(str(next_api + 1), j)
                            c = str(cases)
                            all_cases.append(c)
                            cases.clear()
                    else:
                        for j in list(fuzz_pool.smembers(str(next_api + 1) + 'optional')):
                            cases.append(j)
                            fuzz_pool.srem(str(next_api + 1) + 'optional', j)
                            c = str(cases)
                            all_cases.append(c)
                            cases.clear()
                else:
                    for c in range(process_num):
                        if nums == 0:
                            if c != (process_num-1):
                                for i in range(each_process_exc_case_num):
                                    if fuzz_pool.scard(str(next_api + 1)) < each_process_exc_case_num and fuzz_pool.scard(str(next_api + 1)) != 0:
                                        for j in list(fuzz_pool.smembers(str(next_api + 1))):
                                            print(f"每个测试的用例有{j}")
                                            cases.append(j)
                                            fuzz_pool.srem(str(next_api + 1), j)
                                        cc = str(cases)
                                        all_cases.append(cases)
                                        cases.clear()
                                    elif fuzz_pool.scard(str(next_api + 1)) != 0:
                                        print(f"每个测试的用例有{fuzz_pool.sscan(str(next_api + 1))[1][0]}")
                                        cases.append(fuzz_pool.sscan(str(next_api + 1))[1][0])
                                        fuzz_pool.srem(str(next_api + 1), fuzz_pool.sscan(str(next_api + 1))[1][0])

                                c = str(cases)
                                all_cases.append(c)
                                cases.clear()
                                if fuzz_pool.scard(str(next_api + 1)) == 0:
                                    break
                            else:
                                for m in list(fuzz_pool.smembers(str(next_api + 1))):
                                    print(f"每个测试的用例有{m}")
                                    cases.append(m)
                                    fuzz_pool.srem(str(next_api + 1), m)
                                ccc = str(cases)
                                all_cases.append(ccc)
                                cases.clear()

                        else:
                            if c != (process_num - 1):
                                for i in range(each_process_exc_case_num):
                                    if fuzz_pool.scard(str(next_api + 1) + 'optional') < each_process_exc_case_num and fuzz_pool.scard(
                                            str(next_api + 1) + 'optional') != 0:
                                        for j in list(fuzz_pool.smembers(str(next_api + 1) + 'optional')):
                                            print(f"每个测试的用例有{j}")
                                            cases.append(j)
                                            fuzz_pool.srem(str(next_api + 1) + 'optional', j)
                                        cc = str(cases)
                                        all_cases.append(cases)
                                        cases.clear()
                                    elif fuzz_pool.scard(str(next_api + 1) + 'optional') != 0:
                                        print(f"每个测试的用例有{fuzz_pool.sscan(str(next_api + 1) + 'optional')[1][0]}")
                                        cases.append(fuzz_pool.sscan(str(next_api + 1) + 'optional')[1][0])
                                        fuzz_pool.srem(str(next_api + 1) + 'optional', fuzz_pool.sscan(str(next_api + 1) + 'optional')[1][0])
                                c = str(cases)
                                all_cases.append(c)
                                cases.clear()
                                if fuzz_pool.scard(str(next_api + 1) + 'optional') == 0:
                                    break
                            else:
                                for m in list(fuzz_pool.smembers(str(next_api + 1) + 'optional')):
                                    print(f"每个测试的用例有{m}")
                                    cases.append(m)
                                    fuzz_pool.srem(str(next_api + 1) + 'optional', m)
                                ccc = str(cases)
                                all_cases.append(ccc)
                                cases.clear()

            all_casess = []
            for a in all_cases:
                b = eval(a)
                all_casess.append(b)

            print(f"所有测试用例{all_casess}")

            if each_process_exc_case_num == 0 and int(len(fuzz_cases)) == 1:
                print(1)
                process = []
                for i in range(process_num):
                    all_casess.append([])
                    p = Process(target=test, args=(operation_mode, cov_url, restart, nums,
                                                   api_info, Authorization, username, password, all_casess[i], ))
                    p.start()
                    process.append(p)

                for i in range(process_num):
                    process[i].join()

            elif each_process_exc_case_num == 0:
                print(2)
                process = []
                for i in range(int(len(fuzz_cases))):
                    p = Process(target=test, args=(operation_mode, cov_url, restart, nums,
                                                   api_info, Authorization, username, password, all_casess[i], ))
                    p.start()
                    process.append(p)

                for i in range(int(len(fuzz_cases))):
                    process[i].join()
            elif each_process_exc_case_num == 1 and (process_num - 1) == int(len(fuzz_cases)):
                process = []
                for i in range(int(len(fuzz_cases))):
                    p = Process(target=test, args=(operation_mode, cov_url, restart, nums,
                                                   api_info, Authorization, username, password, all_casess[i], ))
                    p.start()
                    process.append(p)

                for i in range(int(len(fuzz_cases))):
                    process[i].join()

            else:
                print(3)
                process = []
                for i in range(process_num):
                    p = Process(target=test, args=(operation_mode, cov_url, restart, nums,
                                                   api_info, Authorization, username, password, all_casess[i], ))
                    p.start()
                    process.append(p)

                for i in range(process_num):
                    process[i].join()

            g = eval(matr.lindex("matrix", 1))
            visited = eval(matr.lindex("visited", 0))
            visited[next_api] = 1
            matr.lpush("visited", str(visited))
            matr.lpush("matrix", str(g))
            matr.lpush("matrix", next_api)

            print(f"测完第{next_api}个api,并发进程数是{process_num},当前可选参数个数为{nums}个")
            flag.srem('over', 1)
            flag.sadd('over', 0)
        fuzz_pool.flushdb()