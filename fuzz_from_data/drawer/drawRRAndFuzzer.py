import matplotlib
import matplotlib.dates as mdate
import matplotlib.pyplot as plt

matplotlib.rcParams['timezone'] = 'Asia/Shanghai'

x1 = []
y1 = []
x2 = []
y2 = []
tmp = 0
flag = False

for line in open(
        "../coverageData/coverage.txt"):
    arr = line.split()
    # if tmp != int(arr[1]):
    #     tmp = int(arr[1])
    x1.append(float(arr[0]))
    y1.append(int(arr[1]))

for line in open(
        "../coverageData/coverage.txt"):
    arr = line.split()
    x2.append(float(arr[0]))
    # 19202
    # 19202
    if 41632 == int(arr[1]):
        flag = True
    if flag:
        y2.append(41632)
    else:
        y2.append(int(arr[1]))

# # x1 = [20, 33, 51, 79, 101, 121, 132, 145, 162, 182, 203, 219, 232, 243, 256, 270, 287, 310, 325]
# # y1 = [49, 48, 48, 48, 48, 87, 106, 123, 155, 191, 233, 261, 278, 284, 297, 307, 341, 319, 341]
#
# l1 = plt.plot(x1, y1, 'r--', label='RR and mutation')
# # l2 = plt.plot(x2, y2, 'g--', label='type2')
# # l3 = plt.plot(x3, y3, 'b--', label='type3')
# # plt.plot(x1, y1, 'ro-', x2, y2, 'g+-', x3, y3, 'b^-')
#
# plt.plot(x2, y2, 'g--', label='RR')
# plt.ylim((40000, 43000))
# # plt.title('The Lasers in Three Conditions')
# plt.xlabel('row')
# plt.ylabel('covered code lines')
# num2 = 0
# num3 = 3
# num4 = 0

# plt.show()
secs1 = mdate.epoch2num(x1)
secs2 = mdate.epoch2num(x2)
fig, ax = plt.subplots()

# Plot the date using plot_date rather than plot
ax.plot_date(secs1, y1, 'r-', label='R&R + fuzzer', linewidth=1)
ax.plot_date(secs2, y2, 'g--', label='R&R', linewidth=1)

plt.ylabel('covered code lines')
plt.xlabel('time')

# Choose your xtick format string
date_fmt = '%m-%d %H:%M'

# Use a DateFormatter to set the data to the correct format.
date_formatter = mdate.DateFormatter(date_fmt)
ax.xaxis.set_major_formatter(date_formatter)

# Sets the tick labels diagonal so they fit easier.
fig.autofmt_xdate()
# plt.ylim((10000, 30000))
plt.title('R&R vs R&R+fuzzer')
plt.legend(bbox_to_anchor=(1, 0.11), loc='upper right', borderaxespad=0, fontsize=8)

fig.savefig('R&R-fuzzer.svg', format='svg', dpi=1200)
plt.show()
