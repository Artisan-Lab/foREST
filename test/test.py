# di = {
#     0:['jj','ko'],
#     9:['fty+nkj','njk'],
#     15:[],
#     6:[],
#     4:[]
# }
#
# list = [0,1,15,2,6,48,9]
#
# for l in list:
#     if l in di.keys():
#         print(l)

# list = [1,2,0,1,5,0,3,6]
# for i,v in enumerate(list):
#     if v == 0:
#         print(i)

# import numpy as np
# graph = []
# visited = np.zeros(len(graph)).astype(dtype=int).tolist()
#
# def r(i):
#     visited[i] = 8
#
# def ru(graph):
#     g = graph
#     print(type(visited))
#     visited[1] = 2
#     r(3)
#     print(visited[1])
#
# def al():
#     graph = [1, 2, 3, 6, 5, 4, 7, 8, 9, 1]
#     for i in range(15):
#         ru()
#         print(visited[3])
#
# al()
# m = 'view'
#
# if m != None:
#     print(1)

# la = ['a',5,'ed',95]
# h = {}
# d = []
# for k,v in enumerate(la):
#     h[k]=v
#
# print(type(h))
# print(h)
# if h.__contains__(0):
#     print(1)

# path = 'http://10.177.74.168:81/wp-json/wp/v2/posts'
# url = 'http://10.177.74.168:81/wp-json/wp/v2'
#
# ll = path.replace(url, '')
# print(ll)
