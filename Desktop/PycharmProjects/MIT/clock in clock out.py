import datetime
import sqlite3

time = datetime.datetime.now()

# since i started adding data in 2019 it gives me 0
# 52 is number weeks a year, so first week of 2020 I am going to have 52 weeks recorded

modifier = (time.year - 2019) * 52



# use this list in several occasions in order to determine day of the week
day_of_week=(['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
empty=0
# study time before database
before = 57

# time calculation formulas
# calculate total time from multiple 'total' column
def cal_time(total1):
    min1=0
    hrs = 0
    for t in total1:
        t=t[0]
        t = (str(t))
# check if ':' in data because if we are currently recording our 'total' value is 0
# we calculate values only from completed rows
        if ":" in t:
            hrs += int(t[0:2])
            min1 += int(t[3:5])
            total1= ((str(hrs + min1 // 60) + ":" + str(min1 % 60)))
    return total1

#table formulas
# we created a class for our functions so that we only need to make load, make
# cursor object, and close statement only once
# out code is shorter and looks better if all database manipulations use classes
class Database:
    def __init__(self, db):
        self.conn=sqlite3.connect("check in and out.db")
        self.cur=self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS study "
                    "(id,"
                    "week,"
                    "date,"
                    "day,"
                    "start,"
                    "end,"
                    "total,"
                    "project,"
                    "topic)")
        self.conn.commit()

#s
# output how much time elapsed since we started activity
# calculate time difference to 'total' cell deference is between 'start' and 'current time'
    def last_cell_time(self,):
        self.cur.execute("SELECT*FROM study")
# select last item from table and in [4] possition that is our 'time started' value
# t1 is started, t2 is current time. Use it to find difference
        t1 = str(self.cur.fetchall()[-1][4])
        t2 = str(time.time())[0:5]
        hrs1 = int(t1[0:2])
        min1 = int(t1[3:5])
        hrs2 = int(t2[0:2])
        min2 = int(t2[3:5])
        min_t1 = hrs1 * 60 + min1
        min_t2 = hrs2 * 60 + min2

#calculate difference between two times  to calculate 'total' time
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

# use this condition in case we started and 11 pm and finished at 1 am
# 1440 is number of minutes in a day
        if hrs2 >= hrs1:
            time_delta()
        elif hrs2 < hrs1:
            min_t2 += 1440
            time_delta()
        t_total = (time_delta())
        return t_total

# on
# add new values to the SQL
    def insert(self,id, week,date,day_week, time_in, time_out,time_total,project, subject):
        self.cur.execute("INSERT INTO study VALUES(?,?,?,?,?,?,?,?,?)",(id, week,date,day_week, time_in, time_out, time_total,project, subject))
        self.conn.commit()

# off
# used to finish current section and calculates time spent on task
    def done_studying(self):
        self.cur.execute("SELECT*FROM study")
        t1 = str(self.cur.fetchall()[-1][4])
        t2 = str(time.time())[0:5]
        self.cur.execute("UPDATE study SET end=?,total=? WHERE start=?", (t2, database.last_cell_time(), t1))
        self.conn.commit()
# new
# creates new row for specified items
    def new(self,id, week,date,day_week, time_in, time_out,time_total,project, subject):
        self.cur.execute("INSERT INTO study VALUES(?,?,?,?,?,?,?,?,?)",(id, week,date,day_week, time_in, time_out, time_total,project, subject))
        print("happy studying")
        self.conn.commit()
# up
# updates specific row with values and condition we are been provided
#(new, old) when manual update method
    def update(self):
        self.cur.execute("UPDATE study SET total=? WHERE total=?", ('00:30', '1:15'))
        self.conn.commit()
# v
# view all database
    def view(self):
        self.cur.execute("SELECT * FROM study")
        rows=self.cur.fetchall()
        return rows
# s
# returns ammout you been working on a current task
    def study_time(self):
        return database.last_cell_time()

# w
# amount of time spent a week
    def study_report_week(self,week_id):
        self.cur.execute("SELECT total FROM study WHERE id=(?)",(week_id,))
        all=self.cur.fetchall()
        self.conn.commit()
        return cal_time(all)

    def week_tot(self,week_num):
        self.cur.execute("SELECT total FROM study WHERE week=(?)",(week_num,))
        all=self.cur.fetchall()
        self.conn.commit()
        return cal_time(all)

# tot
# extract all total columns in order to calculatee total time from the start
    def total(self):
        self.cur.execute("SELECT total FROM study")
        all = self.cur.fetchall()
        self.conn.commit()
        time = cal_time(all)
        hr = time.split(':')
        return str(int(hr[0])+ before)+ ':'+hr[1]
        # return (type(time))
# d
# returns how much spent a day
    def day_report(self, date):
        self.cur.execute("SELECT total FROM study WHERE date=?",(date,))
        rows = self.cur.fetchall()
        self.conn.commit()
        return cal_time(rows)

#select last row of total to determine if our recording started or not
    def return_last_total(self, week_id):
        self.cur.execute("SELECT total FROM study WHERE id=(?)",(week_id,))
        all=self.cur.fetchall()[-1]
        print(all)
        self.conn.commit()
        return cal_time(all)

# wb
# time spent per day of particular week
    def week_breakdown_by_day(self, week, day):
        self.cur.execute("SELECT total FROM study WHERE week=? and day = ?", (week, day))
        all = self.cur.fetchall()
        self.conn.commit()
        return cal_time(all)


# this section of code is for all the options for the code
# import our database that been created by sqlite
database=Database("inventory.db")


# options that that user has to view data
print("enter 'on' to start studying, enter 'off' to stop studying")
print(" 's' for current time, 'w' current week time, 'v' view all"
      "'wb' breakdown by day of week, 'd' for daily total, 'tot' for all time total, 'wbs' for custom week")
print("'ds' foor custom day")

# we relly on input value to determine what we want to do
menu= input("so what do you want to do today?  ")


# start recording
if menu=='on':
    if (database.view()[-1][-3])==0:
        print("you are already recording your study time")
    else:
        topicS = (input("topic(SQL, syntax, highcharts: "))
        projectsS= (input("what in particular(PROJECT, CHEKIO, MIT, study.db, review analysis): ")).lower()
        # I used '-25 + modifier' because I wanted to make sure that my beginning week in 1
        # '-25' is a week number I started this project
        weeekS = time.isocalendar()[1] - 25 + modifier
        # get all dateframe values that we are going to put into out table
        idS = str(time.month) + str(weeekS)
        dateS = str(time.date())
        day = day_of_week[time.isoweekday() - 1]
        time_inS=str(time.time())[0:5]
        time_outS= 0
        time_totalS=0
        database.insert(idS, weeekS, dateS, day, time_inS, time_outS, time_totalS, projectsS,topicS)

# stop recording
if menu=='off':
    if (database.view()[-1][-3])==0:
        database.done_studying()
        print("please come again")
        print(str(database.study_time()) + " last study time")
        print(str(database.day_report(time.date()) + " you studied today"))
    else:
        print("you haven't started studying yet")

# all table
if menu=='v':
    print(database.view())

# current study time
if menu=='s':
    print(str(database.study_time())+ " is your current study time")

# daily total so far
if menu=='d':
    print(str(database.day_report(time.date()) + " you studied today"))

if menu=='ds':
    print("date format 2019-07-10")
    date = input("enter your day you want to check: ")
    print(str(database.day_report(time.date()) + " you studied that day"))

# total time for current week
if menu == 'w':
    weeekS = time.isocalendar()[1] - 25 + modifier
    idS = str(time.month) + str(weeekS)
    print((database.week_tot(weeekS))+ " you studied this week")

if menu == "wb":
    week = time.isocalendar()[1] - 25 + modifier
    print("find hours total for week and each day")
    print("input week # please")
    print("current is " + str(week))
    week_num = input("enter your value")
    for x in day_of_week:
        print(str(database.week_breakdown_by_day(int(week_num), x)) + ' ' + x)
    print((database.week_tot(int(week_num))) + " total")


if menu == 'tot':
    print(database.total() + " is your total time so far, keep it up!!!")
#don't touch

# custom update options if user wasn't able to ran program and record time
if menu == "new":
    topicS = "GCP"
    projectsS = "anki"
    weeekS = time.isocalendar()[1] - 25 + modifier
    # weeekS = 59
    idS = str(time.month) + str(weeekS)
    dateS = '2020-10-21'
    day = day_of_week[time.isoweekday() - 1]
    time_inS = "14:00"
    time_outS = "14:15"
    time_totalS = "00:15"
    database.new(idS, weeekS,dateS,day, time_inS, time_outS,time_totalS,projectsS, topicS)

if menu == 'up':
    database.update()
