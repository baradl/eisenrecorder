import datetime
from tabulate import tabulate
import helper as he
import converter as conv
import filter
from termcolor import colored


START = datetime.date(2019, 3, 1).isocalendar()[1] - 1

def summary_run(db, ret = False):
    global START
    current_week = datetime.date(he.year_now(),
                                 he.month_now(), he.day_now()).isocalendar()[1]
    
    headers = ["Week", "Number", "Distance", "Time", "Pace", "Fastest Run", "Longest Run"]
    
    content = []
    
    all_dist = []
    all_time = []
    all_pace = []
    all_fast = []
    all_long = []
    
    for week in range(START, current_week):
        runs = weekly_runs(db,week)
        #if runs == []: continue
        summary_float = summary_week(runs)
        
        all_dist.append(summary_float[0])
        all_time.append(summary_float[1])
        if summary_float[2] == 0:
            all_pace.append(100)
            pace = "-"
        else:
            all_pace.append(summary_float[2])
            pace = conv.convert_float_totime(summary_float[2])
        time = conv.convert_float_totime(summary_float[1])
        
        
        fastest = fastest_run(runs)
        if fastest == None:
            out_fastest = "-"
            all_fast.append(1000)
        else:
            fastest_stats = fastest["run"]
            all_fast.append(fastest_stats[2])
            pace_fastest = conv.convert_float_totime(fastest_stats[2])
            dist_fastest = fastest_stats[0]
            out_fastest = str(dist_fastest)+ " at " + pace_fastest
            
            
        
        longest = longest_run(runs)
        if longest == None:
            out_longest = "-"
            all_long.append(-1)
        else:
            longest_stats = longest["run"]
            all_long.append(longest_stats[0])
            pace_longest = conv.convert_float_totime(longest_stats[2])
            dist_longest = longest_stats[0]
            out_longest = str(dist_longest) + " at " + pace_longest
        
        
        
        summary_string = [str(week-START+1), str(len(runs)) ,str(summary_float[0]),
                          time, pace, out_fastest, out_longest]
        content.append(summary_string)
        
    dist_index = all_dist.index(max(all_dist))
    time_index = all_time.index(max(all_time))
    pace_index = all_pace.index(min(all_pace))
    fastest_index = all_fast.index(min(all_fast))
    longest_index = all_long.index(max(all_long))
    
    content = color_content(content, dist_index, time_index, pace_index, 
                            fastest_index, longest_index)
    
    
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


def color_content(content, index_dist, index_time, index_pace, index_fastest, index_longest):
    dist = content[index_dist]
    time = content[index_time]
    pace = content[index_pace]
    longest = content[index_longest]
    fastest = content[index_fastest]
    
    text_color = "grey"
    backround_color = "on_cyan"
    
    dist[2] = colored(dist[2], text_color, backround_color)
    time[3] = colored(time[3], text_color, backround_color)
    pace[4] = colored(pace[4], text_color, backround_color)
    fastest[5] = colored(fastest[5], text_color, backround_color)
    longest[6] = colored(longest[6], text_color, backround_color)
    
    return content
    