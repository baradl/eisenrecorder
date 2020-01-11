import datetime
from datetime import timedelta
from tabulate import tabulate
from parsing import converter
from utils import check
import os, glob

STRENGHT_TYPES = ["SQ", "DL", "BP", "UB", "LB"]

def day_now():
    return datetime.datetime.now().day

def month_now():
    return datetime.datetime.now().month

def year_now():
    return datetime.datetime.now().year

def today():
    day = day_now()
    month = month_now()
    year = year_now()
    tod = str(day) + "." + str(month) + "." + str(year)
    return tod

def monthly_days(year=None):
    if year is None:
        year = year_now()
    days = [31,28,31,30,31,30,31,31,30,31,30,31]
    if leap(year): days[1] = 29
    
    return days

def leap(year):
    if year % 4 == 0: return True
    else: return False

def get_day_in_year(date):
    date = date.split(".")
    day = int(date[0])
    month = int(date[1])
    
    
    if len(date) == 2:
        year = str(year_now())
    else:
        year = date[2]
        if len(year) == 2:
            year = "20" + year
    
    assert len(year) == 4
    year = int(year)
    assert year >= 2019
    assert month <= 12
    days = monthly_days(year)
    assert day <= days[month-1]
    
    
    consecutive_days = 0
    year_ = 2019
    while year_ < year:
        consecutive_days += 365
        if leap(year_): consecutive_days += 1
        
        year_ += 1    
    
    for i in range(month-1):
        consecutive_days += days[i]
    
    return consecutive_days + day       

def get_week(date):
    [day, month, year] = converter.convert_date(date)
    
    if month == 1 and day<=6: return [0,6]
    
    month = converter.convert_to_month(month)
    month = month[:3]
    
    date_ = datetime.datetime.strptime(str(month) + " " + str(day) + " " + str(year), "%b %d %Y")
    
    weekday = date_.weekday()
    
    start = get_day_in_year(date) - weekday
    end = get_day_in_year(date) + (7 - weekday)
    
    
    return [start, end]


def indexes_max(array):
    maxi = max(array)
    index = []
    i = 0
    while i < len(array):
        if array[i] == maxi: 
            index.append(i)
        i+=1
        
    return index


def start_end_week(year, calendar_week):
    
    assert year >= 2019       
    if calendar_week == 0: return 0,6
    
    monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
    sunday = monday + datetime.timedelta(days=6.9)
    
    start = str(monday.day) + "." + str(monday.month) + "." + str(monday.year)
    end   = str(sunday.day) + "." + str(sunday.month) + "." + str(sunday.year)
    
    start = get_day_in_year(start)
    end = get_day_in_year(end)
    return start, end

def days_in_month(month):
    if type(month) == str:
        if len(month) <= 2: month = converter.convert_to_month(int(month))
    elif type(month) == int: month = converter.convert_to_month(month)
    
    months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]
    
    days_in_months = monthly_days()
    
    index = months.index(month)
    return days_in_months[index]


def indent(): 
    return "_______________________________________________________________________________"

def string_to_list(string, sep = ","):
    list_ = string.split(sep)
    for i in range(len(list_)):
        try: list_[i] = int(list_[i])
        except: 
            try: list_[i] = float(list_[i])
            except: list_[i] = str(list_[i])
    return list_

def get_days_col(db):
    col = db["AllSessions"]
    if type(col) == str: col = db(col)
    
    days = []
    for document in col.find():
        days.append(int(document["day"]))
    return days

def get_days_dir():
    directory = "../../backup"
    os.chdir(directory)
    files = glob.glob("*.txt")
    days = []
    for file in files:
        file = file.replace(".txt","")
        file = int(file)
        days.append(file)
    return days


def divide_int_list(int_list):
    n = len(int_list)
    div = [[int_list[0]]]
    j = 0
    for i in range(1,n):
        if int_list[i] == int_list[i-1]:
            div[j].append(int_list[i])
        else: 
            div.append([int_list[i]])
            j += 1
    return div


def delete_ints(int_list, to_delete, number = 1):   
    for i in range(number):
        assert to_delete in int_list
        int_list.remove(to_delete)


def find_substring_in_stringlist(stringlist, substring):
    result = []
    
    for string in stringlist:
        substring = substring.lower()
        stringnew = string.lower()
        if substring in stringnew: result.append(string)
    
    return result

def swap(x1,x2):
    xh = x1
    x1 = x2
    x2 = xh
    return [x1,x2]      

def get_exercise(doc, exercise):
    assert doc["type"] != "run"
    assert doc["type"] != "off"
    
    assert exercise in doc["exercise list"]
    
    for i in range(doc["amount of exercises"]):
        ex = doc["exercise" + str(i+1)]
        if ex[0] == exercise: return ex, doc["day"]


def abbreviation():
    abbrev = tabulate([['BP', "Benchpress"],
                    ["CGBP", "Closegrip-Benchpress"],
                    ["OHP","Overheadpress"],
                    ["Inc-BP", "Incline-Benchpress"],
                    ["DB", "Dumbell"],
                    ["BB", "Barbell"],
                    ["FP","Face-Pulls"],
                    ["Bi", "Biceps"],
                    ["Tri", "Triceps"],
                    ["PD1","Pushdown one arm"],
                    ["PD2","Pushdown two arms"],
                    ["OH1","Overhead Tricep one arm"],
                    ["OH2","Overhead Tricep two arms"],
                    ["M", "Machine"],
                    ["HC","Hammercurls"],
                    ["RFly", "Reverse-Fly"],
                    ["SH", "Seitheben"],
                    ['DL', "Deadlift"],
                    ["Sumo-DL", "Sumo-Deadlift"],
                    ["RDL","Romanian Deadlift"],
                    ["LZ(b)", "Lat-Zug (breit)"],
                    ["LZ(e)", "Lat-Zug (eng)"],
                    ["KZ(e)", "Klimmzug (eng)"],
                    ["KZ(b)", "Klimmzug (breit)"]],
            headers=['Abbreviation', 'Exercise'])
    
    print(indent())
    print("\n")    
    print(abbrev)    
    print(indent())