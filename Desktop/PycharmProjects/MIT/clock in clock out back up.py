import datetime
import sqlite3

menu = input("on ,of, view, study time")

time = datetime.datetime.now()
modifier = (time.year-2019)*52
day_of_week = (['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
empty=0

#time calculation formulas
#calulate total time from multiple 'total' column
def cal_time(total1):
    min1 = 0
    hrs = 0
    # print(total1)
    for t in total1:
        # print(t)
        t=t[0]
        t = (str(t))
        if ":" in t:
            hrs += int(t[0:2])
            min1 += int(t[3:5])
            total1 = ((str(hrs + min1 // 60) + ":" + str(min1 % 60)))
        # else:
        #     last=study_time()
        #     hrs = int(total1[0:2])+int(last[0:2])
        #     min1 = int(t[3:5])+int(last[3:5])
        #     total1 = ((str(hrs + min1 // 60) + ":" + str(min1 % 60)))



    return total1

#calculate time difference to 'total' cell deference is between 'start' and 'current time'
def last_cell_time():
    conn = sqlite3.connect("check in and out.db")
    cur = conn.cursor()
    cur.execute("SELECT*FROM study")
    t1 = str(cur.fetchall()[-1][4])
    t2 = str(time.time())[0:5]
    hrs1 = int(t1[0:2])
    min1 = int(t1[3:5])
    hrs2 = int(t2[0:2])
    min2 = int(t2[3:5])
    min_t1 = hrs1 * 60 + min1
    min_t2 = hrs2 * 60 + min2

    def time_delta():
        total_s = min_t2 - min_t1
        hr = str(total_s // 60)
        min_t = str(total_s % 60)
        if len(hr) == 1:
            hr = ('0' + hr)
        if len(min_t) == 1:
            min_t = ('0' + min_t)
        t_total = (hr + ':' + min_t)
        return t_total

    if hrs2 >= hrs1:
        time_delta()
    elif hrs2 < hrs1:
        min_t2 += 1440
        time_delta()
    # print(time_delta() + ' is your study time')
    t_total = (time_delta())
    return t_total



#table formulas
def start():
    menu=input("enter 's' to start, 'w' for week total, 'd' for each day of week, 'q' for week by subject")
    work=input("press 't' for how long been already,'w' for week total, 'd' for each day of week, 'q' for week by subject")

def create_table():
    conn=sqlite3.connect("check in and out.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS study "
                "(id,"
                "week,"
                "date,"
                "day,"
                "start,"
                "end,"
                "total,"
                "project,"
                "topic)")
    conn.commit()
    conn.close()
create_table()

#on
def insert(id, week,date,day_week, time_in, time_out,time_total,project, subject):
    conn=sqlite3.connect("check in and out.db")
    cur=conn.cursor()
    cur.execute("INSERT INTO study VALUES(?,?,?,?,?,?,?,?,?)",(id, week,date,day_week, time_in, time_out, time_total,project, subject))
    print("happy studying")
    conn.commit()
    conn.close()


#up
#(new, old) when manual update method
def update():
    conn = sqlite3.connect("check in and out.db")
    cur=conn.cursor()
    cur.execute("SELECT*FROM study")
    cur.execute("UPDATE study SET total=? WHERE total=?", ('00:35',"0:35",))
    conn.commit()
    conn.close()
#v
def view():
    conn = sqlite3.connect("check in and out.db")
    cur=conn.cursor()
    cur.execute("SELECT*FROM study")
    rows=cur.fetchall()
    return rows
#s
def study_time():
    return (last_cell_time())
#off 
def done_studying():
    conn = sqlite3.connect("check in and out.db")
    cur=conn.cursor()
    cur.execute("SELECT*FROM study")
    t1 = str(cur.fetchall()[-1][4])
    t2 = str(time.time())[0:5]
    cur.execute("UPDATE study SET end=?,total=? WHERE start=?",(t2,last_cell_time(),t1))
    conn.commit()
    conn.close()
#w
def study_report_week(week_id):
    conn = sqlite3.connect("check in and out.db")
    cur = conn.cursor()
    cur.execute("SELECT total FROM study WHERE id=(?)",(week_id,))
    all=cur.fetchall()
    conn.commit()
    conn.close()
    return cal_time(all)
#z
def study_report_custom(parameter1, parameter2, parameter3):
    # print(value1)
    print(parameter1)
    print(parameter2)
    print(parameter3)
    conn = sqlite3.connect("check in and out.db")
    cur = conn.cursor()
    cur.execute("SELECT total FROM study WHERE ? = 61",(parameter2,))
    rows=cur.fetchall()
    print(rows)
    conn.commit()
    conn.close()
    return rows
#d
def day_report(date):
    #establish connection with database
    conn = sqlite3.connect("check in and out.db")
    #make cursor
    cur = conn.cursor()
    cur.execute("SELECT total FROM study WHERE date=?",(date,))
    rows = cur.fetchall()
    # have to commit so that data is changed
    conn.commit()
    # have to close database
    conn.close()
    return cal_time(rows)

#secect last row of total to determine if our recording started or not
def return_last_total(week_id):
    conn = sqlite3.connect("check in and out.db")
    cur = conn.cursor()
    cur.execute("SELECT total FROM study WHERE id=(?)",(week_id,))
    all=cur.fetchall()[-1]
    print(all)
    conn.commit()
    conn.close()
    return cal_time(all)

#wb
def week_breakdown_by_day(week, day):
    conn = sqlite3.connect("check in and out.db")
    cur = conn.cursor()
    cur.execute("SELECT total FROM study WHERE id=? and day = ?",(week, day))
    all=cur.fetchall()
    # print(all)
    conn.commit()
    conn.close()
    return cal_time(all)

#don't touch
if menu=='on':
    if (view()[-1][-3])==0:
        print("you are already recording your study time")
    else:
        topicS = (input("topic(SQL, syntax,: "))
        projectsS= (input("what in particular(PROJECT, CHEKIO, MIT): ")).lower()
        weeekS = time.isocalendar()[1] - 25 + modifier
        idS = str(time.month) + str(weeekS)
        dateS = str(time.date())
        day = day_of_week[time.isoweekday() - 1]
        time_inS = str(time.time())[0:5]
        time_outS = 0
        time_totalS = 0
        insert(idS, weeekS, dateS, day, time_inS, time_outS, time_totalS, projectsS, topicS)
if menu=='off':
    if (view()[-1][-3]) == 0:
        done_studying()
        print("please come again")
        print(str(study_time()) + " last study time")
        print((day_report(time.date()) + " you studied today"))
    else:
        print("you haven't started studying yet")
if menu=='v':
    print(view())
if menu=='s':
    print(str(study_time()) + " is your current study time")
if menu=='d':
    print((day_report(time.date()) + " you studied today"))

if menu == 'w':
    weeekS = time.isocalendar()[1] - 25 + modifier
    idS = str(time.month) + str(weeekS)
    print((study_report_week(idS))+ " you studied this week")
    print("breakdown by day")

if menu == "wb":
    weekID = str(72)
    for x in day_of_week:
        print(str(week_breakdown_by_day(weekID, x)) + x)
    print((study_report_week(weekID)) + " total")
#don't touch

if menu=='b':
    for day in day_of_week:
        weekS = time.isocalendar()[1] - 25 + modifier
        idS = str(time.month) + str(weekS)
        print((day + " "+break_down_by_day(idS, day)))

if menu == 'z':
    para1 = "total"
    para2 = "id"
    para3 = "10"
    print("SELECT (para1) FROM study WHERE (para2) = (para3)")
    print(study_report_custom(para1, para2, para3))

if menu == 'up':
    update()

#just in case need this
#b
# def break_down_by_day(week_id,days):
#     conn = sqlite3.connect("check in and out.db")
#     cur = conn.cursor()
#     cur.execute("SELECT total FROM study WHERE id=? and day=?",(week_id,days))
#     rows = cur.fetchall()
#     conn.commit()
#     conn.close()
#     return cal_time(rows)





#this works/back up
# def study_time():
#     conn = sqlite3.connect("check in and out.db")
#     cur = conn.cursor()
#     cur.execute("SELECT*FROM study")
#     t1 = str(cur.fetchall()[-1][4])
#     t2 = str(time.time())[0:5]
#     hrs1 = int(t1[0:2])
#     min1 = int(t1[3:5])
#     hrs2 = int(t2[0:2])
#     min2 = int(t2[3:5])
#     min_t1 = hrs1 * 60 + min1
#     min_t2 = hrs2 * 60 + min2
#
#     def time_delta():
#         total_s = min_t2 - min_t1
#         hr = str(total_s // 60)
#         min_t = str(total_s % 60)
#         if len(hr) == 1:
#             hr = ('0' + hr)
#         if len(min_t)==1:
#             min_t = ('0' + min_t)
#         t_total = (hr + ':' + min_t)
#         return t_total
#
#     if hrs2 >= hrs1:
#         time_delta()
#     elif hrs2 < hrs1:
#         min_t2 += 1440
#         time_delta()
#     t_total = (time_delta())
#     conn.commit()
#     conn.close()
#     return t_total
#
# def done_studying():
#     conn = sqlite3.connect("check in and out.db")
#     cur=conn.cursor()
#     cur.execute("SELECT*FROM study")
#     t1 = str(cur.fetchall()[-1][4])
#     t2 = str(time.time())[0:5]
#     hrs1 = int(t1[0:2])
#     min1 = int(t1[3:5])
#     hrs2 = int(t2[0:2])
#     min2 = int(t2[3:5])
#     min_t1 = hrs1 * 60 + min1
#     min_t2 = hrs2 * 60 + min2