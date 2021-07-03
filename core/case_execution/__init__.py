from module.make_url import make_url

url = "12{3}{4}{5}"
p_location = [0,0,0]
p_name = ["3","4","5"]
v1 = [1,1,1]
v2 = [2,2,2]
v3 = [3,3,3]
v= []
pl = []
pn = []
v.append(v1)
v.append(v2)
v.append(v3)
for i in range(3):
    pl.append(p_location)
    pn.append(p_name)
headers = {}
data = {}
for i in range(3):
    print(make_url().make(url,pl[i],pn[i],v[i],headers,data))