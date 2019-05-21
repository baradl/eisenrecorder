import datetime
from tabulate import tabulate
import helper as he
import converter as conv
import filter


START = datetime.date(2019, 3, 1).isocalendar()[1] - 1

def summary_run(db, ret = False):
    global START
    current_week = datetime.date(he.year_now(),
                                 he.month_now(), he.day_now()).isocalendar()[1]
    
    headers = ["Week", "Number", "Distance", "Time", "Pace", "Fastest Run", "Longest Run"]
    
    content = []
    
    for week in range(START, current_week):
        runs = weekly_runs(db,week)
        #if runs == []: continue
        summary_float = summary_week(runs)
        
        time = conv.convert_float_totime(summary_float[1])
        pace = conv.convert_float_totime(summary_float[2])
        
        fastest = fastest_run(runs)
        if fastest == None:
            out_fastest = "-"
        else:
            fastest_stats = fastest["run"]
            pace_fastest = conv.convert_float_totime(fastest_stats[2])
            dist_fastest = fastest_stats[0]
            out_fastest = str(dist_fastest)+ "   @ " + pace_fastest
        
        
        longest = longest_run(runs)
        if longest == None:
            out_longest = "-"
        else:
            longest_stats = longest["run"]
            pace_longest = conv.convert_float_totime(longest_stats[2])
            dist_longest = longest_stats[0]
            out_longest = str(dist_longest) + "   @ " + pace_longest
            
        summary_string = [str(week-START+1), str(len(runs)) ,str(summary_float[0]),
                          time, pace, out_fastest, out_longest]
        content.append(summary_string)
        
    
    out = tabulate(content, headers)
    print(out)
    if ret: return out
        
    


def weekly_runs(db, week, year = datetime.datetime.now().year):
    start, end = he.start_end_week(year, week)
    
    runs = filter.filter_consecutive_days(db, start, end, "run")    
    return runs


def fastest_run(runs):
    if runs == []:
        return None
    paces = []
    for run in runs:
        stats = run["run"]
        paces.append(stats[2])
    return runs[paces.index(min(paces))]

def longest_run(runs):
    if runs == []: 
        return None
    dists = []
    for run in runs:
        stats = run["run"]
        dists.append(stats[0])    
    return runs[dists.index(max(dists))]

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