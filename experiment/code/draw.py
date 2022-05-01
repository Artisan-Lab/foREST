import csv
import matplotlib.dates as mdate
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
from datetime import datetime
import numpy as np



plt.figure(figsize=(150,150))

forest_file = open('../data/gitlab-all/foREST.csv')  # 打开csv文件
forestReader = csv.reader(forest_file)  # 读取csv文件
forestData = list(forestReader)  # csv数据转换为列表
forest_length = len(forestData)  # 得到数据行数

evomaster_file = open('../data/gitlab-all/evomaster.csv')
evomaster_reader = csv.reader(evomaster_file)
evomaster_data = list(evomaster_reader)
evomaster_length = len(evomaster_data)

restler_file = open('../data/gitlab-all/restler.csv')
restler_reader = csv.reader(restler_file)
restler_data = list(restler_reader)
restler_length = len(restler_data)
# for i in range(1,length_zu):
#     print(exampleData[i])

# restler_rw_file = open('../data/gitlab-project/RESTCT-6h.csv')
# restler_rw_reader = csv.reader(restler_rw_file)
# restler_rw_data = list(restler_rw_reader)
# restler_rw_length = len(restler_rw_data)

x1 = list()
y1 = list()
y12 = list()

x2 = list()
y2 = list()
y22 = list()

x3 = list()
y3 = list()
y32 = list()
x4 = list()
y4 = list()
y42 = list()
for i in range(0, forest_length):  # 从第二行开始读取
    # if '0:05:' in forestData[i][0]:
    #     break
    if i > 0 and forestData[i][0] == forestData[i-1][0]:
        continue
    date1 = datetime.strptime(forestData[i][0], '%H:%M:%S')
    x1.append(date1)  # 将第一列数据从第二行读取到最后一行赋给列表x
    y1.append(int(forestData[i][2]))
    y12.append(float(forestData[i][1]))

for _ in range(0, evomaster_length):
    # if '0:30:' in evomaster_data[_][0]:
    #     break
    if y2 and int(evomaster_data[_][2]) < y2[-1]:
        continue
    date2 = datetime.strptime(evomaster_data[_][0], '%H:%M:%S')
    x2.append(date2)
    y2.append(int(evomaster_data[_][2]))
    y22.append(float(evomaster_data[_][1]))

for _ in range(0, restler_length):
    # if '0:30:' in restler_data[_][0]:
    #     break
    date3 = datetime.strptime(restler_data[_][0], '%H:%M:%S')
    x3.append(date3)
    y3.append(int(restler_data[_][2]))
    y32.append(float(restler_data[_][1]))

# for _ in range(0, restler_rw_length):
#     # if '0:30:' in restler_rw_data[_][0]:
#     #     break
#     date4 = datetime.strptime(restler_rw_data[_][0], '%H:%M:%S')
#     x4.append(date4)
#     y4.append(int(restler_rw_data[_][2]))
#     y42.append(float(restler_rw_data[_][1]))
fig, ax = plt.subplots()
ax2 = ax.twinx()
# Plot the date using plot_date rather than plot
ax.plot(x1, y1, 'r-', label='foREST', linewidth=3)


ax.plot(x2, y2, 'b--', label='EvoMaster', linewidth=3)
ax.plot(x3, y3, color='violet', linestyle='-.', label='RESTler', linewidth=3)
# ax.plot(x4, y4,label='restCT', linewidth=3)
ax.legend(loc='lower right')
ax2.plot(x1, y12, 'b',alpha=0)
ax.set_xlabel("time (hours)")
ax.set_ylabel("code coverage (# LoC)")
ax2.set_ylabel("code coverage (rate)")
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')


ax.xaxis.set_major_formatter(mdate.DateFormatter('%H'))
# Choose your xtick format string
# date_fmt = '%m-%d %H:%M:%S'
# Use a DateFormatter to set the data to the correct format.


# Sets the tick labels diagonal so they fit easier.
plt.title('GitLab')
plt.legend(bbox_to_anchor=(1, 0.15), loc='upper right', borderaxespad=0, fontsize=8)
fig.savefig('GitLab.png', format='png', dpi=300, bbox_inches='tight')

plt.show()





