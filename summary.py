import datetime
import helper as he
import filter
from tabulate import tabulate
import converter as conv

START = datetime.date(2019, 3, 1).isocalendar()[1] - 1

def summary_run(db, output = True):
    global START
    current_week = datetime.date(he.year_now(),
                                 he.month_now(), he.day_now()).isocalendar()[1]
    
    headers = ["Week", "Distance", "Time", "Pace"]
    
    content = []
    
    for week in range(START, current_week):
        runs = weekly_runs(db,week)
        summary_float = summary_week(runs)
        time = conv.convert_float_totime(summary_float[1])
        pace = conv.convert_float_totime(summary_float[2])
        summary_string = [str(week-START+1), str(summary_float[0]) , time, pace]
        content.append(summary_string)
        
    
    out = tabulate(content, headers)
    print(out)
        
    


def weekly_runs(db, week, year = datetime.datetime.now().year):
    start, end = he.start_end_week(year, week)
    
    weekly_sessions = filter.filter_consecutive_days(db, start, end)
    runs = []
    for doc in weekly_sessions:
        if doc["type"] == "run": runs.append(doc)
    
    return runs


def summary_week(runs):
    if runs == []: return 0,0,0
    total_distance = 0
    total_time = 0
        
    for doc in runs:
        stats = doc["run"]
        total_distance += stats[0]
        total_time += stats[1]
    
    pace = total_time/total_distance
    
    return total_distance, total_time, pace
        