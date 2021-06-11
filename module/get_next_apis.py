
def get_next_apis(matr):
    apis = []
    next_apis = {}
    gra = eval(matr.lindex("matrix", 1))
    visited = eval(matr.lindex("visited", 0))
    flag = len(gra)
    for i in range(len(visited)):
        if visited[i] != 1:
            count = 0
            for j in range(len(gra[i])):
                if gra[i][j] != -1:
                    count += 1
            if count <= flag:
                flag = count
                next_apis[i] = count

    m = min(next_apis.values())
    print(f"最小值是{m}")
    for key in next_apis.keys():
        if next_apis[key] == m:
            apis.append(key)
    print(f"当前入度最小的api集合为{apis},入度为{m}")
    return apis

