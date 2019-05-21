"""
Collection of filters which prepare for statistical analysis of the bulk of 
workouts
"""

import helper as he
import request as re


STR_TYPES = ["SQ", "DL", "BP", "UB", "LB"]



def filter_filtered(cursor, type_):
    global STR_TYPES
    
    if type_ != "strength": 
        assert type_ in re.TYPES
    
    filtered_cursor = []
    
    for doc in cursor:
        if type_ == "strength" and doc["type"] in STR_TYPES:
            filtered_cursor.append(doc)
        
        elif doc["type"] == type_:
            filtered_cursor.append(doc)
           
    return filtered_cursor
            
        

def filter_type(db, session_type):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    if type(session_type) == str:
        session_type = [session_type]
    
    for doc in cursor:
        if doc["type"] in session_type:
            filtered.append(doc)
            
    return filtered


def filter_consecutive_days(db, start, end, type_):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    if type(start) == str and len(start) > 3:
        start = he.get_day_in_year(start)
    if type(end) == str and len(end) > 3:
        end = he.get_day_in_year(end)
    
    
    for doc in cursor:
        day = doc["day"]
        if day >= start and day <= end:
            filtered.append(doc)
    
    if type_: return filter_filtered(filtered, type_)
    return filtered


def filter_days(db, day_list, *type_):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    
    for doc in cursor:
        if doc["day"] in day_list:
            filtered.append(doc)
    
    if type_: return filter_filtered(filtered, type_)        
    return filtered


def filter_exercise(db, exercise):
    col = db["AllSessions"]
    cursor = col.find().sort("day")
    filtered = []
    days = []
    
    for doc in cursor:
        if doc["type"] != "off" and doc["type"] != "run":
            if exercise in doc["exercise list"]:
                exercise_as_list, day = he.get_exercise(doc, exercise)
                days.append(day)
                filtered.append(exercise_as_list)
            
    return filtered, days
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    