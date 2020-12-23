import pygal
import operator
from pygal.style import Style

# This file is responsible for all math calculations and graph creation
# I rely on dictionaries and tuples in order to organize my data
# and make it useful for data visualization


# time calculation formulas
# calculate total time from multiple 'total' column
# check if ':' in data because if we are currently recording our 'total' value is 0
# we calculate values only from completed rows
def cal_time(total1):
    min1 = 0
    hrs = 0
    for t in total1:
        if type(t) == str:
            t = (str(t))
            if ":" in t:
                hrs += int(t[0:2])
                min1 += int(t[3:5])
                total1 = (str(hrs + min1 // 60) + ":" + str(min1 % 60))
        else:
            if type(t) != int:
                t = t[0]
                # print(t)
                t = (str(t))
                # print(t)
                if ":" in t:
                    hrs += int(t[0:2])
                    min1 += int(t[3:5])
                    total1 = (str(hrs + min1 // 60) + ":" + str(min1 % 60))
        # print(total1)
    return total1


# convert regular tine time to minutes 01:10 == int(70)
# need to calculate average a week
def make_minutes(time):
    time = time.split(':')
    hours = time[0]
    minutes = time[0]
    total = int(hours) * 60 + int(minutes)
    return total


# calculate difference between 2 times, t1 is initial and t2 is last
def time_dif(t1, t2):
    # calculate difference between two times  to calculate 'total' time
    # main time dif formula
    def time_delta():
        total_s = min_t2 - min_t1
        hr = str(total_s // 60)
        min_t = str(total_s % 60)
        # we are checking if len of calculation is bigger that 1
        # if we didn't out time would look '2:2' instead of '02:02'
        if len(hr) == 1:
            hr = ('0' + hr)
        if len(min_t) == 1:
            min_t = ('0' + min_t)
        t_total = (hr + ':' + min_t)
        return t_total
    # convert time in total minutes and determine way how data recorded
    hrs1 = int(t1[0:2])
    min1 = int(t1[3:5])
    hrs2 = int(t2[0:2])
    min2 = int(t2[3:5])
    min_t1 = hrs1 * 60 + min1
    min_t2 = hrs2 * 60 + min2
    # use this condition in case we started and 11 pm and finished at 1 am
    # 1440 is number of minutes in a day
    if hrs2 >= hrs1:
        time_delta()
    elif hrs2 < hrs1:
        min_t2 += 1440
        time_delta()
    t_total = (time_delta())
    return t_total


# dictionary for adding times from previous weeks
# make one upwards line
def conseq_add(dictionary):
    conseq_lib = {}
    number = 0
    tuple_dict = dictionary.items()
    for each in tuple_dict:
        number += each[1]
        conseq_lib.update({each[0]: number})
    return conseq_lib


# make sorted dictionary by sorting by 1st tuple
# limit number of items we want to get from dictionary
def sorted_dict(dictionary, limit):
    sorted_tuples = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    sorted_tuples = sorted_tuples[:limit]
    sort_dict = {}
    for each in sorted_tuples:
        sort_dict.update({each[0]: each[1]})
    return sort_dict


# make dictionary that only include items on a list
# the list contains list of projects that have been completed
def completed(completed, dictionary):
    new_dik = {}
    for each in dictionary:
        if each in completed:
            new_dik.update({each: dictionary.get(each)})
    return new_dik


# make graphs using pygal dictionary
# rely on dictionaries to get values
# keys = labels, values = numbers
# global variable because all y axis labels are the same
y_title = 'time(hrs)'


def bar_graph(dictionary, title, x_title, output):
    graph = pygal.Bar(height=400, width=500, y_title=y_title, x_title=x_title, show_legend=False)
    graph.title = title
    graph.x_labels = (dictionary.keys())
    graph.add(title, dictionary.values())
    if output == 'html':
        graph.render_in_browser()
    else:
        return graph.render_data_uri()


def multi_list_bar_graph(dictionary, title, x_title, y_title):
    graph = pygal.Bar(y_title=y_title, x_title=x_title, show_legend=False)
    graph.title = title
    for day in dictionary:
        data_list = dictionary.get(day)
        graph.add('day', (round(sum(data_list) / len(data_list) / 60, 2)))
    graph.render_data_uri()


def line_graph(dictionary, title, x_title, y_title):
    graph = pygal.Line(height=300, width=600, y_title=x_title, x_title=y_title, show_legend=False)
    graph.title = title
    graph.x_labels = (dictionary.keys())
    graph.add(title, dictionary.values())
    return graph.render_data_uri()


def horiz_bar(dictionary, title, x_title, output):
    graph = pygal.HorizontalBar(height=220, width=500, y_title=x_title, x_title=y_title,
                                show_legend=False)
    graph.title = title
    graph.x_labels = (dictionary.keys())
    graph.add(title, dictionary.values())
    if output == 'html':
        graph.render_in_browser()
    else:
        return graph.render_data_uri()


def multiple_line(total, weekly, title, x_title, output):
    graph = pygal.Line(height=250, width=500, y_title=y_title, x_title=x_title, show_legend=True)
    graph.title = title
    graph.add('Total', total)
    graph.add('Weekly', weekly)
    if output == 'html':
        graph.render_in_browser()
    else:
        return graph.render_data_uri()


def pie_charts(dictionary, title):
    pie_chart = pygal.Pie(legend_at_bottom=True)
    pie_chart.title = title.capitalize()
    for item in dictionary:
        pie_chart.add(item, float(dictionary.get(item)))
    return pie_chart.render_data_uri()




