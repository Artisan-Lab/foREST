from fnmatch import fnmatch
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
                if api_ in api.keys():
                    pass
                else:
                    count = count + 1
                    api[status + api_] = time + "&" + str(count)

    print(api)


sum = 69  # the number of api
x = []
y = []
i = list(api.keys())
for value in api.values():
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