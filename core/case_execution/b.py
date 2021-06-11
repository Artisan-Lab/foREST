# import time
# from multiprocessing import Process,Pool
#
# def a():
#     time.sleep(6)
#     print("asdfghjkl")
# def waitp():
#     print("等待")
#
#
#
# if __name__ == '__main__':
#     # pool = Pool(processes=3)
#     # for i in range(3):
#     #     pool.apply_async(a, ())
#
#     process = []
#     for i in range(5):
#         p = Process(target=a, args=())
#         process.append(p)
#     for i in range(5):
#         process[i].start()
#     for i in range(5):
#         process[i].join()
#
#     print("over")

# import redis
# r = redis.StrictRedis(host="127.0.0.1", port=6379, db=1, decode_responses=True)
# r.flushdb()
# print(r.sscan(str(46))[1])
# print(type(r.sscan(str(46))[1]))
# if r.sscan(str(46))[1] == ['{}']:
#     print(1)
# a = r.sscan("56")
# b = a[1]
# c = []
# for i in range(1):
#     if r.scard("56") < 1:
#         print(list(r.smembers("56")))
#         for j in list(r.smembers("56")):
#             c.append(j)
#             r.srem("56", j)
#         break
#     else:
#         c.append(b[i])
#         r.srem("56", b[i])
# print(c)







# import random
#
#
# def get_next_apis():
#     next_apis = {}
#     apis = []
#     gra = [[2,-1,-1,0,1],
#            [1,-1,-1,2,5],
#            [3,-1,-1,-1,4],
#            [-1,-1,-1,-1,-1],
#            [1,-1,-1,-1,2]]
#     visited = [0,0,0,1,0]
#     global flag
#     flag = len(gra)
#     print(f"flag 是 {flag}")
#     for i in range(len(visited)):
#         if visited[i] != 1:
#             print(f"i 是 {i}")
#             count = 0
#             for j in range(len(gra[i])):
#                 print(f"  j 是 {j}")
#                 if gra[i][j] != -1:
#                     count += 1
#             print(f"count 是 {count}")
#             if count <= flag:
#                 flag = count
#                 next_apis[i] = count
#     print(next_apis)
#
#
#     m = min(next_apis.values())
#     print(f"最小值是{m}")
#     for key in next_apis.keys():
#         if next_apis[key] == m:
#             apis.append(key)
#     print(apis)
#     print(random.choice(apis))
#
# get_next_apis()
import redis


fuzz_pool = redis.StrictRedis(host="127.0.0.1", port=6379, db=1, decode_responses=True)
nums = 0
process_num = 5
each_process_exc_case_num = 1
next_api = 0
cases = []
all_cases = []



for k in range(process_num):
    if nums == 0:
        if k != process_num-1:
            for i in range(each_process_exc_case_num):
                # print(fuzz_pool.smembers(str(next_api + 1)))
                if fuzz_pool.scard(str(next_api + 1)) < each_process_exc_case_num and fuzz_pool.scard(str(next_api + 1)) != 0:
                    for j in list(fuzz_pool.smembers(str(next_api + 1))):
                        print(f"每个测试的用例有{j}")
                        cases.append(j)
                        fuzz_pool.srem(str(next_api + 1), j)
                    cc = str(cases)
                    all_cases.append(cc)
                    cases.clear()
                elif fuzz_pool.scard(str(next_api + 1)) != 0:
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
        for i in range(each_process_exc_case_num):
            if fuzz_pool.scard(str(next_api + 1) + 'optional') < each_process_exc_case_num:
                for j in list(fuzz_pool.smembers(str(next_api + 1) + 'optional')):
                    cases.append(j)
                    # fuzz_pool.srem(str(next_api + 1) + 'optional', j)
                break
            else:
                cases.append(fuzz_pool.sscan(str(next_api + 1) + 'optional')[1][i])
                # fuzz_pool.srem(str(next_api + 1) + 'optional', fuzz_pool.sscan(str(next_api + 1) + 'optional')[1][i])

print(all_cases)



#
# c = []
# ccc = ['["{\'name\': \'PD1111119Dsts3\'}", "{\'name\': \'PD9555Dsts3\'}"]', '["{\'name\': \'PD2222Dsts3\'}", "{\'name\': \'PD99999Dsts3\'}"]', '["{\'name\': \'PD44449Dsts3\'}"]']
# for a in ccc:
#     b = eval(a)
#
#     c.append(b)
#
# print(c)










































