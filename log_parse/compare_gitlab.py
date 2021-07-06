import csv
from datetime import datetime
from fnmatch import fnmatch

from matplotlib import pyplot as plt
from pyecharts  import options as opts   #pyecharts库，用于绘制图表
from pyecharts.charts import Line  # 折线图绘制模块


##############################

api_restler = {}
count_restler = 0
files_restler = ["./restler_gitlab/network.testing.123145504280576.1.txt",
                 "./restler_gitlab/network.testing.123145504280576.2.txt",
                 "./restler_gitlab/network.testing.123145504280576.3.txt",
                 "./restler_gitlab/network.testing.123145504280576.4.txt",
                 "./restler_gitlab/network.testing.123145504280576.5.txt",
                 "./restler_gitlab/network.testing.123145504280576.6.txt"]
# files = ["./restler_gitlab/network.testing.123145582157824.1.txt"]
for file in files_restler:
    with open(file) as file:
        while True:
            line = file.readline()
            if not line:
                break
            sending = line.split(" ")
            if "Sending:" in sending:
                time = sending[0] + " " + sending[1]
                time = ''.join(list(time)[0:23])
                # print(time)
                api_ = sending[3] + sending[4]
                api_ = ''.join(list(api_)[1:])
                # print(api_)
                nextline = next(file)
                next_line = next(file)
                received = next_line.split(" ")
                status = received[4]
                # print(count_restler)
                # print(status)
                if not fnmatch(status, "4*"):
                    if status + api_ in api_restler.keys():
                        pass
                    else:
                        count_restler = count_restler + 1
                        api_restler[status + api_] = time + "&" + str(count_restler)


apis_restler = {}

for i in range(len(api_restler.keys())):
    a = list(api_restler.values())[i].split("&")
    apis_restler[list(api_restler.keys())[i]] = "".join(list(a[0])[:19]) + "&" + str(i)

time_ = list(apis_restler.values())[0].replace("&0", "")
t0_restler = datetime.strptime(time_, "%Y-%m-%d %H:%M:%S")

plo_restler = {}
for i in range(len(apis_restler.keys())):
    if i == 0:
        plo_restler[list(apis_restler.keys())[i]] = str(0) + "&" + str(i)
    else:
        a = list(apis_restler.values())[i].split("&")
        plo_restler[list(apis_restler.keys())[i]] = str(datetime.strptime(a[0], "%Y-%m-%d %H:%M:%S") - t0_restler) + "&" + str(i)

# print(apis_restler)
# print(time_)
# print(type(time_))
# print("----------------------------------------------------")
# print(plo_restler)
sum = 677
x_restler = []
y_restler = []

for value in plo_restler.values():
    val = value.split("&")
    if val[0] != "0":
        ti = val[0].split(":")
        t = int(ti[1])*60 + int(ti[2])
        x_restler.append(t)
    else:
        x_restler.append(val[0])
    y_restler.append("%.4f"%float(float(val[1]) / sum))

x_restler.append(60*60)
y_restler.append(y_restler[-1])


###############################

api = {}
count = 0
with open("./request.log") as file:
    while True:
        line = file.readline()
        if not line:
            break
        sending = line.split(" ")
        if "Sending:" in sending:
            time = sending[0] + " " + sending[1]
            time = ''.join(list(time)[0:19])
            # print(time)
            api_ = sending[3] + sending[4]
            api_ = ''.join(list(api_)[1:])
            # print(api_)
            # nextline = next(file)
            next_line = next(file)
            received = next_line.split(" ")
            status = received[4]
            # print(status)
            if not fnmatch(status, "4*"):
                if status + api_ in api.keys():
                    pass
                else:
                    count = count + 1
                    api[status + api_] = time + "&" + str(count)

apis = {}

for i in range(len(api.keys())):
    a = list(api.values())[i].split("&")
    apis[list(api.keys())[i]] = "".join(list(a[0])[:19]) + "&" + str(i)


time_ = list(apis.values())[0].replace("&0", "")
t0 = datetime.strptime(time_, "%Y-%m-%d %H:%M:%S")

plo = {}
for i in range(len(apis.keys())):
    if i == 0:
        plo[list(apis.keys())[i]] = str(0) + "&" + str(i)
    else:
        a = list(apis.values())[i].split("&")
        plo[list(apis.keys())[i]] = str(datetime.strptime(a[0], "%Y-%m-%d %H:%M:%S") - t0) + "&" + str(i)

# print(apis)
# print("----------------------------------------------------------")
# print(time_)
# print(plo)


sum = 677  # the number of api
x = []
y = []

for value in plo.values():
    val = value.split("&")
    if val[0] != "0":
        ti = val[0].split(":")
        t = int(ti[1])*60 + int(ti[2])
        x.append(t)
    else:
        x.append(val[0])
    y.append("%.4f"%float(float(val[1]) / sum))

x.append(60*60)
y.append(y[-1])
##########################################

out = open("./restler_gitlab.csv", "a", newline="")
csv_write = csv.writer(out, dialect="excel")
for i in range(len(x_restler)):
    w = []
    w.append(str(x_restler[i]))
    w.append(str(y_restler[i]))
    csv_write.writerow(w)

out = open("./rest_fuzz_gitlab.csv", "a", newline="")
csv_write = csv.writer(out, dialect="excel")
for i in range(len(x)):
    w = []
    w.append(str(x[i]))
    w.append(str(y[i]))
    csv_write.writerow(w)
##########################################


# print(x_restler, y_restler)
# print("-------------------")
# print(x, y)



# line = (
#         Line()
#         .add_xaxis(x)
#         .add_yaxis("restful_api_fuzz gitlab api 覆盖率", y)
#         .add_yaxis("restler gitlab api 覆盖率", y_restler)
#         .set_global_opts(title_opts=opts.TitleOpts(title="覆盖率-时间曲线"))
#      )
#
# line.render('compare_gitlab_coverage.html') #生成HTML文件 在浏览器中打开 即可看到折线图



