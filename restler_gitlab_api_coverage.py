from fnmatch import fnmatch
from pyecharts  import options as opts   #pyecharts库，用于绘制图表
from pyecharts.charts import Line  # 折线图绘制模块


api = {}
count = 0
files = ["./restler_gitlab/network.testing.123145368481792.1.txt",
         "./restler_gitlab/network.testing.123145368481792.2.txt",
         "./restler_gitlab/network.testing.123145368481792.3.txt",
         "./restler_gitlab/network.testing.123145368481792.4.txt",
         "./restler_gitlab/network.testing.123145368481792.5.txt"]
for file in files:
    with open(file) as file:
        while True:
            line = file.readline()
            if not line:
                break
            sending = line.split(" ")
            if "Sending:" in sending:
                time = sending[0] + " " + sending[1]
                time = ''.join(list(time)[0:23])
                print(time)
                api_ = sending[3] + sending[4]
                api_ = ''.join(list(api_)[1:])
                print(api_)
                nextline = next(file)
                next_line = next(file)
                received = next_line.split(" ")
                status = received[4]
                print(count)
                print(status)
                if not fnmatch(status, "4*"):
                    if api_ in api.keys():
                        pass
                    else:
                        count = count + 1
                        api[status + api_] = time + "&" + str(count)


apis = {}
for i in range(len(api.keys())):
    a = list(api.values())[i].split("&")
    apis[list(api.keys())[i]] = a[0] + "&" + str(i)

print(apis)

sum = 677
x = []
y = []
i = list(apis.keys())
for value in apis.values():
    val = value.split("&")
    x.append(val[0])
    y.append(int(val[1])/sum)

line = (
        Line()
        .add_xaxis(x)
        .add_yaxis("restler gitlab api 覆盖率", y)
        .set_global_opts(title_opts=opts.TitleOpts(title="覆盖率-时间曲线"))
     )



line.render('restler_gitlab_api_coverage.html') #生成HTML文件 在浏览器中打开 即可看到折线图



