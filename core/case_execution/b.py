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

import redis
r = redis.StrictRedis(host="127.0.0.1", port=6379, db=7, decode_responses=True)
a = r.sscan("16")
b = a[1]
c = []
for i in range(3):
    if r.scard("16") < 3:
        print(list(r.smembers("16")))
        for j in list(r.smembers("16")):
            c.append(j)
            r.srem("16", j)
        break
    else:
        c.append(b[i])
        r.srem("16", b[i])
print(c)

















