from utils import check
from parsing import converter
from utils.helper import year_now


def get_date_from_user():
    dec = input("Current month and year [y/n]: ")
    if dec == "y": 
        year = str(year_now())
        month = str(converter.convert_month_to_int(str(he.month_now())))
    else:
        year = input("Year: ")
        month = input("Month: ")
        month = str(converter.convert_month_to_int(month))
        
    
    day = input("Day: ")
    day = check.check_day(day)
    
    if len(day) == 1: day = "0" + day
    if len(month) == 1: month = "0" + month
    if len(year) ==2: year = "20" + year
    
    date = day + "." + month + "." + year
    return date

def construct_exercises():
    exercises = []
    while True:
        exercise = input("Exercise: ")
        if len(exercise) < 4: break
        exercise = converter.convert_input(exercise)
        exercises.append(exercise)
    return exercises

def construct_run():
    stats = input("Distance in km and time in minutes (dis time): ")
    run = converter.convert_run(stats)
    return run

def contruct_hike():
    dis = float(input("Distance [km]: "))
    height = float(input("Height meter: "))
    minutes, seconds = converter.convert_time_tofloat(input("Time: "))
    time = minutes + seconds/60
    hike = [dis, height, time]

    return hike