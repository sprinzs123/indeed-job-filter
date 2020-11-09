from flask import Flask, render_template
import collections
import datetime
import sqlite3
import math_calculation as calculi

DATABASE = './check in and out.db'
conn = sqlite3.connect(DATABASE)
cur = conn.cursor()


# all weeks recorded in db
# get all weeks nums and sort them
def all_week_nums():
    cur.execute("SELECT week FROM study")
    all_times = cur.fetchall()
    conn.commit()
    unique = set(all_times)
    all_weeks = []
    for i in list(unique):
        all_weeks.append(i[0])
    all_weeks.sort()
    return all_weeks


# for average study time per day
# getting total minutes for particular day and particular week
def day_of_week(week, day):
    cur.execute("SELECT total FROM study WHERE week = ? and day = ?", (week, day))
    all_times = cur.fetchall()
    conn.commit()
    if len(all_times) == 0:
        all_times = [('00:00'),]
    time_total = calculi.cal_time(all_times)
    all_minutes = calculi.make_minutes(time_total)
    # print(all_minutes)
    return all_minutes


# make list of all times for particular day from entire db
def list_time_day(day, week_nums):
    day_mins_all = []
    for week in week_nums:
        mins_day = day_of_week(week, day)
        if mins_day != 0:
            day_mins_all.append(mins_day)
    return day_mins_all


# get average for day
# returns list of averages per day
def get_avg_day():
    all_total_day = {}
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    week_nums = all_week_nums()
    for day in days:
        time = list_time_day(day, week_nums)
        all_total_day.update({day: time})
    calculi.multi_list_bar_graph(all_total_day, 'Time of day averages', 'days', 'hours')



get_avg_day()

# day_of_week(18, 'tuesday')

app = Flask(__name__)

