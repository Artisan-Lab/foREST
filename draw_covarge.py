from pyecharts  import options as opts   #pyecharts库，用于绘制图表
from pyecharts.charts import Line  # 折线图绘制模块

x1 = [0.00]
y1 = [0.00]
with open('./cov/COVERAGE_RATE-ps.txt') as k:
    a = "0.00%"
    for line in k:
        time, per = line.split()
        print(per)
        if per != a and per != "0.00%":
            a = per
            b = float(''.join(list(per)[:-1]))/100.00
            c = '%.6f' % b
            x1.append(time)
            y1.append(c)

x2 = [0.00]
y2 = [0.00]
with open('./cov/COVERAGE_RATE-pns.txt') as k:
    a = "0.00%"
    for line in k:
        time, per = line.split()
        print(per)
        if per != a and per != "0.00%":
            a = per
            b = float(''.join(list(per)[:-1]))/100.00
            c = '%.6f' % b
            x2.append(time)
            y2.append(c)

x3 = [0.00]
y3 = [0.00]
with open('./cov/COVERAGE_RATE-ss.txt') as k:
    a = "0.00%"
    for line in k:
        time, per = line.split()
        print(per)
        if per != a and per != "0.00%":
            a = per
            b = float(''.join(list(per)[:-1]))/100.00
            c = '%.6f' % b
            x3.append(time)
            y3.append(c)

x4 = [0.00]
y4 = [0.00]
with open('./cov/COVERAGE_RATE-sns.txt') as k:
    a = "0.00%"
    for line in k:
        time, per = line.split()
        print(per)
        if per != a and per != "0.00%":
            a = per
            b = float(''.join(list(per)[:-1]))/100.00
            c = '%.6f' % b
            x4.append(time)
            y4.append(c)


line = (
        Line()
        .add_xaxis(x4)
        .add_yaxis("并发有认证覆盖率", y1)
        .add_yaxis("并发无认证覆盖率", y2)
        .add_yaxis("串行有认证覆盖率", y3)
        .add_yaxis("串行无认证覆盖率", y4)
        .set_global_opts(title_opts=opts.TitleOpts(title="覆盖率-时间曲线"))
     )



line.render('coverages.html') #生成HTML文件 在浏览器中打开 即可看到折线图
