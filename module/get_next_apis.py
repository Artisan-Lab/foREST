
def get_next_apis(matr):
    next_apis = []
    gra = eval(matr.lindex("matrix", 1))
    visited = eval(matr.lindex("visited", 0))
    flag = len(gra)
    for i in visited:
        if i != 1:
            count = 0
            for j in gra[i]:
                if gra[i][j] != -1:
                    count += 1
            if count < flag:
                flag = count
                next_apis.append(i)
    m = min(next_apis)
    a = next_apis.copy()
    for i in a:
        if i != m:
            next_apis.remove(i)
    print(next_apis)
    return next_apis

