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
    stats = input("Distance [km] and time [hh:mm:ss] (dis time): ")
    run = converter.convert_run(stats)
    return run

def contruct_hike():
    dis = float(input("Distance [km]: "))
    height = float(input("Height [m]: "))
    minutes, seconds = converter.convert_time_tofloat(input("Time: "))
    time = minutes + seconds/60
    hike = [dis, height, time]
    return hike

def construct_cardio():
    stats = input("Speed [km/h] and Time [hh:mm:ss]  (speed time): ")
    run = converter.convert_run(stats)

    rounds = int(input("Number of circuit rounds: "))

    circuit = [rounds]
    while True:
        exercise = input("Exercise: ")
        if len(exercise)<3:
            break
        exercise = exercise.split()
        exercise[1] = parse_exercise_data(exercise[1])
        exercise[2] = parse_exercise_data(exercise[2])

        circuit.append(exercise)
    
    return [run[:2], circuit]

def parse_exercise_data(exercise_data):
    try:
        exercise_data = int(exercise_data)
    except:
        try: 
            exercise_data = float(exercise_data)
        except:
            pass
    
    return exercise_data

        
        

