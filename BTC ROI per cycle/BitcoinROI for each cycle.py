import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import *
import datetime
import math
def get_plot(xlabel_text,ylabel_text):
    global cid
    cid = fig.canvas.mpl_connect('key_press_event', on_key)
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
    ax.xaxis.set_major_locator(MultipleLocator(365))
    ax.grid()
    plt.xlabel(xlabel_text, labelpad=40, fontsize=20, color=tickParamColor)
    plt.ylabel(ylabel_text, labelpad=40, fontsize=20, color=tickParamColor)
    plt.title("credit: Benjamin Cowen", color=tickParamColor, pad=30, fontsize=25)

def set_plot(ax,date = datetime):
    pass
def plot_axis(cycle_lows, cycle_highs, axes_color = ["green", "orange", "red", "#3594FF"]):
    ROI_prices, date_passed = ROI_calculate(close, time, cycle_lows, cycle_highs)
    date_since_bottoms_per_cycle = []
    for date_since_bottom in date_passed:
        date_since_bottoms_per_cycle.append([i + 1 for i in range(date_since_bottom)])

    for i in range(len(cycle_lows)):
        ax.plot(date_since_bottoms_per_cycle[i], ROI_prices[i], color=axes_color[i], label=str.format(
            "{first_year:04d}/{first_month:02d}/{first_date:02d} ~ {second_year:04d}/{second_month:02d}/{second_date:02d} cycle"
            , first_year=cycle_lows[i].year, first_month=cycle_lows[i].month, first_date=cycle_lows[i].day
            , second_year=cycle_highs[i].year, second_month=cycle_highs[i].month, second_date=cycle_highs[i].day))

def on_key(event):
    global current_plot_index
    global fig, ax #I probably will end up in hell for this fuckfest code


    if(event.key == "right"):
        plt.cla()
        current_plot_index = (current_plot_index+1)%len(cycle_lows)
        get_plot(xyLabels[current_plot_index][0], xyLabels[current_plot_index][1])
        plot_axis(cycle_lows[current_plot_index], cycle_highs[current_plot_index])
        legend_and_show()
    elif(event.key == "left"):
        plt.cla()
        current_plot_index = (current_plot_index - 1) % len(cycle_lows)
        get_plot(xyLabels[current_plot_index][0], xyLabels[current_plot_index][1])
        plot_axis(cycle_lows[current_plot_index], cycle_highs[current_plot_index])
        legend_and_show()
def legend_and_show():
    legend = plt.legend(loc="upper right", framealpha=0)
    plt.setp(legend.get_texts(), color='w')
    plt.show()

def get_angle_in_degree(x,y):
    return math.degrees(math.atan(y/x))

def ROI_calculate(prices,dates,low_dates,high_dates):
    ROI_prices_axes = []
    date_passed = []
    for low_date,high_date in zip(low_dates,high_dates):
        low_index = dates.index(low_date)
        high_index = dates.index(high_date)
        date_passed.append(high_index-low_index+1)
        ROI_prices = []
        for i in range(low_index,high_index+1):
            ROI_prices.append((prices[i]/prices[low_index]*100))
        ROI_prices_axes.append(ROI_prices)
    return ROI_prices_axes, date_passed

raw_data = pd.read_csv("..\data\Bitstamp ALL TIME 2021-10-18_ISO_time.csv")

close = list(map(float, raw_data["close"]))
time = [datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ") for d in raw_data["time"]]
#
current_plot_index =0  # to show which chart we on

cycle_lows = []
cycle_highs = []
recent_date = datetime.datetime(2021,10,18)
cycle_lows.append([datetime.datetime(2009,12,18), datetime.datetime(2011,11,18), datetime.datetime(2015,8,18), datetime.datetime(2018,12,15)]) #list of cycle
cycle_highs.append([datetime.datetime(2011,6,8), datetime.datetime(2013,12,4), datetime.datetime(2017,12,16), recent_date])

cycle_lows.append([datetime.datetime(2012,11,29), datetime.datetime(2016,7,10), datetime.datetime(2020,5,12)]) #cycle per halving
cycle_highs.append([datetime.datetime(2016,7,9), datetime.datetime(2020,5,11), recent_date])

cycle_lows.append([datetime.datetime(2011,6,8), datetime.datetime(2013,12,4), datetime.datetime(2017,12,16)]) #list of ATH
cycle_highs.append([datetime.datetime(2013,12,4), datetime.datetime(2017,12,16), recent_date])

#
xyLabels = [["date since bottom","percentage return"],["date since halving","percentage return"],["date since ATH","percentage return"]]
fig, ax = plt.subplots()
get_plot(xyLabels[current_plot_index][0],xyLabels[current_plot_index][1])
plot_axis(cycle_lows[current_plot_index],cycle_highs[current_plot_index])
#
legend_and_show()


