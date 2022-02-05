import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import *
import datetime
import numpy as np
import matplotlib.colors as mcol
import matplotlib.cm as cm
def get_plot(xlabel_text,ylabel_text):
    global cid
    # cid = fig.canvas.mpl_connect('key_press_event', on_key)
    fig.subplots_adjust(bottom=0.15)
    fig.canvas.toolbar.pack_forget()

    tickParamColor = "white"
    backgroundColor = "black"

    fig.patch.set_color(backgroundColor)
    ax.patch.set_color(backgroundColor)

    ax.spines['bottom'].set_color(tickParamColor)
    ax.spines['top'].set_color(tickParamColor)
    ax.spines['right'].set_color(tickParamColor)
    ax.spines['left'].set_color(tickParamColor)
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    ax.set_yscale('log')

    ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.xaxis.set_major_locator(MultipleLocator(365))
    ax.grid()
    plt.xlabel(xlabel_text, labelpad=40, fontsize=20, color=tickParamColor)
    plt.ylabel(ylabel_text, labelpad=40, fontsize=20, color=tickParamColor)
    plt.title("inspired by: Benjamin Cowen", color=tickParamColor, pad=30, fontsize=25)

def set_plot(ax,date = datetime):
    pass

def legend_and_show():
    legend = plt.legend(loc="upper right", framealpha=0)
    plt.setp(legend.get_texts(), color='w')
    plt.show()
def get_risk(data):
    a=[]
    for d in data:
        if d == "NaN":
            a.append(0)
        else:
            a.append(min(float(d),1))
    return a
def split_axis_into_two(x):
    a = []
    for i in range(len(x)-1):
        a.append([x[i],x[i+1]])
    return a


raw_data = pd.read_csv("..\data\Bit INDEX 2021-10-22_ISO_time.csv")

close = np.asarray(list(map(float, raw_data["close"])))
reshaped_close = split_axis_into_two(close)

risk_data = get_risk(raw_data["Plot"])


time = [datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ") for d in raw_data["time"]]
reshaped_time = split_axis_into_two(time)
#
current_plot_index =0  # to show which chart we on

cm1 = mcol.LinearSegmentedColormap.from_list("MyCmapName",["b","aqua","gold","r"])
cpick = cm.ScalarMappable(cmap=cm1)


xyLabels = [["Date","Price"]]
fig, ax = plt.subplots()
get_plot(xyLabels[current_plot_index][0],xyLabels[current_plot_index][1])
cb = plt.colorbar(cpick)
cb.set_label("Risk", color= "white",fontsize=15)
# set colorbar tick color
cb.ax.yaxis.set_tick_params(color='white')

# set colorbar edgecolor
cb.outline.set_edgecolor('white')
plt.setp(plt.getp(cb.ax.axes, 'yticklabels'), color='white')

for p,t,c in zip(reshaped_close[100:],reshaped_time[100:],risk_data[100:]):
    ax.plot(t,p,linewidth=5,color=cpick.to_rgba(c))
#
legend_and_show()


