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

list = [1,2,0,1,5,0,3,6]
for i,v in enumerate(list):
    if v == 0:
        print(i)