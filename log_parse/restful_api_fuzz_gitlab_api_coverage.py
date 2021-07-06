from datetime import datetime
from fnmatch import fnmatch

from matplotlib import pyplot as plt
from pyecharts  import options as opts   #pyecharts库，用于绘制图表
from pyecharts.charts import Line  # 折线图绘制模块


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
            print(time)
            api_ = sending[3] + sending[4]
            api_ = ''.join(list(api_)[1:])
            print(api_)
            # nextline = next(file)
            next_line = next(file)
            received = next_line.split(" ")
            status = received[4]
            print(status)
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


time_restler = list(apis.values())[0].replace("&0", "")
t0 = datetime.strptime(time_restler, "%Y-%m-%d %H:%M:%S")

plo = {}
for i in range(len(apis.keys())):
    if i == 0:
        plo[list(apis.keys())[i]] = str(0) + "&" + str(i)
    else:
        a = list(apis.values())[i].split("&")
        plo[list(apis.keys())[i]] = str(datetime.strptime(a[0], "%Y-%m-%d %H:%M:%S") - t0) + "&" + str(i)

print(apis)
print("----------------------------------------------------------")
print(time_restler)
print(plo)


sum = 677  # the number of api
x = []
y = []
i = list(plo.keys())
for value in plo.values():
    val = value.split("&")
    x.append(val[0])
    y.append(int(val[1])/sum)

line = (
        Line()
        .add_xaxis(x)
        .add_yaxis("restful_api_fuzz gitlab api 覆盖率", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="覆盖率-时间曲线"))
     )

line.render('restful_api_fuzz_api_coverage.html') #生成HTML文件 在浏览器中打开 即可看到折线图

