import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv("./data.csv")

data_30min = data[data["time"] == "30min"]
data_6h = data[data["time"] == "6h"]
ax = sns.catplot(x="tool_name", y="coverage (#LoC)", order=["RESTler", "EvoMaster","restler"],data=data, hue="time",  col="server_name",kind="box", aspect=.5,linewidth=0.3, ci=None,width=0.4,legend=False)
ax.despine(left=True)

ax.figure.subplots_adjust(wspace=0.1, hspace=0)
for col_val, g in ax.axes_dict.items():
    g.set_title(" ")
    g.set_xlabel(col_val)
    if col_val == "commit":
        g.legend(loc=4,fontsize=8)
    if col_val != "project":
        g.axes.get_yaxis().set_visible(False)

plt.show()
