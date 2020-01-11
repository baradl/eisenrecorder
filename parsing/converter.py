from utils import helper as he
import math

def convert_to_month(month):
    assert  type(month) is int or type(month) is str
    
    if type(month) is int: assert month in range(1,13)
    
    try: month = int(month)
    except:
        month = month.lower()
        month = month[0:3]
        months_abbrev = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        if type(month) is str: 
            if len(month) > 3: month = month[:3]
            month.lower()
            month = months_abbrev.index(month) + 1
        
    months = ["January", "February", "March", "April","May", "June", "July",
              "August", "September", "October", "Novemver", "December"]
    return months[month - 1]
    

def convert_month_to_int(month):
    assert type(month) is str
    
    try: 
        month = int(month)
        return month
    except:
        month = month.lower()
        month = month[0:3]
        months_abbrev = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug",
                         "sep", "oct", "nov", "dec"]
        return months_abbrev.index(month) + 1
   
    
def convert_input(exercise):
    exercise = exercise.split()
    
    assert len(exercise) <= 4
    assert len(exercise) >= 3
    
    if len(exercise) == 4:
        exercise[1] = int(exercise[1])
        exercise[2] = int(exercise[2])
        try: exercise[3] = int(exercise[3])
        except: 
            try: exercise[3] = float(exercise[3])
            except: exercise[3] = str(exercise[3])
    else:
        exercise[1] = he.string_to_list(string = exercise[1])
        exercise[2] = he.string_to_list(string = exercise[2])
        n1 = len(exercise[1])
        n2 = len(exercise[2])
        if n1 < n2:
            assert n1 == 1
            exercise[1] = exercise[1] * n2
        elif n1 > n2:
            assert n2 == 1
            exercise[2] = exercise[2] * n1
    return exercise

def convert_ciruit_exercise(exercise):
    exercise = exercise.split()

    assert len(exercise)==3

    exercise
  
def convert_run(string):
    stats = string.split()
    distance = float(stats[0])
    [minutes, seconds] = convert_time_tofloat(stats[1])
    time = minutes + (seconds/60)
    pace = time/distance
    return [distance, time, pace]


def convert_time_tofloat(time):
    time = time.split(":")
    if len(time) == 3:
        hours = int(time[0])
        minutes = int(time[1])
        seconds = int(time[2])
        minutes += hours * 60
    elif len(time) == 2:
        minutes = int(time[0])
        seconds = int(time[1])
    else: 
        minutes = int(time[0])
        seconds = 0
    return [minutes, seconds]

def convert_float_totime(time):
    minutes = math.floor(time)
    seconds = time - minutes
    
    seconds = round(seconds * 60)  
    seconds = str(seconds)
    
    if len(seconds) < 2:
        seconds = "0" + seconds
        
    if minutes >= 60: 
        hours = math.floor(minutes/60)
        minutes = minutes - 60*hours
        return str(hours) + ":" + str(minutes) + ":" + seconds
    return str(minutes) + ":" + seconds


    
def convert_date(string):
    date = he.string_to_list(string, sep = ".")
    
    day = date[0]
    month = date[1]
    
    if len(date) == 3:
        year = date[2]
        if len(str(year)) == 2: 
            year = "20" + str(year)
            year = int(year)
    else: year = str(he.year_now())
    
    return [day, month, year] 


def convert_int_todate(day):
    day_ = day
    year = 2019
    
    while day_ > 0:
        days_in_year = 365
        if he.leap(year): days_in_year += 1
        
        if day_ - days_in_year >= 0: 
            year += 1
            day -= days_in_year
            
        day_ -=  days_in_year  
    
    assert day < 365
    
    monthly_days = he.monthly_days(year)
    
    month = 1
    while sum(monthly_days[:month-1]) < day:
        month += 1
    
    month -= 1 
    
    day = day - sum(monthly_days[:month-1])
    
    day = str(day)
    month = str(month)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    
    return day + "." + month + "." + str(year)
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