@app.route('/')
def home():
    DATABASE = './check in and out.db'
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()

    # return a dictionaries keys=variable, value=hrs on that variable
    # get data to make graphs
    # can 'week' = hrs, each week, topic/project = return all of them
    def project_time(find):
        cur.execute("SELECT " + find + " FROM study GROUP BY " + find + "")
        project_names = cur.fetchall()
        full_dik = {}
        for goal in project_names:
            goal = (goal[0])
            cur.execute("SELECT total FROM study WHERE " + find + "=?", (goal,))
            all_times = cur.fetchall()
            conn.commit()
            duration = calculi.cal_time(all_times)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1]) / 60), 2)
            full_dik.update({goal: hours+min})
        return full_dik

    # breakdown on a certain project by topics used
    def project_breakdown(copare, column, find):
        cur.execute("SELECT " + copare + ", total FROM study WHERE " + column + "=? ", (find,))
        rows = cur.fetchall()
        c = collections.defaultdict(list)
        for a, b in rows:
            c[a].append(b)  # add to existing list or create a new one
        grouped_tpl = list(c.items())
        # print(grouped_tpl)
        sum_lib = {}
        for each in grouped_tpl:
            duration = calculi.cal_time(each[1])
            # print(duration)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1]) / 60), 2)
            if hours >= 1:
                sum_lib.update({each[0]: hours + min})
        return sum_lib

    # last n weeks reports
    # get all time for the last n week
    def weeks_report(find, number):
        time = datetime.datetime.now()
        modifier = (time.year - 2019) * 52
        current_week = time.isocalendar()[1] - 25 + modifier
        start_week = current_week - number

        # start_week = 33
        # current_week = 40
        # print(current_week, start_week)
        cur.execute("SELECT " + find + " FROM study WHERE week BETWEEN ? and ? "
                                       "GROUP BY " + find + "", (start_week, current_week))
        all_names = cur.fetchall()
        # print(all_names)
        conn.commit()
        full_dik = {}
        for goal in all_names:
            goal = (goal[0])
            cur.execute("SELECT total FROM study "
                        "WHERE " + find + "=? and week BETWEEN ? and ? ", (goal, start_week, current_week))
            all_times = cur.fetchall()
            conn.commit()
            duration = calculi.cal_time(all_times)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1]) / 60), 2)
            full_dik.update({goal: hours + min})
        return full_dik

    # bar graph of projecs/topics in past n weeks
    def past_study(find, number):
        time = datetime.datetime.now()
        modifier = (time.year - 2019) * 52
        current_week = time.isocalendar()[1] - 25 + modifier
        start_week = current_week - number
        cur.execute("SELECT " + find + " FROM study "
                                       "WHERE week BETWEEN ? and ? GROUP BY " + find + "", (start_week, current_week))
        project_names = cur.fetchall()
        full_dik = {}
        for goal in project_names:
            goal = (goal[0])
            cur.execute("SELECT total FROM study "
                        "WHERE " + find + "=? AND week BETWEEN ? and ?", (goal, start_week, current_week))
            all_times = cur.fetchall()
            conn.commit()
            duration = calculi.cal_time(all_times)
            split_time = duration.split(":")
            hours = int(split_time[0])
            min = round((int(split_time[1]) / 60), 2)
            if hours > 1:
                full_dik.update({goal: hours+min})
        return full_dik

    # Each function is a graph that is going to be displayed
    # goal = 'project'
    # some global variable we need
    limit = 5
    y_axis = 'Time(hrs)'
    completed_projects = ['review analysis', 'security app', 'mit', 'study.db', 'store', 'clinic', 'store2', 'bakery', 'debate', 'interview', 'translate']
    working_proj = "translate"

    # top subject/topic
    def get_top(goal, lmt):
        dictionary = project_time(goal)
        title = 'Top ' + str(lmt) + ' ' + goal + 's'
        x_axis = goal + 's'
        short_dict = calculi.sorted_dict(dictionary, lmt)
        return calculi.bar_graph(short_dict, title, x_axis, 'pygal')

    # consequitive line of time for all weeks
    def conseq_add(goal):
        dictionary = project_time(goal)
        full_dict = calculi.conseq_add(dictionary)
        title = 'Time completed vs weeks'
        return calculi.line_graph(full_dict, title, 'time(hrs)', 'week')

    # graph of projects that are finished and their time
    def done_proj(goal):
        dictionary = project_time(goal)
        dictionary = calculi.completed(completed_projects, dictionary)
        title = 'All completed projects'
        return calculi.horiz_bar(dictionary, title, 'Project Names', 'pygal')

    # project_breakdown('topic', 'project', 'review analysis') would give all topics in project
    # project_breakdown('project', 'topic', 'flask') all projects when used flask
    def one_summary(show, find, name_proj):
        full_dict = project_breakdown(show, find, name_proj)
        short_dict = calculi.sorted_dict(full_dict, limit)
        return calculi.pie_charts(short_dict, name_proj)

    # line graph that compares weekly progress and overall progress for last n weeks
    def past_history(goal):
        full_dict = weeks_report(goal, limit)
        conseq_dik = calculi.conseq_add(full_dict)
        all_list = list(full_dict.values())
        conseq_list = list(conseq_dik.values())
        return calculi.multiple_line(all_list, conseq_list, '', '', 'pygal')

    def past_focus(goal, number):
        dictionay = past_study(goal, number)
        title = 'Top ' + goal + 's for past '+str(number)+' weeks'
        x_axis = goal + 's'
        return calculi.bar_graph(dictionay, title, x_axis, 'pygal')
    past = 5

    top_topic = get_top('topic', limit)
    top_subject = get_top('project', limit)
    week_time = conseq_add('week')
    finished = done_proj('project')
    one_proj = one_summary('topic', 'project', working_proj)
    portfolio_proj = one_summary('topic', 'project', 'portfolio')
    study_proj = one_summary('topic', 'project', 'study.db')
    store_proj = one_summary('topic', 'project', 'store2')
    bakery_proj = one_summary('topic', 'project', 'bakery')
    debate_proj = one_summary('topic', 'project', 'debate')


    past_time = past_history('week')
    past_proj = past_focus('project', past)
    past_topic = past_focus('topic', past)

    return render_template('hi.html', top_topic=top_topic, top_subject=top_subject,
                           week_time=week_time, finished=finished, one_proj=one_proj,
                           past_time=past_time, past_proj=past_proj, past_topic=past_topic,
                           store_proj=store_proj, bakery_proj=bakery_proj, debate_proj=debate_proj,
                           portfolio_proj=portfolio_proj, study_proj=study_proj)


if __name__ == '__main__':
    app.run(debug=True)
# # #
